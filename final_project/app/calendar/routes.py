# app\calendar\routes.py

from flask import render_template
from . import calendar_bp


@calendar_bp.route("/teacher", methods=["GET", "POST"])
def calendar_teacher():
    return render_template("calendar_t.html")


@calendar_bp.route("/student", methods=["GET", "POST"])
def calendar_student():
    return render_template("calendar_s.html")