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
    AlcoholType:str = ' ' #usually str strIngredient1
    AlcoholAmount:str = ' ' #strMeasure1
    purchaseTime: datetime = datetime.now()
    def toJSON(self,json):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class UserDrinkDTO(BaseModel):
    drinkId: str
    userId:str
    drinkName:str #strDrink
    AlcoholType:str #usually str strIngredient1
    AlcoholAmount:str #strMeasure1
