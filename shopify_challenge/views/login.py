from flask import render_template, request, redirect, session, flash
from flask.views import MethodView

from shopify_challenge.helpers.validations import validate_user
from shopify_challenge.models.user import UserModel

class Login(MethodView):

    def post(self):
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password")

        error = validate_user(username, password)
        if error:
            flash(error, 'danger')
            return render_template("login.html")
        
        session["username"] = username
        session.permanent = True

        return redirect("/")
    
    def get(self):
        session.clear()
        return render_template("login.html")