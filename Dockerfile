# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Create the .aws directory
RUN mkdir -p /root/.aws

# Copy the current directory contents into the container at /app
COPY . .

# Copy the .aws directory into the container
COPY /var/lib/jenkins/.aws /root/.aws/

# Create the reports directory
RUN mkdir -p /app/reports

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run generate_report.py when the container launches
CMD ["python", "/app/generate_report.py"]
