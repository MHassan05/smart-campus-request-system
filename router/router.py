# from utils import input_form 
import utils.input_form as input_form
import random 

def generate_request_id():
    request_id = f"REQ{random.randint(1000, 9999)}"
    return request_id 


def route(): 
    # get the data from user 
    user_input = input_form.get_user_input()
    for key, value in user_input.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    route()

