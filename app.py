from flask import Flask, request, jsonify, render_template
import os
from flask_mail import Mail, Message
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-email', methods=['POST'])
def generate_email():
    data = request.json
    prompt = data.get('prompt')

    try:
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {os.getenv("GROQ_API_KEY")}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'llama-3.3-70b-versatile',  # Use the appropriate model
                'messages': [
                    {
                        'role': 'user',
                        'content': f"Write an email based on the following prompt: {prompt}"
                    }
                ]
            }
        )
        response.raise_for_status()
        generated_email = response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'email': generated_email})

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipients = data.get('recipients').split(',')
    email_content = data.get('emailContent')

    msg = Message('Generated Email', sender=os.getenv('EMAIL_USER'), recipients=recipients)
    msg.body = email_content
    mail.send(msg)

    return jsonify({'message': 'Email sent successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))