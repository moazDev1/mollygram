# Use the Cypress base image with necessary dependencies for the browser
FROM cypress/browsers:latest

# Install Python and pip if not already available
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    libnss3 \
    libatk-bridge2.0-0 \
    libxss1 \
    libgbm1 \
    libasound2 \
    libappindicator3-1 \
    libatk1.0-0 \
    libnspr4 \
    && apt-get clean

# Ensure pip is up-to-date
RUN python3 -m pip install --upgrade pip

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from the requirements.txt
RUN pip3 install -r requirements.txt

# Set permissions for chromedriver
RUN chmod +x /root/.wdm/drivers/chromedriver/linux64/114.0.5735/chromedriver

# Copy the rest of the application code into the container
COPY . .

# Set environment variable for PATH (where pip installs executables)
ENV PATH /home/root/.local/bin:${PATH}

# Expose the application port (this is the default Railway port)
EXPOSE $PORT

# Command to start the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
