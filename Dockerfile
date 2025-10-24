# Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /noshirt

# Install system dependencies and security updates
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ libpq-dev \
    python3-dev libxml2-dev libxslt1-dev libssl-dev gfortran && \
    rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /noshirt/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir psycopg[binary]==3.2.1 && \
    pip install --no-cache-dir -r requirements.txt

COPY ./main ./main

ENV PYTHONPATH=/noshirt/main

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "main/prod/app.py"]