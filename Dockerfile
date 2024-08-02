FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /website_status

# Install dependencies
COPY requirements.txt /myproject/
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev python3-dev gcc \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install gunicorn \
    && pip install django-cors-headers

# Copy project
COPY . /myproject/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port your app runs on
EXPOSE 8080

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]