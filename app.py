# app.py - COMPLETE WORKING VERSION
import os
import json
import re
from datetime import datetime, timedelta
import google.generativeai as genai
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from route_optimizer import LogisticsRouteOptimizer

load_dotenv()
app = Flask(__name__, static_folder='static')

# Configure Gemini API
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found")
    
    genai.configure(api_key=api_key)
    
    model_names = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest'
    ]
    
    gemini_model = None
    for model_name in model_names:
        try:
            gemini_model = genai.GenerativeModel(model_name)
            test = gemini_model.generate_content("Hello")
            print(f"✓ Gemini API configured with model: {model_name}")
            print(f"✓ API Key: {api_key[:10]}...")
            break
        except Exception as e:
            print(f"  Model {model_name} failed: {str(e)[:80]}...")
            continue
    
    if not gemini_model:
        raise Exception("No working model found")
        
except Exception as e:
    gemini_model = None
    print(f"⚠️ Gemini API failed: {e}")

optimizer = LogisticsRouteOptimizer()
print("✓ Optimizer initialized.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_cities')
def get_cities():
    return jsonify({
        "cities": optimizer.get_all_cities(),
        "coordinates": optimizer.city_coordinates
    })

@app.route('/api/get_shortest_route')
def get_shortest_route():
    source = request.args.get('src')
    destination = request.args.get('dest')

    if not source or not destination:
        return jsonify({"error": "Source and destination required."}), 400

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
        return jsonify({"error": f"No route found."}), 404

@app.route('/api/get_gemini_insights', methods=['POST'])
def get_gemini_insights():
    if not gemini_model:
        return jsonify({"insights": "⚠️ Gemini API not configured."})

    data = request.json
    route_path = data.get('path')
    distance = data.get('distance')

    if not route_path:
        return jsonify({"error": "Route path required."}), 400

    prompt = f"""Analyze this delivery route in India: {' -> '.join(route_path)}, {distance} km
    
    Provide brief insights on:
    - Route summary
    - Potential challenges (traffic, road conditions, weather)
    - Driver tips
    """

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"insights": response.text})
    except Exception as e:
        return jsonify({"insights": f"Error: {str(e)}"}), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    message = data.get('message', '')
    context = data.get('context', {})

    if not message:
        return jsonify({"error": "Message required."}), 400

    context_str = ""
    if context.get('current_route'):
        context_str = f"\nCurrent Route: {context['current_route']}"

    prompt = f"""You're an AI assistant for logistics in India.{context_str}
    
    User: {message}
    
    Provide helpful logistics advice."""

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/predict_delivery_time', methods=['POST'])
def predict_delivery_time():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    
    prompt = f"""Predict delivery time for:
Route: {' -> '.join(data.get('path', []))}
Distance: {data.get('distance')} km
Vehicle: {data.get('vehicle_type')}
Weight: {data.get('cargo_weight')} kg

Provide JSON: {{"estimated_hours": "X", "risk_factors": ["..."]}}"""

    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return jsonify(json.loads(match.group(1)))
        return jsonify({"raw_response": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/optimize_multi_stop', methods=['POST'])
def optimize_multi_stop():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    prompt = f"""Optimize delivery order:
Start: {data.get('start_city')}
Stops: {', '.join(data.get('stops', []))}

JSON: {{"optimized_order": [...], "reasoning": "..."}}"""

    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return jsonify(json.loads(match.group(1)))
        return jsonify({"raw_response": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/cost_estimate', methods=['POST'])
def cost_estimate():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    prompt = f"""Estimate delivery cost (India):
Distance: {data.get('distance')} km
Vehicle: {data.get('vehicle_type')}
Weight: {data.get('cargo_weight')} kg
Fuel: ₹{data.get('fuel_price')}/L

JSON: {{"total_cost": X, "breakdown": {{}}, "recommendations": []}}"""

    try:
        response = gemini_model.generate_content(prompt)
        text = response.text.strip()
        match = re.search(r'```json\s*(\{.*?\})\s*```', text, re.DOTALL)
        if match:
            return jsonify(json.loads(match.group(1)))
        return jsonify({"raw_response": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/weather_impact', methods=['POST'])
def weather_impact():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    prompt = f"""Weather impact analysis:
Route: {' -> '.join(data.get('path', []))}
Season: {data.get('season')}

Provide weather risks and precautions."""

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/safety_check', methods=['POST'])
def safety_check():
    if not gemini_model:
        return jsonify({"error": "Gemini API not configured."}), 503

    data = request.json
    prompt = f"""Safety check:
Route: {' -> '.join(data.get('path', []))}
Cargo: {data.get('cargo_type')}

Provide safety recommendations."""

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"safety_report": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

# app.py - END OF FILE