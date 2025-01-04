# app/dashboard/routes.py

from flask import render_template
from . import dashboard_bp


@dashboard_bp.route("/teacher", methods=["GET", "POST"])
def dashboard_teacher():
    return render_template("dashboard_t.html")


@dashboard_bp.route("/student", methods=["GET", "POST"])
def dashboard_student():
    return render_template("dashboard_s.html")