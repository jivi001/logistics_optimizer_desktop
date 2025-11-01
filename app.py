# app.py - COMPLETE FIXED VERSION
import os
import json
import re
from datetime import datetime, timedelta
import google.generativeai as genai
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from route_optimizer import LogisticsRouteOptimizer

# Load environment variables
load_dotenv()

# Configure Flask App
app = Flask(__name__, static_folder='static')

# Configure Gemini API
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    
    # Try different model names
    model_names = [
        'gemini-1.5-flash',
        'gemini-1.5-pro', 
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-1.5-pro',
        'models/gemini-pro'
    ]
    
    gemini_model = None
    for model_name in model_names:
        try:
            gemini_model = genai.GenerativeModel(model_name)
            # Test if it works with a simple query
            test = gemini_model.generate_content("Hello")
            print(f"✓ Gemini API configured successfully with model: {model_name}")
            print(f"✓ API Key found: {api_key[:10]}...")
            break
        except Exception as e:
            print(f"  Model {model_name} failed: {str(e)[:80]}...")
            continue
    
    if not gemini_model:
        raise Exception("No working model found. Please check your API key at https://aistudio.google.com/apikey")
        
except Exception as e:
    gemini_model = None
    print(f"⚠️ Gemini API configuration failed: {e}")
    print("   Please ensure you have a .env file with GEMINI_API_KEY=your_actual_key")

# Global Instance of the Optimizer
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
        return jsonify({"insights": "⚠️ Gemini API is not configured. AI insights are unavailable. Please check your GEMINI_API_KEY in .env file."})

    data = request.json
    route_path = data.get('path')
    distance = data.get('distance')

    if not route_path:
        return jsonify({"error": "Route path is required."}), 400

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
        return jsonify({"insights": f"Could not retrieve AI insights: {str(e)}"}), 500

# --- NEW AI FEATURES ---

