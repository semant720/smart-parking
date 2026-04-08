from flask import Flask, render_template, jsonify
import json, math, random

app = Flask(__name__)

# CGC Jhanjeri fallback location
CGC_LAT = 30.6873
CGC_LNG = 76.7256

# Google Maps API Key (should be in environment variable in production)
GOOGLE_MAPS_API_KEY = "AIzaSyCMR6wHCjf-5Tbp-v_AKn5JR_42OGP-kQA"

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

@app.route("/")
def index():
    return render_template("index.html", api_key=GOOGLE_MAPS_API_KEY)

@app.route("/data")
def data():
    with open("parking.json") as f:
        parking_data = json.load(f)

    nearest = None
    min_distance = float("inf")

    for p in parking_data:
        p["status"] = random.choice(["Available", "Full"])
        dist = calculate_distance(CGC_LAT, CGC_LNG, p["lat"], p["lng"])
        p["distance"] = dist

        if p["status"] == "Available" and dist < min_distance:
            min_distance = dist
            nearest = p

    return jsonify({
        "all_parking": parking_data,
        "nearest_parking": nearest
    })

if __name__ == "__main__":
    app.run(debug=True)
