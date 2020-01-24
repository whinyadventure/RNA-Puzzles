version: "3.3"
services: 
  postgres:
    container_name: postgres
    restart: always
    image: postgres:latest
    environment:
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=${POSTGRES_DB}
    volumes:
      - ${POSTGRES_FOLDER}:/var/lib/postgresql
    ports:
    - "5432:5432"
  rabbitmq:
    container_name: rabbitmq
    restart: always
    image: rabbitmq:latest
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASSWORD}
    ports:
      - "5672:5672"

  django-migration:
    container_name: django-migration
    image: luki4824/rnapuzzles
    environment:
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
      - DB_HOST=postgres
      - DB_PORT=5432
    entrypoint: "python manage.py migrate"
    depends_on:
      - postgres

  django-collectstatic:
    container_name: django-collectstatic
    image: luki4824/rnapuzzles
    environment:
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
      - DB_HOST=postgres
      - DB_PORT=5432
    entrypoint: "python manage.py collectstatic --no-input"
  django:
    container_name: django
    restart: always
    image: luki4824/rnapuzzles
    environment:
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
      - DB_HOST=postgres
      - DB_PORT=5432
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_PORT=5672
      - RABBITMQ_USER=${RABBITMQ_USER}
      - RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD}
      - DEBUF=False
    ports:
      - "3000:3000"
    command: "RNAPuzzles.wsgi:application --bind=0.0.0.0:3000 --workers=2"
    depends_on:
      - postgres
      - rabbitmq
      - django-migration
      - django-collectstatic
      - celery
      - celery-beat
  celery:
    container_name: celery
    restart: always
    image: luki4824/rnapuzzles
    environment:
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
      - DB_HOST=postgres
      - DB_PORT=5432
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_PORT=5672
      - RABBITMQ_USER=${RABBITMQ_USER}
      - RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD}
      - DEBUF=False
    entrypoint: "celery worker -A RNAPuzzles -l info"
    depends_on:
      - postgres
      - rabbitmq
      - django-migration
      - django-collectstatic
    
  celery-beat:
    container_name: celery-beat
    restart: always
    image: luki4824/rnapuzzles
    environment:
      - DB_USER=${POSTGRES_USER}
      - DB_PASSWORD=${POSTGRES_PASSWORD}
      - DB_NAME=${POSTGRES_DB}
      - DB_HOST=postgres
      - DB_PORT=5432
      - RABBITMQ_HOST=rabbitmq
      - RABBITMQ_PORT=5672
      - RABBITMQ_USER=${RABBITMQ_USER}
      - RABBITMQ_PASSWORD=${RABBITMQ_PASSWORD}
      - DEBUF=False
    entrypoint: "celery beat -A RNAPuzzles -l info"
    depends_on:
      - postgres
      - rabbitmq
      - django-migration
      - django-collectstatic