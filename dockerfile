# Use a Python base image
FROM python:3.12-slim-bookworm

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    chromium-driver \
    libgconf-2-4

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy your application code
COPY main.py .
COPY telegram_bot.py .

# Set chromedriver path - since we install chromium-driver it will be found in PATH, so no need for specific path.
# Set binary location
ENV CHROMEDRIVER_PATH=/usr/lib/chromium/chromedriver
ENV CHROMIUM_BIN=/usr/bin/chromium

# Run the script
CMD ["python", "main.py"]