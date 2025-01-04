# app\sessions\routes.py

from flask import render_template
from . import sessions_bp


@sessions_bp.route("/teacher", methods=["GET", "POST"])
def sessions_teacher():
    return render_template("sessions_t.html")


@sessions_bp.route("/student", methods=["GET", "POST"])
def sessions_student():
    return render_template("sessions_s.html")