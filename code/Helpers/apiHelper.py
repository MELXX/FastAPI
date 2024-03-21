
import httpx


class apiHelper:
    def __init__(self) -> None:
        pass

    def get_drinkByName(self,name: str):
        req = httpx.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=%s"%(name))
        data = req.json()
        # for drink in data['drinks']:
        #     id_drink = drink['idDrink']
        #     name = drink['strDrink']
        #     ingredient1 = drink['strIngredient1']
        #     print(f"idDrink: {id_drink}, strDrink: {name}, strIngredient1: {ingredient1}")

        parsed = [{
            "id_drink" : drink['idDrink'],
            "name" : drink['strDrink'],
            "ingredient1": drink['strIngredient1']} 
            for drink in data['drinks']]
        
        # for i in parsed:
        #     print(i)
        return parsed

    def getAllAlcoholicDrinks(self):
        req = httpx.get("www.thecocktaildb.com/api/json/v1/1/filter.php?a=Alcoholic")
        data = req.json()
    
print(apiHelper().get_drinks(name="beer"))

