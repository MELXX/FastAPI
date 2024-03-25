from datetime import datetime
import json
import os
from pymongo import *
from Models.models import User, UserDTO, UserDrink


class AppMongoClient:
    def __init__(self) -> None:
        pass

    def get_database(self):
        # Provide the mongodb atlas url to connect python to mongodb using pymongo
        CONNECTION_STRING = os.getenv('MONGO_URI', "mongodb://localhost:27017/")

        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client["barDb"]

    # This is added so that many files can reuse the function get_database()
    if __name__ == "__main__":
        # Get the database
        dbname = get_database()

    def getCollection(self, id: str = "Users"):
        dbname = self.get_database()
        return dbname[id]

    def insertUser(self, user: User, id: str = "Users"):
        dbname = self.get_database()
        collection_name = dbname[id]
        user = {
            "uid": user.id,
            "name": user.name,
            "height": user.height,
            "weight": user.weight,
        }
        return collection_name.insert_one(user).inserted_id

    def insertUserDrink(self, uDrink: UserDrink, id: str = "UserDrink"):
        dbname = self.get_database()
        collection_name = dbname[id]
        UserDrink = {
            "drinkId": uDrink.drinkId,
            "userId": uDrink.userId,
            "drinkName":uDrink.drinkName,
            "AlcoholAmount":uDrink.AlcoholAmount,
            "purchaseTime": datetime.now(),
        }
        return collection_name.insert_one(UserDrink).inserted_id

    def getUserById(self,id:str)->User:
        users = self.getCollection()
        return users.find_one({"uid": id})

    def getCurrentPatrons(self):
        users = self.getCollection(id="UserDrink")
        d = users.find()
        return d

