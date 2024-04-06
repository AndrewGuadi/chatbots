from flask import Flask
from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape

from menu import take_order
import json
from menu import menu
from gpt_helpers import OpenAIHelper


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Set a secret key for CSRF token
csrf = CSRFProtect(app)


menu_string = json.dumps(menu)
# existing setup
with open('data/openai_apikey.txt' , 'r', encoding='utf-8') as file:
    api_key = file.read()

with open('data/rules.txt', 'r', encoding='utf-8') as file:
    rules = file.read()

intent = f"Take orders as a restaurant customer service worker would. You are most optimal, accurate and kind to the guest. This is our menu: {menu_string}.\nRules for the job: {rules}"
bot = OpenAIHelper(api_key=api_key, intent_message=intent)


@app.route('/')
def index():

    # Renders the HTML page
    return render_template('menu.html')


@app.route('/message', methods=['POST'])
def handle_message():

    user_input = request.json['message']
    safe_input = escape(user_input)
    print(safe_input)
    # iteration_counter = request.json.get('iteration_counter', 1)
    # iteration_counter += 1

    if user_input.lower() == 'done':
        return jsonify({'response': 'Thank you for your order!', 'done': True})

    response = bot.gpt_3(user_input)
    print(response)
    return jsonify({'response': response, 'done': False})

if __name__ == '__main__':
    app.run(debug=True)