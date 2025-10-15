# app.py
import os
import json
import google.generativeai as genai
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from route_optimizer import LogisticsRouteOptimizer # Import your class

# Load environment variables (for Gemini API key)
load_dotenv()

# Configure Flask App
app = Flask(__name__)

# Configure Gemini API
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-pro')
    print("✓ Gemini API configured successfully.")
except Exception as e:
    gemini_model = None
    print(f"⚠️ Gemini API configuration failed: {e}. AI features will be disabled.")
    print("   Please ensure you have a .env file with your GEMINI_API_KEY.")


# --- Global Instance of the Optimizer ---
# Create a single instance of the optimizer to be used across requests
optimizer = LogisticsRouteOptimizer()
print("✓ Logistics Route Optimizer initialized.")

# --- HTML Serving Route ---
@app.route('/')
def index():
    """Serves the main HTML user interface."""
    return render_template('index.html')

# --- API Endpoints ---
@app.route('/api/get_cities')
def get_cities():
    """Returns a list of all cities and their coordinates."""
    return jsonify({
        "cities": optimizer.get_all_cities(),
        "coordinates": optimizer.city_coordinates
    })

@app.route('/api/get_shortest_route')
def get_shortest_route():
    """Calculates and returns the shortest route between two cities."""
    source = request.args.get('src')
    destination = request.args.get('dest')

    if not source or not destination:
        return jsonify({"error": "Source and destination cities are required."}), 400

    path, distance = optimizer.dijkstra(source.title(), destination.title())

    if path and distance is not None:
        estimated_time = optimizer.calculate_estimated_time(distance)
        return jsonify({
            "path": path,
            "distance": round(distance, 2),
            "time_hours": round(estimated_time, 2),
            "coordinates": {city: optimizer.city_coordinates.get(city) for city in path}
        })
    else:
        return jsonify({"error": f"No route found between {source} and {destination}."}), 404

@app.route('/api/get_gemini_insights', methods=['POST'])
def get_gemini_insights():
    """Generates AI-powered insights for a given route using the Gemini API."""
    if not gemini_model:
        return jsonify({"insights": "Gemini API is not configured. AI insights are unavailable."})

    data = request.json
    route_path = data.get('path')
    distance = data.get('distance')

    if not route_path:
        return jsonify({"error": "Route path is required."}), 400

    # Create a detailed prompt for the Gemini API
    prompt = f"""
    Analyze the following logistics delivery route in India and provide brief, helpful insights for a truck driver.
    
    Route: {' -> '.join(route_path)}
    Total Distance: {distance} km

    Provide insights on the following points in a concise, bulleted list (using markdown):
    - **General Route Summary:** Briefly describe the journey.
    - **Potential Challenges:** Mention common challenges like potential for highway traffic near major cities (like Mumbai, Delhi), varied road conditions in certain regions, or weather considerations (e.g., monsoon season impact). Keep it general.
    - **Driver Tip:** Offer a practical tip for the driver, such as planning for stops or checking weather forecasts.
    
    Format the response clearly in markdown.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"insights": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"insights": "Could not retrieve AI insights at this time."}), 500

# --- Main Execution ---
if __name__ == '__main__':
    # Use port 5001 to avoid potential conflicts with other apps
    app.run(debug=True, port=5001)