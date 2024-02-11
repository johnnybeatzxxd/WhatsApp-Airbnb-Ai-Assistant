from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

client = MongoClient(os.environ.get("MongoConnection"))
db = client['AirbnbAssistant']
Users = db['Users']  

instruction = {"role": "system","content": "you are help full assistant. you assist our customers by answering questions about our property we have on airbnb. you only assist users with only our property and business realted question. call wrong_prompt when user prompt is not related to our service and business."}

def reset_conversation(_id):
    Users.update_one({"_id":int(_id)},{"$set":{"conversation":[instruction]}})

def register(_id,first_name,username): 
    existance = Users.find_one({"_id":int(_id)})
    if existance == None:
        Users.insert_one({"_id":_id,"firstName":first_name,"userName":username,"email":"","personalName":"","conversation":[instruction]})

def add_message(_id,message):
    conversation = list(Users.find_one({"_id":_id})["conversation"])
    Users.update_one({"_id":int(_id)},{"$set":{"conversation":conversation.append(message)}})

def required_user_info(_id): # returns user Email and Name
    required_info = {}
    email = Users.find_one({"_id":_id}).get("email")
    personalName = Users.find_one({"_id":_id}).get("personalName")
    user_info = {"email":email,"personalName":personalName}
    required_info = []
    if user_info["email"] == "":
        required_info.append("email")
    if user_info["personalName"] == "":
        required_info.append("personalName")
    return required_info

def set_user_info(_id,info):
    Users.update_one({"_id":int(_id)},{"$set":info})

    