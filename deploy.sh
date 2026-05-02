#!/bin/bash

# Exit on any error
set -e

echo "=== Sign Language Classifier Deployment Script ==="

# Check for DockerHub username
if [ -z "$DOCKER_USERNAME" ]; then
    echo "ERROR: DOCKER_USERNAME environment variable is not set."
    echo "Please set it before running this script: export DOCKER_USERNAME=yourusername"
    exit 1
fi

IMAGE_NAME="sign-language-classifier"
IMAGE_TAG="latest"
FULL_IMAGE_NAME="$DOCKER_USERNAME/$IMAGE_NAME:$IMAGE_TAG"

echo "[1/3] Building Docker Image: $FULL_IMAGE_NAME..."
docker build -t $FULL_IMAGE_NAME .

echo "[2/3] Docker Image Built Successfully."

# Ask user if they want to run it locally
read -p "Do you want to run the container locally now? (y/n): " run_locally
if [ "$run_locally" == "y" ]; then
    echo "Starting container on http://localhost:5000..."
    # Map port 5000 and pass GEMINI_API_KEY if it exists
    docker run -d -p 5000:5000 -e GEMINI_API_KEY=$GEMINI_API_KEY --name $IMAGE_NAME $FULL_IMAGE_NAME
    echo "Container is running in the background."
fi

# Ask user if they want to push to DockerHub
read -p "Do you want to push the image to DockerHub? (y/n): " push_docker
if [ "$push_docker" == "y" ]; then
    echo "Logging into DockerHub (you may be prompted for your password)..."
    docker login -u $DOCKER_USERNAME
    
    echo "[3/3] Pushing Image to DockerHub..."
    docker push $FULL_IMAGE_NAME
    echo "Deployment to DockerHub Complete!"
else
    echo "Skipping push to DockerHub."
fi

echo "Done!"
