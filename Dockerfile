# Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /noshirt

# Install system dependencies and security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    gcc \
    wget \
    build-essential \
    libffi-dev \
    && wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz \
    && tar -xzf ta-lib-0.4.0-src.tar.gz \
    && cd ta-lib/ \
    && ./configure --prefix=/usr \
    && make \
    && make install \
    && cd .. \
    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz \
    && ldconfig \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /noshirt/
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    TA_LIBRARY_PATH=/usr/lib TA_INCLUDE_PATH=/usr/include pip install --no-cache-dir -r requirements.txt

COPY ./main ./main

ENV PYTHONPATH=/noshirt/main

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "main/prod/app.py"]