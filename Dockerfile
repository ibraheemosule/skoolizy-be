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

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CMD ["python", "app.py"]
CMD make reset-migration && python app.py
