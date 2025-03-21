FROM python:3.12-slim

# Install Chrome & dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run script
CMD ["python", "main.py"]
