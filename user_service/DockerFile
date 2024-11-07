# Use the official Python image as a base
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose the port the service runs on
EXPOSE 5001

# Run the Flask app
CMD ["python", "app.py"]
