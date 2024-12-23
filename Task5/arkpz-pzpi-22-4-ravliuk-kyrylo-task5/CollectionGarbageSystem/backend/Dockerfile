# Use the official Python 3.13 image as the base image
FROM python:3.13

# Ensure the output from Python is unbuffered, helpful for logging
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python dependencies
RUN pip install -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose port 8000 to allow external access to the application
EXPOSE 8000

# Define the script to be executed when the container starts
ENTRYPOINT ["/app/migration.sh"]
