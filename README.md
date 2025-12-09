# trutone

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver

##run tests##
python manage.py test

# rebuild web image if you changed Dockerfile or installed dj_database_url
docker compose --env-file .env -f docker/docker-compose.yml up --build -d



# if db is empty
docker compose --env-file .env -f docker/docker-compose.yml exec db psql -U trutone -d trutone -c "\dt"

# Restart the web container so the server notices applied migrations
docker compose --env-file .env -f docker/docker-compose.yml restart web

# Run migrations (creates all Django tables)

docker compose --env-file .env -f docker/docker-compose.yml run --rm web python manage.py migrate

# create superuser
docker compose --env-file .env -f docker/docker-compose.yml run --rm web python manage.py createsuperuser

# verify tables exist
docker compose --env-file .env -f docker/docker-compose.yml exec db psql -U trutone -d trutone -c "\dt"


# Access Django admin in your browser
# Open: http://localhost:8000/admin/ and log in with the superuser you created (username root in your run).

# collect static files if needed
docker compose --env-file .env -f docker/docker-compose.yml run --rm web python manage.py collectstatic --noinput

# Confirm env inside web
docker compose --env-file .env -f docker/docker-compose.yml exec web env | grep -E 'DATABASE_URL|POSTGRES'

# Test DB connectivity from web
docker compose --env-file .env -f docker/docker-compose.yml run --rm web sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\q"'

# tail logs
docker compose --env-file .env -f docker/docker-compose.yml logs -f db web

#Ruff#

Quick install & usage
Install pre‑commit: pip install pre-commit (or use your package manager).

Install hooks in your repo: pre-commit install.

Run on all files: pre-commit run --all-files.

In CI, add a step to run pre-commit run --all-files (or ruff check .) to fail builds on lint errors.