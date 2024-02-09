from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()

client = MongoClient(os.environ.get("MongoConnection"))
db = client['AirbnbAssistant']
Users = db['Users']  


def reset_conversation(id_):
    Users.update_one({"_id":int(id_)},{"$set":{"conversation":[{"role": "system","content": "you are help full assistant. you assist our customers by answering questions about our property we have on airbnb. you only assist users with only our property and business realted question. call wrong_prompt when user prompt is not related to our service and business."}]}})

def register(id_,first_name,username):
    existance = Users.find_one({"_id":int(id_)})
    if existance == None:
        Users.insert_one({"_id":id_,"firstName":first_name,"userName":username,"email":"","personalName":"","conversation":[]})