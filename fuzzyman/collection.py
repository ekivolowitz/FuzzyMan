import json
from fuzzyman.request import RequestEncoder 

class Collection():
    def __init__(self, name: str="Collection Name", description: str="Description"):
        self.name = name
        self.description = description
        self.item = []
    
    def _get_representation():
        return {
            "collection" : {
                "info" : {
                    "name" : self.name,
                    "description" : self.description,
                    "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
                },
                "item" : self.item
            }
        }

    def __str__(self):
        representation = {
            "collection" : {
                "info" : {
                    "name" : self.name,
                    "description" : self.description,
                    "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
                },
                "item" : self.item
            }
        }

        return json.dumps(representation, indent=4, cls=RequestEncoder)
