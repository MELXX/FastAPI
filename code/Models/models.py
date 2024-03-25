from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    id: str
    height: float
    weight: float

class UserDTO(BaseModel):
    id: str
    lastDrink:str
    lastDrinkTime:datetime
    alcoholSaturation:float = 0

class UserDrink(BaseModel):
    drinkId: str
    userId:str
    drinkName:str = ' '#strDrink
    AlcoholAmount:str = ' ' #strMeasure1
    purchaseTime: datetime = datetime.now()

class UserDrinkDTO(BaseModel):
    drinkId: str
    userId:str
    drinkName:str #strDrink
    AlcoholType:str #usually str strIngredient1
    AlcoholAmount:str #strMeasure1
