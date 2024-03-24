import json

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
                ingredient_measure_dict[ingredient_key] = measure_value
    
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
            "strMeasure3": "1 oz ",
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
