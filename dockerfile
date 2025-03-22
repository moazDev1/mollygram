# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Install system dependencies for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y wget curl unzip libnss3 libgdk-pixbuf2.0-0 \
    libasound2 libxss1 libappindicator3-1 libatk-bridge2.0-0 libatk1.0-0 \
    libgbm1 libgtk-3-0 ca-certificates

# Install Google Chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Install ChromeDriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /usr/local/bin

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Command to run your app
CMD ["python", "main.py"]