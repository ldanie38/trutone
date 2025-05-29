# Use official Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000 for Django
EXPOSE 8000

# Run Django server

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