@app.route('/api/ai/predict_delivery_time', methods=['POST'])
def predict_delivery_time():
    """AI-powered delivery time prediction considering multiple factors."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    route_path = data.get('path', [])
    distance = data.get('distance', 0)
    vehicle_type = data.get('vehicle_type', 'truck')
    cargo_weight = data.get('cargo_weight', 0)
    departure_time = data.get('departure_time', datetime.now().strftime('%Y-%m-%d %H:%M'))

    prompt = f"""
    As a logistics expert, predict the delivery time for this route considering all factors:
    
    Route: {' -> '.join(route_path)}
    Distance: {distance} km
    Vehicle Type: {vehicle_type}
    Cargo Weight: {cargo_weight} kg
    Planned Departure: {departure_time}
    
    Consider:
    1. Traffic patterns for the time of day
    2. Road conditions between these cities
    3. Required rest stops for long journeys (Indian regulations)
    4. Potential delays at city entry/exit points
    5. Weather conditions for the current season
    
    Provide:
    - Estimated delivery time (in format: "X hours Y minutes")
    - Best departure time if different from planned
    - Risk factors that might cause delays
    
    Format as JSON with keys: estimated_hours, best_departure, risk_factors (array)
    """

    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            prediction_data = json.loads(json_match.group(1))
        else:
            try:
                prediction_data = json.loads(response_text)
            except:
                prediction_data = {"raw_response": response_text}
        
        return jsonify(prediction_data)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not generate prediction: {str(e)}"}), 500

@app.route('/api/ai/optimize_multi_stop', methods=['POST'])
def optimize_multi_stop():
    """AI-powered optimization for routes with multiple delivery stops."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    stops = data.get('stops', [])
    start_city = data.get('start_city')
    
    if len(stops) < 2:
        return jsonify({"error": "At least 2 stops are required."}), 400

    prompt = f"""
    Optimize the delivery sequence for these stops in India:
    
    Starting Point: {start_city}
    Delivery Stops: {', '.join(stops)}
    
    Analyze and suggest:
    1. The most efficient order to visit these stops (considering geography and typical traffic)
    2. Reasoning for the suggested order
    3. Any stops that should be combined or visited consecutively
    
    Provide the response as JSON with keys:
    - optimized_order (array of city names in suggested order)
    - reasoning (string explaining the optimization)
    - estimated_total_distance (rough estimate in km)
    
    Format as JSON only.
    """

    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            optimization_data = json.loads(json_match.group(1))
        else:
            try:
                optimization_data = json.loads(response_text)
            except:
                optimization_data = {"raw_response": response_text}
        
        return jsonify(optimization_data)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not optimize route: {str(e)}"}), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """Natural language chat interface for logistics queries."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {})

    if not user_message:
        return jsonify({"error": "Message is required."}), 400

    context_str = ""
    if context:
        if 'current_route' in context:
            context_str += f"\nCurrent Route: {context['current_route']}"
        if 'distance' in context:
            context_str += f"\nDistance: {context['distance']} km"

    prompt = f"""
    You are an AI assistant for a logistics route optimization system in India. 
    Help the user with their query about route planning, delivery optimization, or logistics operations.
    
    {context_str}
    
    User Question: {user_message}
    
    Provide a helpful, concise response focused on practical logistics advice.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not process your message: {str(e)}"}), 500

@app.route('/api/ai/weather_impact', methods=['POST'])
def weather_impact_analysis():
    """Analyze potential weather impact on the route."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    route_path = data.get('path', [])
    season = data.get('season', 'current')

    prompt = f"""
    Analyze weather impact for this logistics route in India:
    
    Route: {' -> '.join(route_path)}
    Season/Period: {season}
    
    Provide:
    1. Weather risks for each major segment of the route
    2. Recommended precautions
    3. Alternative routes if weather conditions are severe
    4. Best time of day/week to travel this route during this season
    
    Format the response in clear markdown with sections.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"analysis": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not analyze weather impact: {str(e)}"}), 500

@app.route('/api/ai/cost_estimate', methods=['POST'])
def cost_estimate():
    """AI-powered cost estimation for the route."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    distance = data.get('distance', 0)
    vehicle_type = data.get('vehicle_type', 'truck')
    cargo_weight = data.get('cargo_weight', 0)
    fuel_price = data.get('fuel_price', 100)

    prompt = f"""
    Estimate the total cost for this logistics delivery in India:
    
    Distance: {distance} km
    Vehicle: {vehicle_type}
    Cargo Weight: {cargo_weight} kg
    Current Fuel Price: ₹{fuel_price}/liter
    
    Provide detailed cost breakdown:
    1. Fuel costs (estimate mileage based on vehicle type and load)
    2. Toll charges (approximate for Indian highways)
    3. Driver costs (consider journey duration)
    4. Maintenance and vehicle wear
    5. Other operational costs
    
    Provide as JSON with keys:
    - total_cost (in INR)
    - breakdown (object with cost categories)
    - cost_per_km
    - recommendations (array of cost-saving tips)
    
    Format as JSON only.
    """

    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            cost_data = json.loads(json_match.group(1))
        else:
            try:
                cost_data = json.loads(response_text)
            except:
                cost_data = {"raw_response": response_text}
        
        return jsonify(cost_data)
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not estimate costs: {str(e)}"}), 500

@app.route('/api/ai/safety_check', methods=['POST'])
def safety_check():
    """AI-powered safety and compliance check for the route."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured."}), 503

    data = request.json
    route_path = data.get('path', [])
    cargo_type = data.get('cargo_type', 'general')
    distance = data.get('distance', 0)

    prompt = f"""
    Perform a safety and compliance check for this logistics route in India:
    
    Route: {' -> '.join(route_path)}
    Cargo Type: {cargo_type}
    Distance: {distance} km
    
    Check and advise on:
    1. Required permits or documentation for this route
    2. Restricted zones or timing restrictions (if any)
    3. Safety considerations for this cargo type
    4. Recommended rest stops (as per Indian driving regulations)
    5. Emergency contacts or services along the route
    
    Provide clear, actionable safety recommendations in markdown format.
    """

    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"safety_report": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not generate safety report: {str(e)}"}), 500

# --- Main Execution ---
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(debug=debug, port=port, host='0.0.0.0')