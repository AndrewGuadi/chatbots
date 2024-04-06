from gpt_helpers import OpenAIHelper
import json


# existing setup
with open('data/openai_apikey.txt' , 'r', encoding='utf-8') as file:
    api_key = file.read()

intent = f"You take text and help convert it to a python array for use in backend code."
bot = OpenAIHelper(api_key=api_key, intent_message=intent)


def running_order(order, text, menu):
    prompt = "Please take the text based order and convert it to our desired array"
    data = f"[Standing Order]: {order}\n[Added Text]: {text}\n[menu]:{menu}"
    example = '''{"order":[
                "item_name_as_key":{
                    "price": float,
                    "toppings": [array of topping strings],
                },
                "item_name_as_key":{
                    "price": float,
                    "toppings": [array of topping strings],
                },
            ]'''
    result = bot.gpt_json(prompt=prompt, data=data, example=example)
    try:
        order = json.loads(result)
        return order
    except:
        print('Unable to convert gpt output to json')
        order = None
        return order
    


def total_order(order):
    print(order)
    order = order.get('order')
    total = float()
    for item in order:
        for key in item:
            print(key)
            price = item[key].get('price')
            if price:
                total += price

    return total


def get_receipt(order):

    receipt = ""
    order = order.get('order')
    for item in order:
        for key in item:
            receipt += f"{key} @ {item[key].get('price')}\n"
        
    return receipt

if __name__=="__main__":

    text = input('Order:  ')
    order = running_order(None, text)
    print(order)





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