# app\registry\routes.py

from flask import render_template
from . import registery_bp


@registery_bp.route("/registry", methods=["GET", "POST"])
def register():
    return render_template("registry.html")

