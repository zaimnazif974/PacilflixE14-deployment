FROM python:3.10-slim-buster

WORKDIR /app

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=pacilflix.settings \
    PORT=8000 \
    WEB_CONCURRENCY=2 \
    DB_NAME=${DB_NAME} \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD} \
    DB_HOST=${DB_HOST} \
    DB_PORT=${DB_PORT}


# Install system packages required for Django and psycopg2.
RUN apt-get update --yes --quiet \
    && apt-get install --yes --quiet --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /requirements.txt

# Copy project code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --clear

# Run as non-root user (commented out if not needed)
# RUN chown -R django:django /app
# USER django

EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=5", "--threads=5", "pacilflix.wsgi:application"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
