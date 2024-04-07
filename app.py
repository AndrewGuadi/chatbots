from flask import Flask
from flask import Flask, render_template, request, jsonify, session
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape

from order_helpers import running_order, total_order, get_receipt
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

    if not session.get('current_order'):
        ## Set the session order
        session['current_order'] = []

    return render_template('menu.html')


@app.route('/message', methods=['POST'])
def handle_message():

    user_input = request.json['message']
    safe_input = escape(user_input)

    if user_input.lower() == 'done':

        #query gpt to get a finalized order to feed to running_order
        query = "Can you read back my entire order to me please?"
        response = bot.gpt_3(query)
        order = running_order(session.get('current_order'), response, menu)
        total = total_order(order)
        print(total)
        receipt = get_receipt(order)
        print(receipt)
        return jsonify({'response': f'Thank you for your order!\n{receipt}\n\nYour total is: {total}', 'done': True})

    response = bot.gpt_3(user_input)
    return jsonify({'response': response, 'done': False})

if __name__ == '__main__':
    app.run(debug=True)