import json
import random
from . import database
from . import airbnb
import datetime
import time
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get('OpenAiKey')

today = datetime.date.today()
year = today.year
month = today.month
day = today.day

responseType = 'text'  
imgs = []
random_imgs =[]   



function_descriptions = [
        {
            "name": "save_user_information",
            "description": "This function must be triggerd when customer provide their email and name. if the user provide one of them it should be saved instantly",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "save the name of the customer eg. anuar,yishak ...",
                    },
                    "email": {
                        "type": "string",
                        "description": "save the email of the customer eg. anuar@...,yishak@...",
                        },

                },
                "required": [],
            }
            },
        {
            "name": "off_topic",
            "description": "this function must be triggered when user prompt is not related to our service and business. eg. 'how to install requerments of script thats in text file','how to be good sells man?','how is a car made','how to cook a piza','whats inside car engine','What has a mouth but never speaks?'",
            "parameters": {
                "type": "object",
                "properties": {
                    "off topic": {
                        "type": "string",
                        "description": "true or false",
                    }

                },
                "required": ["question didnt relate"],
            }
            },
            
        {
            "name": "include_image",
            "description": "this function must be triggered when you always talk about specific thing in our property. like about the kitchen bathroom bedroom...",
            "parameters": {
                "type": "object",
                "properties": {
                    "image_of": {
                        "type": "string",
                        "description": "the image to send with your responses. It must be one of the following: [outdoor,house,bedroom,bathroom]. Otherwise, say i dont have an image, because the app will crash. choose one of them that matches with user question.",
                    }

                },
                "required": ["image_of"],
            }
            },
        
        
        
        {
            "name": "get_property_info",
            "description": "you will get the answer of any question about our property.",
            "parameters": {
                "type": "object",
                "properties": {
                    "information needed": {
                        "type": "string",
                        "description": "The type of information requested. It must be one of the following: [title,description,price,availability,bedroom,location,rules,Safety & property]. Otherwise, the app will crash.",
                    },               

                },
                "required": ['information needed']
            }
            },
            {
            "name": "get_aminities_info",
            "description": "This function returns the information about a specific amenity. use ['All amenities'] to get all the amenities details at once.",
            "parameters": {
                "type": "object",
                "properties": {
                    "aminities": {
                        "type": "string",
                        "description": 'The name of the amenity. It must be one of the following: ["Bathroom", "Bedroom and laundry", "Essentials", "Entertainment", "Family", "Heating and cooling", "Home safety", "Internet and office", "Kitchen and dining", "Location features", "Outdoor", "Parking and facilities", "Services", "Not included","All amenities"]. Otherwise, the app will crash. Use "All amenities" to get all the amenities.',
                    }
                    

                },
                "required": ['amenity']
            }
            }      
] 

def image_randomizer(imgs):

    def pick_random_numbers(list_of_numbers, number_of_numbers_to_pick):
        random_numbers = []
        picked_numbers = set()
        for _ in range(number_of_numbers_to_pick):
          while True:
            random_number = random.randint(0, len(list_of_numbers) - 1)
            if random_number not in picked_numbers:
              break
          picked_numbers.add(random_number)
          random_numbers.append(list_of_numbers[random_number])
        return random_numbers
        
    sequence = []
    n = len(imgs)
    for i in range(n):
      sequence.append(i)

    list_of_numbers = sequence
    number_of_numbers_to_pick = 1
    random_numbers = pick_random_numbers(list_of_numbers, number_of_numbers_to_pick)
    return random_numbers
 
def function_call(response,_id):
    
    function_call = response["choices"][0]["message"]["function_call"]
    function_name = function_call["name"]
    function_args = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])

    with open("properties.json", "r") as f:
            properties = json.load(f)

    if function_name == "save_user_information":
        info = {}
        try:
            name = function_args["name"]
        except:
            info["personalName"] = ""
        try:
            email = function_args["email"]
        except:
            info["email"] = ""
        if name == 'John Doe':
            info["personalName"] = ""

        return database.set_user_info(_id,info)
   
    if function_name == "get_property_info":
        arg = function_args["information needed"]
        
        if arg == "price":

            price = airbnb.get(query="price")
            return f'currency = € {price}'

        if arg == "availability":

            availability = airbnb.get(query="availability")
            return f'1 = available\ndate = {today}\n{availability}'

        try:
            return properties["642919"][arg]
        except:
            return 'Error: the information is in the description.'
        
    if function_name == "get_aminities_info": 
        try:
            aminities = function_args['aminities']
        except:
            aminities = "All amenities"
        if aminities == "All amenities":
            return str(properties['642919']['amenities'])
        else:
            try:
                return str(properties['642919']['amenities'][aminities])
            except:
                return 'Error: amenity not found.'
                
    if function_name == "off_topic":

        return 'you should only assist the user with only our property and business realted question.so dont assist! tell them to google it or somthing.'

    if function_name == "include_image":
        
        global responseType
        global imgs
        global random_imgs

        arg = function_args["image_of"]
        responseType = 'image'
        
        try:

            imgs = properties["642919"]['images'][arg]
            random_imgs = image_randomizer(imgs)
            
            return f'image of {arg} will be sent with your reponses.dont say "I am currently unable to send images." so pretend like you sent the image.'

        except:
            return 'image not found with this argument please use one of them [outdoor,house,bedroom,bathroom] if it doesnt match you can just pass.'

def generate_response(_id,messages,required_user_info,):
    print("generating answer ... ")
    responseType = 'text'
    while True:
        try:
            response = openai.ChatCompletion.create( 
                model="gpt-3.5-turbo-1106",
                messages=messages,
                functions = function_descriptions,
                function_call="auto",
                temperature = 0.9
            )
            break
        except openai.error.RateLimitError:
            print('limit exception...')
            time.sleep(20)
    print(response["choices"][0]["message"])
    while response["choices"][0]["finish_reason"] == "function_call":
        
        function_response = function_call(response,_id)
        #bot.send_chat_action(tg.chat.id, 'typing')
        result = json.dumps(function_response)
        messages.append({
            "role": "function",
            "name": response["choices"][0]["message"]["function_call"]["name"],
            "content": response["choices"][0]["message"]["function_call"]['arguments']
        })
        messages.append({
            "role": "function",
            "name": response["choices"][0]["message"]["function_call"]["name"],
            "content": function_response
        })
        #print(messages)
        while True:
            try:
                response = openai.ChatCompletion.create( 
                    model="gpt-3.5-turbo-1106",
                    messages=messages,
                    functions = function_descriptions,
                    function_call="auto",
                    temperature = 0.9
                )
                break
            except openai.error.RateLimitError:
                print('limit exception...')
                time.sleep(20)
                
           #print(response["choices"][0]["message"])
        print(responseType);
    return response["choices"][0]["message"]["content"]

