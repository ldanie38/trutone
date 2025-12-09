#!/usr/bin/env bash
set -euo pipefail

DB_WAIT_RETRIES=${DB_WAIT_RETRIES:-30}
DB_WAIT_SLEEP=${DB_WAIT_SLEEP:-1}

echo "Entry point: waiting for database (up to ${DB_WAIT_RETRIES} seconds)..."

wait_for_db() {
  # 1) try pg_isready
  if command -v pg_isready >/dev/null 2>&1; then
    for i in $(seq 1 $DB_WAIT_RETRIES); do
      pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" >/dev/null 2>&1 && return 0
      sleep "$DB_WAIT_SLEEP"
    done
  fi

  # 2) try nc
  if command -v nc >/dev/null 2>&1; then
    for i in $(seq 1 $DB_WAIT_RETRIES); do
      nc -z "${POSTGRES_HOST:-db}" "${POSTGRES_PORT:-5432}" && return 0
      sleep "$DB_WAIT_SLEEP"
    done
  fi

  # 3) fallback to Python + psycopg2 if available
  for i in $(seq 1 $DB_WAIT_RETRIES); do
    python - <<'PY' && exit 0 || true
import os, sys
try:
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise SystemExit(1)
    import urllib.parse as up, psycopg2
    u = up.urlparse(url)
    conn = psycopg2.connect(dbname=u.path.lstrip('/'), user=u.username, password=u.password, host=u.hostname, port=u.port)
    conn.close()
    sys.exit(0)
except Exception:
    sys.exit(1)
PY
    sleep "$DB_WAIT_SLEEP"
  done

  return 1
}

if [ -n "${DATABASE_URL:-}" ]; then
  if ! wait_for_db; then
    echo "ERROR: database did not become available in time" >&2
    exit 1
  fi
  echo "Database ready"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if env provided (idempotent)
if [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ] && [ -n "${DJANGO_SUPERUSER_PASSWORD:-}" ] && [ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]; then
  echo "Ensuring superuser ${DJANGO_SUPERUSER_USERNAME} exists..."
  python - <<PY || true
from django.contrib.auth import get_user_model
User = get_user_model()
username = "${DJANGO_SUPERUSER_USERNAME}"
email = "${DJANGO_SUPERUSER_EMAIL}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
print("Superuser check done")
PY
fi

exec "$@"
