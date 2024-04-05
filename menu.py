from gpt_helpers import OpenAIHelper
import os
import json
from menufile import menu




def take_order():
    iteration_counter = 1
    while True:

        
        if iteration_counter == 1:
            user_response = input('Welcome to 5 Guys where we are having the most wonderful of days. What can I get started for you?:  ')
        else:
            user_response = input('') 
        
        if user_response:
            if user_response.strip().lower() == 'done':
                break
            response = bot.gpt_3(user_response, iteration_counter)
            print(response)
        else: 
            print("I'm sorry, I didn't catch that.")
    
        iteration_counter += 1

    return False

if __name__=="__main__":

    pass