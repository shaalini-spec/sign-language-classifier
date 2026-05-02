# Sign Language Classifier (SDG 4: Quality Education)

An AI-powered web application that helps users learn and practice American Sign Language (ASL) by translating hand gestures into conversational English. This project aligns with **UN SDG 4: Quality Education** by promoting accessibility and inclusive learning.

## Features
- **Computer Vision (ML/DL):** Uses a pre-trained Hugging Face image classification model (`dima806/image_classification_sign_language`) to identify ASL alphabet signs from images.
- **Agentic AI:** Integrates Google's Gemini LLM to generate conversational, educational sentences using the detected sign to build context and vocabulary.
- **REST API:** Built with Flask.
- **Containerization:** Fully containerized using Docker for easy deployment.

## Prerequisites
- Python 3.9+ (if running locally without Docker)
- Docker installed on your machine (for container deployment)
- A DockerHub account
- A Google Gemini API Key (get one at [Google AI Studio](https://aistudio.google.com/))

## Local Setup (Without Docker)

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your API Key:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```
4. Run the Flask app:
   ```bash
   python app.py
   ```
5. Open `http://localhost:5000` in your browser.

## Docker Setup & Deployment

We have provided a script that builds the Docker image, runs it locally, and pushes it to DockerHub.

1. Make the script executable:
   ```bash
   chmod +x deploy.sh
   ```
2. Set your DockerHub username and Gemini API key:
   ```bash
   export DOCKER_USERNAME="your_username"
   export GEMINI_API_KEY="your_gemini_key"
   ```
3. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

## Version Control (Git & GitHub)

This repository is initialized with Git. To push your local code to a new public repository on GitHub:

1. Create a new repository on GitHub (do not initialize with README).
2. Link your local repo and push:
   ```bash
   git remote add origin https://github.com/yourusername/sign-language-classifier.git
   git branch -M main
   git push -u origin main
   ```
