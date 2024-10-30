# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port that Uvicorn will run on
EXPOSE 8000

# Command to run the application using Uvicorn
CMD ["python", "-m", "app.main"]
