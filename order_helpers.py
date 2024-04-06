from gpt_helpers import OpenAIHelper


# existing setup
with open('data/openai_apikey.txt' , 'r', encoding='utf-8') as file:
    api_key = file.read()

intent = f"You take text and help convert it to json or a python array for use in backend code."
bot = OpenAIHelper(api_key=api_key, intent_message=intent)


def running_order(order, text):
    bot.gpt_3()

def total_order():
    pass





###this file will take the text input and covert it to a running order in json/array for the backend to use


###EXAMPLE
# order = [
#     "item":{
#         "price": float,
#         "toppings": [array of topping strings],
#         "modifiers": [array of string modifiers]
#     },
#     "item":{
#         "price": float,
#         "toppings": [array of topping strings],
#         "modifiers": [array of string modifiers]
#     },
# ]