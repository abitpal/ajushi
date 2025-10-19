from flask import render_template, redirect, url_for, request, abort, jsonify

from dashboard.app import app

@app.route("/")
def dashboard():
    return render_template("dashboard.html")