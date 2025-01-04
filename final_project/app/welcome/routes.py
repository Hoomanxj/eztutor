# app\welcome\routes.py

from flask import render_template
from . import welcome_bp


@welcome_bp.route("/", methods=["GET", "POST"])
def welcome():
    return render_template("welcome.html")
