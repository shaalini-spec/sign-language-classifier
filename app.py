import os
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image
from transformers import pipeline
from groq import Groq

app = Flask(__name__)

# --- 1. ML/DL Model Setup (Inference Engine via Hugging Face Transformers) ---
print("Loading ASL Classification Model...")
try:
    # Vision Transformer finetuned for Sign Language (ASL alphabet)
    classifier = pipeline("image-classification", model="dima806/image_classification_sign_language")
except Exception as e:
    print(f"Warning: Failed to load specific model. Using fallback. Error: {e}")
    classifier = pipeline("image-classification", model="microsoft/resnet-50")
print("ML Model Loaded successfully.")


# --- 2. GenAI / Agentic AI Setup (Groq Inference Engine) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if GROQ_API_KEY:
    groq_client = Groq(api_key=GROQ_API_KEY)
else:
    print("WARNING: GROQ_API_KEY environment variable not set. LLM features will be simulated.")
    groq_client = None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Read and classify the image
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")

        # 1. Run ML Inference
        predictions = classifier(image)
        top_prediction = predictions[0]
        sign_label = top_prediction['label'].upper()
        confidence = top_prediction['score']

        # 2. Agentic AI via Groq
        llm_report = ""
        if groq_client:
            prompt = f"""You are an educational AI helping someone learn American Sign Language (ASL).
Our computer vision model has detected that the user signed the letter/word: '{sign_label}'.

Please provide:
1. A brief, warm congratulatory message (1 sentence).
2. Two simple, conversational English sentences that start with or prominently feature the letter/word '{sign_label}', to help the user build vocabulary and context.

Format your response in Markdown. Keep it encouraging and concise."""

            try:
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                )
                llm_report = chat_completion.choices[0].message.content
            except Exception as e:
                llm_report = f"Error generating report with Groq: {str(e)}"
        else:
            # Simulated response when no API key is provided
            llm_report = (
                f"**Simulation Mode (No API Key):**\n\n"
                f"Great job! You signed the letter **{sign_label}**.\n\n"
                f"- **{sign_label}** is for Apple. An apple a day keeps the doctor away.\n"
                f"- Are you ready to learn the next letter?\n\n"
                f"*(Set GROQ_API_KEY to see real AI-generated reports.)*"
            )

        return jsonify({
            'sign': sign_label,
            'confidence': f"{confidence:.2%}",
            'ai_context': llm_report
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

