from typing import Union
from bson import ObjectId
from fastapi import FastAPI, HTTPException, status
from Helpers.AppMongoClient import AppMongoClient
from Helpers.apiHelper import apiHelper
from Helpers.dataHelper import *
from Models.models import *
from fastapi.middleware.cors import CORSMiddleware


from Helpers.dataHelper import jsonConvert,calculateAlcoholSaturation, process_drinks_json,strCleaner,create_user_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/getUser/{id}")
def get_user(id: str):

    db = AppMongoClient()
    return jsonConvert(db.getUserById(id))


@app.post("/createUser", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    db = AppMongoClient()
    u = db.getUserById(user.id)
    if u is None:
        returnedId = db.insertUser(user=user)
        return {"id": str(returnedId)}
    else:
        raise HTTPException(status_code=400, detail="User already in system")


@app.post("/serveUser/{id}", status_code=status.HTTP_200_OK)
def serve_user(id: str, userDrink: UserDrink):
    db = AppMongoClient()
    u = db.getUserById(id=id)
    if u is not None:
        returnedId = db.insertUserDrink(uDrink=processDrinkOrder(userDrink))
        return {"id": str(returnedId)}
    else:
        raise HTTPException(status_code=400, detail="User not found in system")


@app.get("/getCurrentPatrons", status_code=status.HTTP_200_OK)
def get_Current_Patrons():
    return create_user_summary(jsonConvert(AppMongoClient().getCurrentPatrons()))

@app.get('/strCleaner')
def strCleaner_test(s:str):
    return strCleaner(s)

def processDrinkOrder(ud:UserDrink):
        res = apiHelper().get_drinkById(ud.drinkId)
        ud.drinkName = res['drinks'][0]['strDrink']
        ud.AlcoholAmount = process_drinks_json(res)
        return ud



