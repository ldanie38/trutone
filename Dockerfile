# Development Dockerfile
FROM python:3.9

# Keep Python behavior predictable in containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy only requirements first to leverage layer cache
COPY requirements.txt /app/requirements.txt

# Install dependencies (include dev deps in requirements-dev.txt if you have one)
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the project (optional for image-only workflows;
# in compose you'll typically mount the source as a volume)
COPY . /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq-dev postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Expose Django default dev port
EXPOSE 8000


# Default command for development: runserver with 0.0.0.0 so it's reachable from host
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
