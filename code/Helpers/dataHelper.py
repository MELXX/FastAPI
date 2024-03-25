import json, re
from bson import json_util
from bson.json_util import dumps, CANONICAL_JSON_OPTIONS
from fractions import Fraction
from collections import defaultdict
from datetime import datetime, timedelta


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
    item = alcoholic_items_abv.get(id)
    if item:
        return item / 100
    else:
        return 0


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


def strCleaner(s: str, len: int = 2):
    s = s.lstrip()
    s = s.strip()
    s = s[:-len]
    return float(sum(Fraction(s) for s in s.split()))


def convert_to_ml(amount, unit):
    """
    Converts volume measurements to milliliters.

    Args:
    - amount (float): The amount of the volume to convert.
    - unit (str): The unit of the volume to convert. Should be one of: "oz", "cl", or "cup".

    Returns:
    - float: The converted volume in milliliters.
    """

    if unit == "oz":
        return amount * 29.5735
    elif unit == "cl":
        return amount * 10
    elif unit == "cup":
        return amount * 236.588
    else:
        return "Invalid unit. Please use 'oz', 'cl', or 'cup'."


def process_drinks_json(json_data):
    # Load JSON data
    totalAlcMl = 0
    data = json_data

    # Extract drinks list
    drinks = data.get("drinks", [])

    # Iterate through drinks
    for drink in drinks:
        # Iterate through ingredient-measure pairs
        for i in range(1, 16):
            ingredient_key = drink.get(f"strIngredient{i}")
            measure_value = drink.get(f"strMeasure{i}")

            # If ingredient is not None and measure is not None, add to dictionary
            alc = calculateAlcoholSaturation(ingredient_key)
            if ingredient_key and measure_value and alc:
                # ingredient_measure_dict[ingredient_key] = convert_to_ml(strCleaner(measure_value,len(getMeasurement(measure_value))),getMeasurement(measure_value))*alc
                totalAlcMl += (
                    convert_to_ml(
                        strCleaner(measure_value, len(getMeasurement(measure_value))),
                        getMeasurement(measure_value),
                    )
                    * alc
                )

    return totalAlcMl



def create_user_summary(drink_entries):
    """
    Creates a summary for each user containing their last drink, last drink time,
    and alcohol saturation, considering only entries from the last 8 hours.

    Args:
    - drink_entries (list): A list of dictionaries representing drink entries.

    Returns:
    - list: A list of dictionaries containing the user summary objects.
    """

    user_summary = defaultdict(lambda: {"userId": "", "lastDrink": "", "lastDrinkTime": "", "alcoholSaturation": 0})

    # Calculate the timestamp 8 hours ago
    eight_hours_ago = datetime.utcnow() - timedelta(hours=8)

    # Iterate through drink entries to calculate alcohol saturation for each user
    for entry in drink_entries:
        purchase_time = datetime.strptime(entry["purchaseTime"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ")

        # Skip entries older than 8 hours
        if purchase_time < eight_hours_ago:
            continue

        user_id = entry["userId"]
        drink_name = entry["drinkName"]
        alcohol_amount = entry["AlcoholAmount"]

        # Update user summary
        user_summary[user_id]["userId"] = user_id
        user_summary[user_id]["lastDrink"] = drink_name
        user_summary[user_id]["lastDrinkTime"] = purchase_time.time()

        # Calculate alcohol saturation
        user_summary[user_id]["alcoholSaturation"] += alcohol_amount

    # Convert datetime to ISO 8601 format
    for user_id, summary in user_summary.items():
        summary["lastDrinkTime"] = summary["lastDrinkTime"].isoformat()

    return list(user_summary.values())
