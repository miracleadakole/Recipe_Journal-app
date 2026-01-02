import requests
from django.conf import settings  

EDAMAM_BASE_URL = "https://api.edamam.com/api/food-database/v2/parser"

def fetch_ingredient_data(ingredient_name):
    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.EDAMAM_APP_KEY,
        "ingr": ingredient_name,
    }

    response = requests.get(EDAMAM_BASE_URL, params=params)
    response.raise_for_status()

    data = response.json()

    if not data.get("parsed"):
        return None

    food = data["parsed"][0]["food"]

    return {
        "label": food.get("label"),
        "nutrients": food.get("nutrients"),
        "category": food.get("category"),
        "image": food.get("image"),
    }
