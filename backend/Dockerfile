# Use the official Python image from the Docker Hub with version 3.12.4 and Alpine Linux
FROM python:3.12.4-alpine

# Set the working directory in the container to /usr/src/app
WORKDIR /usr/src/app

# Set environment variables

# Ensure that the Python output is sent directly to the terminal (stdout/stderr) without being buffered
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from writing .pyc files (compiled bytecode)
ENV PYTHONUNBUFFERED=1         

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy the requirements.txt file from your local machine to the container
COPY ./requirements.txt /usr/src/app/requirements.txt

# Install the dependencies listed in requirements.txt
RUN pip install -r requirements.txt

# Copy the entrypoint.sh script from your local machine to the container
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# Ensure the entrypoint.sh script is executable
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy the rest of the application code from your local machine to the container
COPY . /usr/src/app/

# Specify the script to run when the container starts
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]