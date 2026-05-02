#!/bin/bash

# Exit on any error
set -e

echo "=== Sign Language Classifier Deployment Script ==="

# Default DockerHub username
DOCKER_USERNAME="${DOCKER_USERNAME:-shaalinic}"
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
    docker run -d -p 5000:5000 -e GROQ_API_KEY=$GROQ_API_KEY --name $IMAGE_NAME $FULL_IMAGE_NAME
    echo "Container is running at http://localhost:5000"
fi

# Ask user if they want to push to DockerHub
read -p "Do you want to push the image to DockerHub? (y/n): " push_docker
if [ "$push_docker" == "y" ]; then
    echo "Logging into DockerHub..."
    docker login -u $DOCKER_USERNAME
    echo "[3/3] Pushing Image to DockerHub..."
    docker push $FULL_IMAGE_NAME
    echo "Successfully pushed to: https://hub.docker.com/r/$FULL_IMAGE_NAME"
else
    echo "Skipping push to DockerHub."
fi

echo "Done!"
