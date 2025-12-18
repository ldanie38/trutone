# trutone

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser

python manage.py runserver

##run tests##
python manage.py test

# Use when you want to build and prepare the app but don’t need to watch logs (e.g., CI, background start).
make start 

# Use when you want to build and then immediately monitor the web service output during development or debugging.
make dev

# You can run the individual targets separately: make build, make collectstatic, make logs.

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

# from root
docker compose --env-file .env -f docker/docker-compose.yml ps


# run migrations
docker compose --env-file .env -f docker/docker-compose.yml exec web python manage.py migrate

# (optional) create admin user
docker compose --env-file .env -f docker/docker-compose.yml exec -it web python manage.py createsuperuser

# go to repo root, then restart web !!!!!!!!!!!!!!!!!!! ----- !!!!!!!!!!!!!!!!
cd /Users/luadaniele/trutone/trutone/trutone_repo
docker compose --env-file .env -f docker/docker-compose.yml up -d --build
docker compose --env-file .env -f docker/docker-compose.yml logs --tail=200 -f web
docker compose --env-file .env -f docker/docker-compose.yml run --rm web python manage.py collectstatic --noinput

# build and resTART
docker compose -f docker/docker-compose.yml --env-file .env build web
docker compose -f docker/docker-compose.yml --env-file .env up -d web


# check containers
docker compose -f docker/docker-compose.yml --env-file .env ps
# follow logs
docker compose -f docker/docker-compose.yml --env-file .env logs -f web
# run migrations and create superuser
docker compose -f docker/docker-compose.yml --env-file .env exec web python manage.py migrate
docker compose -f docker/docker-compose.yml --env-file .env exec web python manage.py createsuperuser




# quick check
curl -i http://localhost:8000/

# verbose debug
curl -v http://localhost:8000/


# Access Django admin in your browser
# Open: http://localhost:8000/admin/ and log in with the superuser you created (username root in your run).


# You should see the HTML from core/index.html (or the 200 response and your page content).
curl -i http://localhost:8000/


# collect static files if needed
docker compose --env-file .env -f docker/docker-compose.yml run --rm web python manage.py collectstatic --noinput

# Confirm env inside web
docker compose --env-file .env -f docker/docker-compose.yml exec web env | grep -E 'DATABASE_URL|POSTGRES'

# Test DB connectivity from web
docker compose --env-file .env -f docker/docker-compose.yml run --rm web sh -c 'PGPASSWORD="$POSTGRES_PASSWORD" psql -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\q"'

# tail logs
docker compose --env-file .env -f docker/docker-compose.yml logs -f db web

# print project urls
sed -n '1,200p' trutone/urls.py



# print view
sed -n '1,200p' core/views.py

# print template
sed -n '1,200p' core/templates/core/index.html



# or run locally
python manage.py runserver 8000

# then test
curl -i http://localhost:8000/
