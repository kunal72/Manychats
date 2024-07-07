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
    response = openai.Completion.create(engine="davinci",
                                        prompt=prompt,
                                        max_tokens=500)
    return response.choices[0].text.strip()


def store_in_google_sheet(data):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{SHEET_NAME}!A1:append?valueInputOption=USER_ENTERED&key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    body = {"values": [[data["name"], data["email"], data["comments"]]]}
    response = requests.post(url, headers=headers, json=body)
    return response.json()


@app.route('/collect_info', methods=['POST'])
def collect_info():
    data = request.json
    user_message = data['message']['text']

    # Generate dietary plan using GPT-3
    prompt = f"User: {user_message}\nAI: Based on your requirements, here is a personalized dietary plan for you."
    gpt3_response = ask_gpt3(prompt)

    response = {"messages": [{"text": gpt3_response}]}
    return jsonify(response)


@app.route('/collect_contact_info', methods=['POST'])
def collect_contact_info():
    data = request.json
    user_name = data['name']
    user_email = data['email']
    comments = data['comments']

    user_data = {"name": user_name, "email": user_email, "comments": comments}
    store_in_google_sheet(user_data)

    response = {
        "messages": [{
            "text":
            "Thank you! We will reach out to you soon to schedule a meeting. Have a great day!"
        }]
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
