from collections import defaultdict
from datetime import datetime, timedelta

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
        user_summary[user_id]["lastDrinkTime"] = purchase_time

        # Calculate alcohol saturation
        user_summary[user_id]["alcoholSaturation"] += alcohol_amount

    # Convert datetime to ISO 8601 format
    for user_id, summary in user_summary.items():
        summary["lastDrinkTime"] = summary["lastDrinkTime"].isoformat()

    return list(user_summary.values())



# Example usage:
drink_entries = [
  {
    "_id": {
      "$oid": "6600bc4e8e35f84426b39046"
    },
    "drinkId": "13196",
    "userId": "9809215068087",
    "drinkName": "Long vodka",
    "AlcoholAmount": 20,
    "purchaseTime": {
      "$date": "2024-03-25T01:50:38.832Z"
    }
  },
  {
    "_id": {
      "$oid": "6600bc528e35f84426b39049"
    },
    "drinkId": "11002",
    "userId": "9809215068087",
    "drinkName": "Long Island Tea",
    "AlcoholAmount": 23.6588,
    "purchaseTime": {
      "$date": "2024-03-25T01:50:42.986Z"
    }
  },
  {
    "_id": {
      "$oid": "6600bc568e35f84426b3904c"
    },
    "drinkId": "17831",
    "userId": "9809215068086",
    "drinkName": "A Furlong Too Late",
    "AlcoholAmount": 23.6588,
    "purchaseTime": {
      "$date": "2024-03-25T01:50:46.858Z"
    }
  },
  {
    "_id": {
      "$oid": "6600bc5b8e35f84426b3904f"
    },
    "drinkId": "17204",
    "userId": "9809215068086",
    "drinkName": "Long Island Iced Tea",
    "AlcoholAmount": 23.6588,
    "purchaseTime": {
      "$date": "2024-03-25T01:50:51.147Z"
    }
  },
  {
    "_id": {
      "$oid": "6600bc608e35f84426b39052"
    },
    "drinkId": "16984",
    "userId": "9809215068086",
    "drinkName": "Radioactive Long Island Iced Tea",
    "AlcoholAmount": 56.18965,
    "purchaseTime": {
      "$date": "2024-03-25T01:50:56.905Z"
    }
  }
]

user_summary = create_user_summary(drink_entries)
print(user_summary)
