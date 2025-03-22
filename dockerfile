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
ARG CHROME_DRIVER_VERSION=114.0.5735.90
RUN wget "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/chromedriver

# Copy your application files (if applicable)
COPY . /app

# Install Python dependencies (if applicable)
RUN pip install --no-cache-dir selenium

# Your Python script (example)
COPY main.py /app/main.py

# Run your Python script
CMD ["python", "main.py"]