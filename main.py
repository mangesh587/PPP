import os
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# --- CONFIGURATION ---
# Ensure this filename matches your uploaded GitHub file exactly
CSV_PATH = "House_Price_3tryer.csv"

def load_data():
    if os.path.exists(CSV_PATH):
        # We load the data once when the app starts
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

df = load_data()

@app.route('/')
def index():
    # Get unique locations for the first dropdown
    locations = sorted(df['Location'].dropna().unique().tolist()) if not df.empty else []
    return render_template('index.html', locations=locations)

@app.route('/get_buildings/<location>')
def get_buildings(location):
    # Get buildings belonging to that location
    buildings = sorted(df[df['Location'] == location]['Building_Name'].unique().tolist())
    return jsonify(buildings)

@app.route('/get_bhk_details/<location>/<building>')
def get_bhk_details(location, building):
    # Get all available BHK types for that specific building
    subset = df[(df['Location'] == location) & (df['Building_Name'] == building)]
    # Send BHK, Area, Price, and Rent info to the frontend
    results = subset[['BHK', 'Carpet_Area', 'Price', 'Rented_Price']].to_dict(orient='records')
    return jsonify(results)

if __name__ == '__main__':
    # Required for Render deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)