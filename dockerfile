# Use slim Python image
FROM python:3.12-slim

# Install system dependencies for Chrome + Selenium
RUN apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    fonts-liberation \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin/chromium

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project files
COPY . /app
WORKDIR /app

# Run your script
CMD ["python", "main.py"]
