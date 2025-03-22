FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    libgconf-2-4 \
    --no-install-recommends

# Set the working directory
WORKDIR /app

# Download and install ChromeDriver (adjust version as needed)
ARG CHROME_DRIVER_VERSION=114.0.5735.90 #Ensure this matches chromium version.
RUN wget "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY . /app

# Your Python script (example)
CMD ["python", "main.py"]