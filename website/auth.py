from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requests

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        params = {
            "email": f"{email}",
            "password": f"{password}"
        }

        reply = requests.post("https://rssmilecook.herokuapp.com/token", json=params, headers={"Content-Type": "application/json"})

        if reply.status_code == 200:
            access_token, refresh_token = reply.json()["access_token"], reply.json()["refresh_token"]

            username = requests.get("https://rssmilecook.herokuapp.com/me", headers={f"Authorization": f"Bearer {access_token}"}).json()["username"]

            session["username"] = username
            session["email"] = email
            session["access_token"] = access_token
            session["refresh_token"] = refresh_token

            flash("Successfully logged into your account.", category="success")
            return redirect(url_for("views.home"))

        elif reply.status_code == 403:
            flash("You have not yet been registered. Please check your emails.", category="error")
        elif reply.status_code == 401:
            flash("Email / Password is wrong or you have not made an account yet.", category="error")
        else:
            flash("Something went wrong. Please try again.", category="error")

    return render_template("login.html", user=session)

@auth.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 == password2:
            params = {
                "username": f"{username}",
                "email": f"{email}",
                "password": f"{password1}"
            }
            reply = requests.post("https://rssmilecook.herokuapp.com/users", json=params, headers={"Content-Type": "application/json"})
            if reply.status_code == 201:
                flash("Successfully created your account.", category="success")
                return redirect(url_for("views.home"))
        else:
            flash("Make sure your passwords match.", category="error")

    return render_template("sign-up.html", user=session)


