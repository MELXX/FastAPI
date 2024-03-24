import json, re
from bson import json_util
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS
from fractions import Fraction

def calculateAlcoholSaturation(id: str):
    alcoholic_items_abv = {
        "Light rum": 40,  # Estimated ABV for light rum: 40%
        "Applejack": 40,  # Estimated ABV for applejack: 40%
        "Gin": 40,  # Estimated ABV for gin: 40%
        "Dark rum": 40,  # Estimated ABV for dark rum: 40%
        "Sweet Vermouth": 15,  # Estimated ABV for sweet vermouth: 15%
        "Strawberry schnapps": 20,  # Estimated ABV for strawberry schnapps: 20%
        "Scotch": 40,  # Estimated ABV for scotch: 40%
        "Apricot brandy": 25,  # Estimated ABV for apricot brandy: 25%
        "Triple sec": 30,  # Estimated ABV for triple sec: 30%
        "Southern Comfort": 35,  # Estimated ABV for Southern Comfort: 35%
        "Brandy": 35,  # Estimated ABV for brandy: 35%
        "Lemon vodka": 40,  # Estimated ABV for lemon vodka: 40%
        "Blended whiskey": 40,  # Estimated ABV for blended whiskey: 40%
        "Dry Vermouth": 15,  # Estimated ABV for dry vermouth: 15%
        "Amaretto": 28,  # Estimated ABV for amaretto: 28%
        "Tequila": 40,  # Estimated ABV for tequila: 40%
        "Vodka": 40,  # Estimated ABV for vodka: 40%
        "Añejo rum": 40,  # Estimated ABV for añejo rum: 40%
        "Kahlua": 20,  # Estimated ABV for Kahlua: 20%
        "Dubonnet Rouge": 15,  # Estimated ABV for Dubonnet Rouge: 15%
        "Irish whiskey": 40,  # Estimated ABV for Irish whiskey: 40%
        "Cherry brandy": 25,  # Estimated ABV for cherry brandy: 25%
        "Port": 20,  # Estimated ABV for port: 20%
        "Red wine": 12,  # Estimated ABV for red wine: 12%
        "Rum": 40,  # Estimated ABV for rum: 40%
        "Sloe gin": 25,  # Estimated ABV for sloe gin: 25%
        "Lemon juice": 0,  # Lemon juice has negligible alcohol content
        "Coffee liqueur": 20,  # Estimated ABV for coffee liqueur: 20%
        "Pineapple juice": 0,  # Pineapple juice has negligible alcohol content
        "Grapefruit juice": 0,  # Grapefruit juice has negligible alcohol content
        "Cranberry juice": 0,  # Cranberry juice has negligible alcohol content
        "Orange": 0,  # Oranges have negligible alcohol content
        "Cranberries": 0,  # Cranberries have negligible alcohol content
        "Apple cider": 5,  # Estimated ABV for apple cider: 5%
        "Everclear": 95,  # Estimated ABV for Everclear: 95%
        "Firewater": 50,  # Estimated ABV for firewater: 50%
        "Lemonade": 0,  # Lemonade has negligible alcohol content
        "Lager": 4,  # Estimated ABV for lager: 4%
        "Whiskey": 40,  # Estimated ABV for whiskey: 40%
        "Irish cream": 17,  # Estimated ABV for Irish cream: 17%
        "Ale": 5,  # Estimated ABV for ale: 5%
        "Pisco": 40,  # Estimated ABV for pisco: 40%
        "Cider": 5,  # Estimated ABV for cider: 5%
        "Blackberry brandy": 25,  # Estimated ABV for blackberry brandy: 25%
        "Peppermint schnapps": 50,  # Estimated ABV for peppermint schnapps: 50%
    }
    return alcoholic_items_abv[id]


def jsonConvert(data):
    return json.loads(json_util.dumps(data))


def getMeasurement(strMeasurement: str) -> str:
    if re.match(r"\b\d+(\.\d+)?\s*oz\b", strMeasurement) is not None:
        return "oz"
    elif re.match(r"\b\d+(\.\d+)?\s*ml\b", strMeasurement) is not None:
        return "ml"
    elif re.match(r"\b\d+(\.\d+)?\s*cup\b", strMeasurement) is not None:
        return "cup"
    elif re.match(r"\b\d+(\.\d+)?\s*cl\b", strMeasurement) is not None:
        return "cl"
    else:
        return "oz"


def strCleaner(s: str,len:int = 2):
    s = s.lstrip()
    s = s.strip()
    s = s[:-len]
    return float(sum(Fraction(s) for s in s.split()))

def process_drinks_json(json_data):
    # Load JSON data
    data = json.loads(json_data)
    
    # Extract drinks list
    drinks = data.get('drinks', [])
    
    # Initialize an empty dictionary to store ingredient-measure pairs
    ingredient_measure_dict = {}
    
    # Iterate through drinks
    for drink in drinks:
        # Iterate through ingredient-measure pairs
        for i in range(1, 16):
            ingredient_key = drink.get(f'strIngredient{i}')
            measure_value = drink.get(f'strMeasure{i}')
            
            # If ingredient is not None and measure is not None, add to dictionary
            if ingredient_key and measure_value:
                ingredient_measure_dict[ingredient_key] = strCleaner(measure_value,len(getMeasurement(measure_value)))
    
    return ingredient_measure_dict

# Example JSON data
json_data = '''
{
    "drinks": [
        {
            "strIngredient1": "Tequila",
            "strIngredient2": "Triple sec",
            "strIngredient3": "Lime juice",
            "strIngredient4": "Salt",
            "strIngredient5": null,
            "strIngredient6": null,
            "strIngredient7": null,
            "strIngredient8": null,
            "strIngredient9": null,
            "strIngredient10": null,
            "strIngredient11": null,
            "strIngredient12": null,
            "strIngredient13": null,
            "strIngredient14": null,
            "strIngredient15": null,
            "strMeasure1": "1 1/2 oz ",
            "strMeasure2": "1/2 oz ",
            "strMeasure3": "1 cup ",
            "strMeasure4": null,
            "strMeasure5": null,
            "strMeasure6": null,
            "strMeasure7": null,
            "strMeasure8": null,
            "strMeasure9": null,
            "strMeasure10": null,
            "strMeasure11": null,
            "strMeasure12": null,
            "strMeasure13": null,
            "strMeasure14": null,
            "strMeasure15": null
        }
    ]
}
'''

# Process JSON data
result = process_drinks_json(json_data)

# Print the result
print(result)