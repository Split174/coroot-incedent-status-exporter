FROM python:3.9-slim-buster

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker script into the container
COPY ./src/exporter.py .

# Set the command to run the worker script
CMD [ "python", "exporter" ]