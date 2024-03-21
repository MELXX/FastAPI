from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    name: str
    id: str
    height: float
    weight: float

class UserDTO(BaseModel):
    name: str
    id: str
    height: float
    weight: float
    lastDrink:str
    lastDrinkTime:datetime
    alcoholSaturation:float = 0

class UserDrink(BaseModel):
    drinkId: str
    userId:str
    purchaseTime: datetime = datetime.now()