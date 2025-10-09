# Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /noshirt

# Install system dependencies and security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /noshirt/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --pre -r requirements.txt

COPY ./main ./main

ENV PYTHONPATH=/noshirt/main

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "main/prod/app.py"]