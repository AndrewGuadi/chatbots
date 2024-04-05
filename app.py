from flask import Flask
from flask import Flask, render_template, request, jsonify
from menu import take_order
import json
from menu import menu
from gpt_helpers import OpenAIHelper


menu_string = json.dumps(menu)
# existing setup
api_key = ""
intent = f"Take orders as a restaurant customer service worker would. You are most optimal, accurate and kind to the guest. This is our menu: {menu_string}"
bot = OpenAIHelper(api_key=api_key, intent_message=intent)
app = Flask(__name__)

app = Flask(__name__)

@app.route('/')
def index():
    # Renders the HTML page
    return render_template('menu.html')

@app.route('/message', methods=['POST'])
def handle_message():
    user_input = request.json['message']
    iteration_counter = request.json.get('iteration_counter', 1)

    if user_input.lower() == 'done':
        return jsonify({'response': 'Thank you for your order!', 'done': True})

    response = bot.gpt_3(user_input, iteration_counter)
    print(response)
    return jsonify({'response': response, 'done': False})

if __name__ == '__main__':
    app.run(debug=True)