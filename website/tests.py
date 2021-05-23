import requests
import json
from .recipe import Recipe

def create_recipe_objects(reply):
    info = reply.json()

    all_recipes = []

    for item in info["data"]:
        recipe = Recipe(item["id"], item["name"], item["description"])
        all_recipes.append(recipe)

    return all_recipes





