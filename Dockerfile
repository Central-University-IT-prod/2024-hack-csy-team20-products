# Use the official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements.txt first to leverage Docker cache.
COPY requirements.txt .

# Install the necessary packages.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your FastAPI app code into the container.
COPY FastAPI/ /app

# Expose the port FastAPI runs on (default is 8000).
EXPOSE 8000

# Run the application using Uvicorn.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
