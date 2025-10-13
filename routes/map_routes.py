from flask import Blueprint, render_template
import csv
import folium

map_bp = Blueprint("map", __name__, template_folder="../templates")

# Load CSV helper
def read_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

# Optional: map minerals for nicer display
def load_minerals():
    minerals = read_csv("minerals.csv")
    return {m["MineralID"]: m["MineralName"] for m in minerals}

@map_bp.route("/map")
def map_dashboard():
    sites = read_csv("sites.csv")
    mineral_map = load_minerals()

    # Center the map roughly over Africa
    folium_map = folium.Map(location=[-10, 20], zoom_start=3)

    # Add all mining sites as markers
    for site in sites:
        lat = float(site["Latitude"])
        lon = float(site["Longitude"])
        site_name = site["SiteName"]
        mineral_name = mineral_map.get(site["MineralID"], "Unknown Mineral")
        production = site["Production_tonnes"]

        popup_text = f"<b>{site_name}</b><br>Mineral: {mineral_name}<br>Production: {production} tonnes"
        folium.Marker(location=[lat, lon], popup=popup_text, icon=folium.Icon(color="green", icon="info-sign")).add_to(folium_map)

    # Save map as HTML string to embed in template
    map_html = folium_map._repr_html_()
    return render_template("maps.html", map_html=map_html)
