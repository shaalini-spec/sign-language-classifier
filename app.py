import os
import io
from flask import Flask, request, jsonify, render_template
from PIL import Image
from transformers import pipeline
import google.generativeai as genai

app = Flask(__name__)

# --- 1. ML/DL Model Setup (Inference Engine) ---
print("Loading ASL Classification Model...")
try:
    # Using a Vision Transformer finetuned for Sign Language (ASL alphabet)
    classifier = pipeline("image-classification", model="dima806/image_classification_sign_language")
except Exception as e:
    print(f"Warning: Failed to load specific model. Using fallback. Error: {e}")
    classifier = pipeline("image-classification", model="microsoft/resnet-50")
print("ML Model Loaded successfully.")


# --- 2. GenAI / Agentic AI Setup ---
# Configure Google Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    llm_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    print("WARNING: GEMINI_API_KEY environment variable not set. LLM features will be simulated.")
    llm_model = None

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
        # Read the image
        img_bytes = file.read()
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        
        # 1. Run ML Inference
        predictions = classifier(image)
        # Get the top prediction
        top_prediction = predictions[0]
        sign_label = top_prediction['label'].upper()
        confidence = top_prediction['score']
        
        # 2. Agentic AI Integration
        llm_report = ""
        if llm_model:
            prompt = f"""
            You are an educational AI helping someone learn American Sign Language (ASL).
            Our computer vision model has detected that the user signed the letter/word: '{sign_label}'.
            
            Please provide:
            1. A very brief congratulatory message.
            2. Two common, conversational English sentences that start with or prominently feature the letter/word '{sign_label}' to help them understand context.
            
            Keep the response encouraging, concise, and format it nicely in Markdown.
            """
            try:
                response = llm_model.generate_content(prompt)
                llm_report = response.text
            except Exception as e:
                llm_report = f"Error generating report with Gemini: {str(e)}"
        else:
            # Simulated Response if no API key is provided
            llm_report = f"**Simulation Mode:**\nGreat job! You signed the letter **{sign_label}**. \n\nHere are some sentences:\n- **{sign_label}** is for Apple. An apple a day keeps the doctor away.\n- Are you ready to learn the next letter? (Set GEMINI_API_KEY to see real AI reports)."
            
        return jsonify({
            'sign': sign_label,
            'confidence': f"{confidence:.2%}",
            'ai_context': llm_report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Containerized apps should run on 0.0.0.0
    app.run(host='0.0.0.0', port=5000, debug=True)
