# Use the official Python image as a base image
FROM python:3.12-slim

# Install system dependencies for mysqlclient
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your Flask app runs on (default is 5000)
EXPOSE 80

# Command to run your Flask application
CMD ["python", "app.py"]
