# Use official Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy all files to /app
COPY . .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Expose the port the app runs on
EXPOSE 5000
# Run the application
CMD ["python", "app.py"]