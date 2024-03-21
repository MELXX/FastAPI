from typing import Union
from bson import ObjectId
from fastapi import FastAPI, HTTPException,status
from Helpers.AppMongoClient import AppMongoClient
from Models.models import *
import json, re
from bson import json_util 
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



@app.get("/getUser/{id}")
def get_user(id: str):

    u = User(name="john",id="9812365263632",height=1.61,weight=150)
    ud = UserDrink(drinkId="111111",userId="9812365263632",purchaseTime=datetime.now())
    return {"user":u,"userDop":ud}

@app.post("/createUser",status_code=status.HTTP_201_CREATED)
def create_user(user:User):
    db = AppMongoClient()
    u=db.getUserById(user.id)
    if u is None:
        returnedId = db.insertUser(user=user)
        return  {"id":str(returnedId)}
    else:
        raise HTTPException(status_code=400, detail="User already in system")

@app.post("/serveUser/{id}",status_code=status.HTTP_200_OK)
def serve_user(id:str,userDrink:UserDrink):
    db = AppMongoClient()
    u = db.getUserById(id=id)
    if u is not None:
        returnedId = db.insertUserDrink(uDrink=userDrink)
        return  {"id":str(returnedId)}
    else:
        raise HTTPException(status_code=400, detail="User not found in system")

@app.get("/getCurrentPatrons",status_code=status.HTTP_200_OK)
def get_Current_Patrons():
    return json.loads(json_util.dumps(AppMongoClient().getCurrentPatrons()))

def calculateAlcoholSaturation(id:str):
    pass


