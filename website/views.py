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

        return render_template("recipes.html", recipes=recipes, user=session, page=page, last_page=last_page, total_elements=total_elements, per_page=session["per_page"], session=session)
    else:
        return redirect(url_for("views.home"))


@views.route("/recipes/create-recipe", methods=["GET", "POST"])
def create_recipe():
    if "email" in session:
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

                    if reply.status_code == 201:
                        id = reply.json()["id"]
                        publish = requests.put(f"{URL}/recipes/{id}/publish", headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})
                        flash("Successfully created a new recipe", category="success")

                    elif reply.status_code == 400:
                        flash("One or more or the entered values are invalid", category="error")
                    else:
                        flash("Something went wrong. Please try again", category="error")

                    return redirect(url_for("views.recipes"))

        return render_template("create_recipe.html", user=session)


@views.route("/recipes/edit-recipe", methods=["GET", "POST"])
def edit_recipe():
    if "email" in session:
        try:
            id = request.args.get("id")
            reply = requests.get(f"{URL}/recipes/{id}")

            author = reply.json()["author"]["username"]
            name = reply.json()["name"]
            description = reply.json()["description"]
            num_of_servings = reply.json()["num_of_servings"]
            ingredients = reply.json()["ingredients"]
            cook_time = reply.json()["cook_time"]
            directions = reply.json()["directions"]

            if author == session["username"]:
                if request.method == "POST":
                    data = request.form

                    name = data["name"]
                    description = data["description"]
                    num_of_servings = data["num_of_servings"]
                    ingredients = data["ingredients"]
                    cook_time = data["cook_time"]
                    directions = data["directions"]

                    params = {
                        "name": f"{name}",
                        "description": f"{description}",
                        "num_of_servings": int(num_of_servings),
                        "ingredients": f"{ingredients}",
                        "cook_time": int(cook_time),
                        "directions": f"{directions}"
                    }

                    access_token = session["access_token"]
                    patch = requests.patch(f"{URL}/recipes/{id}", json=params, headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

                    if patch.status_code == 200:
                        flash("Successfully made changes to recipe", category="success")

                    elif patch.status_code == 500:
                        flash("One or more or the entered values are invalid", category="error")
                    else:
                        flash("Something went wrong. Pleasy try again", category="error")

                    return redirect(url_for("views.recipes"))

                return render_template("edit_recipe.html", user=session, name=name, description=description, num_of_servings=num_of_servings, ingredients=ingredients, cook_time=cook_time, directions=directions)

            else:
                return redirect(url_for("views.recipes"))

        except Exception:
            return redirect(url_for("views.recipes"))

@views.route("/recipes/delete-recipe")
def delete_recipe():
    delete = request.args.get("delete")
    if delete == "true":
        id = request.args.get("id")
        access_token = session["access_token"]
        delete = requests.delete(f"{URL}/recipes/{id}", headers={"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"})

        if delete.status_code == 204:
            flash("Successfully removed recipe", category="success")
        else:
            flash("Something went wrong. Please try again", category="error")

        return redirect(url_for("views.recipes"))
    return render_template("delete_recipe.html")











