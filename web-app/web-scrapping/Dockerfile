# Use a lightweight Python image as the base
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the necessary files into the container
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install cron in the container
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Create the cron job directly in the Dockerfile
RUN echo "* * * * * /usr/local/bin/python3 /app/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/my-cron-job

# Set the correct permissions for the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply the cron job
RUN crontab /etc/cron.d/my-cron-job

# Create a log file for cron logs
RUN touch /var/log/cron.log

# Start cron and keep the container running
CMD ["/bin/bash", "-c", "cron && tail -f /var/log/cron.log"]






