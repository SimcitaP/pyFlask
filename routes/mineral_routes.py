import csv
from flask import Blueprint, render_template

minerals_bp = Blueprint("minerals", __name__, template_folder="templates")

def load_minerals():
    minerals = []
    try:
        with open("minerals.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                minerals.append(row)
    except FileNotFoundError:
        print("⚠️ minerals.csv not found! Please make sure the file exists.")
    return minerals

@minerals_bp.route("/")
def index():
    minerals = load_minerals()
    return render_template("minerals.html", minerals=minerals)
