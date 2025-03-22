FROM python:3.10-slim-buster

# Install necessary packages and libraries for Chrome and chromedriver
RUN apt-get update && apt-get install -y \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libnspr4 \
    libnss3 \
    lsb-release \
    xdg-utils \
    libxss1 \
    libdbus-glib-1-2 \
    curl \
    unzip \
    wget \
    vim \
    xvfb \
    libgbm1 \
    libu2f-udev \
    libvulkan1 \
    && apt-get clean

# Install Google Chrome Stable version
RUN CHROME_SETUP=google-chrome.deb && \
    wget -O $CHROME_SETUP "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i $CHROME_SETUP && \
    apt-get install -y -f && \
    rm $CHROME_SETUP

# Set environment variables for locale and Python
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH="$PATH:/bin:/usr/bin"

# Set working directory
WORKDIR /app

# Copy the application code into the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

# Make the app listen on the port assigned by Railway
CMD ["python3", "main.py"]