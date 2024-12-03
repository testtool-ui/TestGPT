from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Hugging Face Inference API
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HEADERS = {"Authorization": "Bearer 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"}  # Replace with your Hugging Face API key

def query_huggingface(payload):
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    try:
        return response.json()
    except ValueError:
        return {"error": "Invalid response from the model."}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")  # Get user input
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    payload = {"inputs": user_message}
    response = query_huggingface(payload)

    if "error" in response:
        chatbot_reply = response["error"]
    else:
        chatbot_reply = response[0]["generated_text"] if isinstance(response, list) else "Sorry, no response generated."

    return jsonify({"reply": chatbot_reply})

if __name__ == "__main__":
    app.run(debug=True)