from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import traceback
from groq import Groq

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Replace with your actual API key
YOUR_API_KEY = "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"

@app.route('/')
def index():
    # Read the HTML file
    try:
        with open('chatbot.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return render_template_string(html_content)
    except FileNotFoundError:
        return "chatbot.html not found. Please ensure the file exists in the same directory.", 404

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Log the incoming request
        print("=" * 50)
        print("Received request")
        print(f"Request method: {request.method}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request data (raw): {request.get_data()}")
        
        # Get message from request
        data = request.get_json()
        print(f"Parsed JSON data: {data}")
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({'error': 'No data provided'}), 400
        
        user_message = data.get('message', '')
        print(f"User message extracted: '{user_message}'")
        
        if not user_message:
            print("ERROR: Empty message")
            return jsonify({'error': 'No message provided'}), 400
        
        # Initialize Groq client
        print("Initializing Groq client...")
        client = Groq(api_key=YOUR_API_KEY)

        # Make API call
        print(f"Sending to Groq API: '{user_message}'")
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False
        )

        answer = completion.choices[0].message.content
        print(f"Groq API response: '{answer}'")
        print("=" * 50)
        
        if answer:
            return jsonify({'response': answer})
        else:
            print("ERROR: Empty response from Groq API")
            return jsonify({'error': 'No response from API'}), 500
            
    except Exception as e:
        print("=" * 50)
        print(f"ERROR occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print("Full traceback:")
        traceback.print_exc()
        print("=" * 50)
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    print("=" * 50)
    print(f"Starting Flask server on port {port}")
    print("Make sure chatbot.html is in the same directory")
    print("=" * 50)
    app.run(debug=False, host='0.0.0.0', port=port)
