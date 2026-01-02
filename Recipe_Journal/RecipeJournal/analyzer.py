import requests
from django.conf import settings

def edamam_lookup(ingredient_text):
    url = "https://api.edamam.com/api/nutrition-data"

    params = {
        "app_id": settings.EDAMAM_APP_ID,
        "app_key": settings.EDAMAM_APP_KEY,
        "nutrition-type": "logging",
        "ingr": ingredient_text
    }

    response = requests.get(url, params=params)

    data = response.json()

    return {
        "calories": data.get("calories", 0),
        "protein": data["totalNutrients"].get("PROCNT", {}).get("quantity", 0),
        "carbs": data["totalNutrients"].get("CHOCDF", {}).get("quantity", 0),
        "fat": data["totalNutrients"].get("FAT", {}).get("quantity", 0),
        "fiber": data["totalNutrients"].get("FIBTG", {}).get("quantity", 0),
        "dietLabels": data.get("dietLabels", []),
        "healthLabels": data.get("healthLabels", []),
    }

from .models import RecipeIngredient

def analyze_recipe(ingredients):
    totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0}
    all_diets = set()
    all_health = set()

    for ing in ingredients:

        label = f"{ing.quantity or ''} {ing.ingredient.name}"

        data = edamam_lookup(label)

        totals["calories"] += data["calories"]
        totals["protein"] += data["protein"]
        totals["carbs"] += data["carbs"]
        totals["fat"] += data["fat"]
        totals["fiber"] += data["fiber"]

        all_diets.update(data["dietLabels"])
        all_health.update(data["healthLabels"])

    return totals, list(all_diets), list(all_health)
