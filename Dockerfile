# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy everything from your repo into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your script
CMD ["python", "rss_to_discord.py"]
