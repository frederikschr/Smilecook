from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import requests
from website import URL

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    if not "username" in session:
        return redirect(url_for("auth.login"))
    return render_template("home.html", user=session)

@views.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        info = request.form.get("text")
        return redirect(url_for("views.home"))
    return render_template("contact.html",  user=session)

@views.route("/recipes", methods=["GET", "POST"])
def recipes():
    if "email" in session:
        search = None

        if request.method == "POST":
            search = request.form.get("search")

        page = 1
        if "page" in request.args:
            page = int(request.args.get("page"))
            if not page >= 1:
                page = 1

        if "per_page" in request.args:
            per_page = int(request.args.get("per_page"))
            session["per_page"] = per_page

        if "sort" in request.args:
            sort = request.args.get(("sort"))
            session["sort"] = sort

        if not search:
            reply = requests.get(f"{URL}/recipes?page={page}&per_page={session['per_page']}&sort={session['sort']}")

        else:
            reply = requests.get(f"{URL}/recipes?q={search}")

        recipes = reply.json()["data"]
        last_page = reply.json()["pages"]
        total_elements = reply.json()["total"]

        return render_template("recipes.html", recipes=recipes, user=session, page=page, last_page=last_page, total_elements=total_elements, per_page=session["per_page"])
    else:
        return redirect(url_for("views.home"))


@views.route("/recipes/create-recipe", methods=["GET", "POST"])
def create_recipe():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        num_of_servings = request.form.get("num_of_servings")
        ingredients = request.form.get("ingredients")
        cook_time = request.form.get("cook_time")
        directions = request.form.get("directions")

        if name and description and num_of_servings and ingredients and cook_time and directions:
            if len(name) <= 3:
                flash("Please enter a longer name", category="error")

            elif len(description) <= 5:
                flash("Please enter a longer description", category="error")

            else:
                flash("Successfully created a new recipe", category="success")

                params = {
                    "name": f"{name}",
                    "description": f"{description}",
                    "num_of_servings": int(num_of_servings),
                    "ingredients": f"{ingredients}",
                    "cook_time": int(cook_time),
                    "directions": f"{directions}"
                }

                access_token = session["access_token"]

                reply = requests.post(f"{URL}/recipes", json=params, headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

                id = reply.json()["id"]

                publish = requests.put(f"{URL}/recipes/{id}/publish", headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

                return redirect(url_for("views.recipes"))

    return render_template("create_recipe.html")










