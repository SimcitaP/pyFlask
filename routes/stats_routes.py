from flask import Blueprint, render_template
import csv
import plotly.graph_objs as go
import plotly.io as pio

stats_bp = Blueprint("stats", __name__, template_folder="../templates")

# Helper function to read CSV
def read_csv(filename):
    with open(filename, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


@stats_bp.route("/")
def stats_dashboard():
    # Load CSV data
    stats = read_csv("production_stats.csv")
    countries = read_csv("countries.csv")
    sites = read_csv("sites.csv")

    # Convert CountryID to readable mapping
    country_map = {c["CountryID"]: c["CountryName"] for c in countries}

    # --- 1️⃣ Link countries to production stats ---
    for row in stats:
        row["CountryName"] = country_map.get(row["CountryID"], "Unknown")

    # --- 2️⃣ Link countries to mining sites ---
    for s in sites:
        s["CountryName"] = country_map.get(s["CountryID"], "Unknown")

    # --- 3️⃣ Aggregate total production by Country ---
    country_production = {}
    for row in stats:
        country = row["CountryName"]
        production = float(row["Production_tonnes"])
        country_production[country] = country_production.get(country, 0) + production

    # --- 4️⃣ Plot 1: Production by Country ---
    country_fig = go.Figure()
    country_fig.add_trace(go.Bar(
        x=list(country_production.keys()),
        y=list(country_production.values()),
        marker=dict(color="steelblue")
    ))
    country_fig.update_layout(
        title="Total Mineral Production by Country",
        xaxis_title="Country",
        yaxis_title="Production (tonnes)",
        template="plotly_white"
    )
    country_chart = pio.to_html(country_fig, full_html=False)

    # --- 5️⃣ Plot 2: GDP vs Mining Revenue (linked to same countries) ---
    gdp = [float(c["GDP_BillionUSD"]) for c in countries]
    mining = [float(c["MiningRevenue_BillionUSD"]) for c in countries]
    names = [c["CountryName"] for c in countries]

    gdp_fig = go.Figure(data=go.Scatter(
        x=gdp, y=mining, mode="markers+text",
        text=names, textposition="top center",
        marker=dict(size=12, color="darkorange")
    ))
    gdp_fig.update_layout(
        title="GDP vs Mining Revenue (Billion USD)",
        xaxis_title="GDP (Billion USD)",
        yaxis_title="Mining Revenue (Billion USD)",
        template="plotly_white"
    )
    gdp_chart = pio.to_html(gdp_fig, full_html=False)

    # --- 6️⃣ Plot 3: Site Map (linked with countries) ---
    map_fig = go.Figure()
    for s in sites:
        map_fig.add_trace(go.Scattergeo(
            lon=[float(s["Longitude"])],
            lat=[float(s["Latitude"])],
            text=f"{s['SiteName']} ({s['CountryName']})",
            mode="markers",
            marker=dict(size=8, color="green", symbol="circle")
        ))

    map_fig.update_layout(
        title="Mining Sites Across Africa (Linked by Country)",
        geo_scope="africa",
        template="plotly_white"
    )
    map_chart = pio.to_html(map_fig, full_html=False)

    # --- 7️⃣ Optional: Production by Year & Country (stacked bar) ---
    year_country_data = {}
    for row in stats:
        year = row["Year"]
        country = row["CountryName"]
        production = float(row["Production_tonnes"])
        year_country_data.setdefault(year, {}).setdefault(country, 0)
        year_country_data[year][country] += production

    stacked_fig = go.Figure()
    for country in country_map.values():
        y_values = []
        for year in sorted(year_country_data.keys()):
            y_values.append(year_country_data[year].get(country, 0))
        stacked_fig.add_trace(go.Bar(
            name=country,
            x=sorted(year_country_data.keys()),
            y=y_values
        ))

    stacked_fig.update_layout(
        barmode="stack",
        title="Yearly Production by Country (Stacked)",
        xaxis_title="Year",
        yaxis_title="Production (tonnes)",
        template="plotly_white"
    )
    stacked_chart = pio.to_html(stacked_fig, full_html=False)

    return render_template(
        "stats.html",
        country_chart=country_chart,
        gdp_chart=gdp_chart,
        map_chart=map_chart,
        stacked_chart=stacked_chart
    )
