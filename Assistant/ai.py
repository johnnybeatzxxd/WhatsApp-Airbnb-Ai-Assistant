import json
import database
import airbnb
import datetime


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
