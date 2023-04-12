docker-compose -f ./docker-compose.prod.yml down --remove-orphans
docker-compose -f ./docker-compose.prod.yml pull
docker-compose -f ./docker-compose.prod.yml up -d --build
docker-compose -f ./docker-compose.prod.yml run django python manage.py migrate
