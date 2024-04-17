# syntax=docker/dockerfile:1

# Step 1: Use official Python image as the base image
FROM python:3.11-slim as builder

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 4: Install Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install "poetry==$POETRY_VERSION"

# Step 5: Copy only the files necessary for installing dependencies
COPY poetry.lock pyproject.toml ./

# Step 6: Install project dependencies
# Configure Poetry: do not create a virtual environment inside the Docker container
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Step 7: Copy the rest of your Django project
COPY . .

# Step 8: Run the application
# Collect static files
# RUN python manage.py collectstatic --noinput
# Make portdo 8000 available to the world outside this container
EXPOSE 8000
# Run the app. CMD can be overridden by providing a different command in the Docker run command
CMD ["gunicorn", "pslvis.wsgi"]
