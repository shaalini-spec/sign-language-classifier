# Sign Language Classifier (SDG 4: Quality Education)

An AI-powered web application that helps users learn and practice American Sign Language (ASL) by translating hand gesture images into text and providing educational conversational context. This project aligns with **UN SDG 4: Quality Education** by promoting accessibility and inclusive learning.

## Tech Stack

| Layer | Technology |
|---|---|
| ML/DL Model | Hugging Face Transformers (`dima806/image_classification_sign_language`) |
| LLM / Agentic AI | **Groq Inference Engine** (`llama-3.1-8b-instant`) |
| Model Serving | Flask REST API |
| Containerization | Docker |
| Version Control | Git & GitHub |

## Features
- **Computer Vision (ML/DL):** Pre-trained Vision Transformer model on Hugging Face detects ASL alphabet signs from uploaded images.
- **Agentic AI (Groq):** After detecting a sign, the app sends a prompt to the **Groq API** (using the ultra-fast `llama-3.1-8b-instant` model) to generate encouraging, educational context sentences.
- **REST API:** Flask serves both the frontend and the `/predict` endpoint.
- **Containerization:** Fully containerized using Docker. Image available at `docker.io/shaalinic/sign-language-classifier`.

## Prerequisites
- Python 3.9+ (if running locally without Docker)
- Docker installed
- A [Groq API Key](https://console.groq.com/)

## Local Setup (Without Docker)

```bash
# 1. Create and activate a virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your Groq API Key
export GROQ_API_KEY="your_groq_api_key_here"

# 4. Run the app
python app.py
```

Open `http://localhost:5000` in your browser.

## Docker Setup & Deployment

```bash
# 1. Make the deployment script executable
chmod +x deploy.sh

# 2. Set your Groq API key
export GROQ_API_KEY="your_groq_api_key_here"

# 3. Run the deployment script (builds, optionally runs & pushes to DockerHub)
./deploy.sh
```

Or run manually with Docker:
```bash
docker build -t shaalinic/sign-language-classifier .
docker run -p 5000:5000 -e GROQ_API_KEY=$GROQ_API_KEY shaalinic/sign-language-classifier
```

## GitHub & DockerHub

- **GitHub:** https://github.com/shaalini-spec/sign-language-classifier
- **DockerHub:** https://hub.docker.com/r/shaalinic/sign-language-classifier

## SDG Alignment

This project supports **SDG 4: Quality Education** by making ASL education accessible and interactive through AI, helping bridge the communication gap for the hearing-impaired community.

