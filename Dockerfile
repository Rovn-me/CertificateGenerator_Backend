# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir reduces image size
# --trusted-host pypi.python.org is sometimes needed in strict network environments
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8030 available to the world outside this container
EXPOSE 8030

# Define environment variable (optional, can be useful)
ENV FLASK_APP=app.py

# Run app.py when the container launches using gunicorn
# Bind to 0.0.0.0 to allow external connections
# Use the port specified in your app (8030)
CMD ["gunicorn", "--bind", "0.0.0.0:8030", "app:app"]
