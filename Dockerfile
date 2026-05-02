# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Upgrade pip to prevent hash mismatch errors on large downloads (like numpy)
RUN pip install --upgrade pip

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Step 1: Install CPU-only PyTorch first (much smaller than GPU version ~200MB vs 2GB)
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    torch==2.3.0 --index-url https://download.pytorch.org/whl/cpu

# Step 2: Install remaining dependencies
RUN pip install --no-cache-dir --timeout=300 --retries=5 \
    Flask==3.0.3 \
    Werkzeug==3.0.3 \
    transformers==4.40.1 \
    Pillow==10.3.0 \
    groq==0.9.0 \
    gunicorn==22.0.0

# Copy the current directory contents into the container at /app
COPY . /app/

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Gunicorn
ENV PORT=5000

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "app:app"]
