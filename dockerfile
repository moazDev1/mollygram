# Use a Python base image
FROM python:3.12-slim-bookworm

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    chromium \
    libgconf-2-4 \
    libnss3 \
    libatk1.0-0 \
    libpango-1.0-0 \
    libasound2 \
    libxshm1

# Get the Chrome version
RUN CHROME_VERSION=$(chromium --version | sed -E 's/Chromium ([0-9]+)\..*/\1/')

# Download chromedriver matching the chrome version.
RUN wget "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" -O chromedriver_version.txt
RUN CHROMEDRIVER_VERSION=$(cat chromedriver_version.txt)
RUN wget "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

# Add debugging steps
RUN ls -l /usr/local/bin/chromedriver
RUN /usr/local/bin/chromedriver --version

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

# Set binary location
ENV CHROMIUM_BIN=/usr/bin/chromium

# Run the script
CMD ["python", "main.py"]