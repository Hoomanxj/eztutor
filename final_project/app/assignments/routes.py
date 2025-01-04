# app\assignments\routes.py

from flask import render_template
from . import assignments_bp


@assignments_bp.route("/teacher", methods=["GET", "POST"])
def assignments_teacher():
    return render_template("assignments_t.html")


@assignments_bp.route("/student", methods=["GET", "POST"])
def assignments_student():
    return render_template("assignments_s.html")