from flask import Blueprint, render_template, request, redirect, url_for, session
import requests
import jsonify
from .tests import create_recipe_objects

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
        if "page" in request.args:
            page = int(request.args.get("page"))
            if not page >= 1:
                page = 1
        else:
            page = 1

        reply = requests.get(f"https://rssmilecook.herokuapp.com/recipes?page={page}&per_page=10")

        recipes = reply.json()["data"]

        last_page = reply.json()["pages"]

        return render_template("recipes.html", recipes=recipes, user=session, page=page, last_page=last_page)
    else:
        return redirect(url_for("views.home"))







