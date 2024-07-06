from flask import Flask, request, jsonify
import openai
import requests
import os

app = Flask(__name__)

# Initialize OpenAI GPT-3
openai.api_key = os.getenv('OPENAI_API_KEY')

# Google Sheets setup
API_KEY = os.getenv('API_KEY')  # Your Google API key
SHEET_ID = os.getenv('SHEET_ID')  # Your Google Sheet ID
SHEET_NAME = 'Sheet1'  # Replace with your sheet name if different

def ask_gpt3(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def store_in_google_sheet(data):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}!A1:append?valueInputOption=USER_ENTERED&key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "values": [
            [data["Name"], data["Email"], data["Comments"]]
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    return response.json()

@app.route('/ask_schedule', methods=['POST'])
def ask_schedule():
    data = request.json
    user_message = data['message']['text']
    prompt = f"User: {user_message}\nAI: Could you tell me about your daily schedule?"
    gpt3_response = ask_gpt3(prompt)
    response = {"messages": [{"text": gpt3_response}]}
    return jsonify(response)

@app.route('/ask_training_hours', methods=['POST'])
def ask_training_hours():
    data = request.json
    user_message = data['message']['text']
    prompt = f"User: {user_message}\nAI: How many hours do you spend training each day?"
    gpt3_response = ask_gpt3(prompt)
    response = {"messages": [{"text": gpt3_response}]}
    return jsonify(response)

@app.route('/ask_diet', methods=['POST'])
def ask_diet():
    data = request.json
    user_message = data['message']['text']
    prompt = f"User: {user_message}\nAI: Do you have any dietary preferences or restrictions?"
    gpt3_response = ask_gpt3(prompt)
    response = {"messages": [{"text": gpt3_response}]}
    return jsonify(response)

@app.route('/collect_contact_info', methods=['POST'])
def collect_contact_info():
    data = request.json
    user_name = data['name']
    user_email = data['email']
    comments = data['comments']

    user_data = {
        "Name": user_name,
        "Email": user_email,
        "Comments": comments
    }
    store_in_google_sheet(user_data)

    response = {"messages": [{"text": "Thank you! We will reach out to you soon to schedule a meeting. Have a great day!"}]}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
