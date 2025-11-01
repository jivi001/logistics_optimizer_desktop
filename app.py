# app.py - AI-Powered Logistics Route Optimizer Backend
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
app.config['JSON_SORT_KEYS'] = False

# Configure Gemini API
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    genai.configure(api_key=api_key)
    
    # Try different model names (based on available models)
    model_names = [
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash',
        'models/gemini-flash-latest',
        'models/gemini-2.5-pro',
        'models/gemini-pro-latest'
    ]
    
    gemini_model = None
    for model_name in model_names:
        try:
            gemini_model = genai.GenerativeModel(model_name)
            # Test if it works with a simple query
            test = gemini_model.generate_content("Hello")
            print(f"✓ Gemini API configured successfully: {model_name}")
            break
        except Exception as model_error:
            print(f"⚠️ Model {model_name} failed: {model_error}")
            continue
    
    if not gemini_model:
        raise Exception("No working Gemini model found")
        
except Exception as e:
    gemini_model = None
    print(f"❌ Gemini API Configuration Failed: {e}")
    print("⚠️ AI features will be unavailable. Please check your GEMINI_API_KEY in .env file")

# Initialize Route Optimizer
optimizer = LogisticsRouteOptimizer()
print(f"✓ Route optimizer initialized with {len(optimizer.get_all_cities())} cities")

# ============================================
# MAIN ROUTES
# ============================================

@app.route('/')
def index():
    """Serves the main HTML user interface."""
    return render_template('index.html')

# ============================================
# CORE API ENDPOINTS
# ============================================

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
        return jsonify({"error": "Source and destination cities are required"}), 400
    
    # Calculate route using Dijkstra's algorithm
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
        return jsonify({"error": f"No route found between {source} and {destination}"}), 404

@app.route('/api/get_gemini_insights', methods=['POST'])
def get_gemini_insights():
    """Generates AI-powered insights for a given route using the Gemini API."""
    if not gemini_model:
        return jsonify({"insights": "⚠️ Gemini API is not configured. AI insights are unavailable."})
    
    data = request.json
    route_path = data.get('path')
    distance = data.get('distance')
    
    if not route_path:
        return jsonify({"error": "Route path is required"}), 400
    
    prompt = f"""Analyze this Indian logistics route and provide concise insights:

Route: {' -> '.join(route_path)} ({distance} km)

Provide in markdown:
- **Route Summary:** Brief description (1-2 sentences)
- **Potential Challenges:** Traffic hotspots, road conditions, weather considerations
- **Driver Tip:** One practical recommendation

Keep it brief and actionable."""
    
    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"insights": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"insights": f"Could not retrieve AI insights: {str(e)}"}), 500

# ============================================
# AI FEATURES ENDPOINTS
# ============================================

@app.route('/api/ai/predict_delivery_time', methods=['POST'])
def predict_delivery_time():
    """AI-powered delivery time prediction considering multiple factors."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    route_path = data.get('path', [])
    distance = data.get('distance', 0)
    vehicle_type = data.get('vehicle_type', 'truck')
    cargo_weight = data.get('cargo_weight', 0)
    departure_time = data.get('departure_time', datetime.now().strftime('%Y-%m-%d %H:%M'))
    
    prompt = f"""Predict delivery time for this Indian logistics route:

Route: {' -> '.join(route_path)} ({distance} km)
Vehicle: {vehicle_type}, Load: {cargo_weight} kg
Departure: {departure_time}

Consider: traffic patterns, mandatory rest stops, city delays, current season weather.

Return JSON only:
{{"estimated_hours": "X hours Y min", "best_departure": "suggested time", "risk_factors": ["factor1", "factor2"]}}"""
    
    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'``````', response_text, re.DOTALL)
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
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    stops = data.get('stops', [])
    start_city = data.get('start_city')
    
    if len(stops) < 2:
        return jsonify({"error": "At least 2 stops are required"}), 400
    
    prompt = f"""Optimize delivery sequence for Indian logistics:

Starting Point: {start_city}
Delivery Stops: {', '.join(stops)}

Return most efficient order considering:
- Geographic proximity
- Typical traffic patterns between cities
- Logical routing to minimize backtracking

JSON format only:
{{"optimized_order": ["city1", "city2", "..."], "reasoning": "brief explanation", "estimated_total_distance": 0}}"""
    
    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'``````', response_text, re.DOTALL)
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
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    user_message = data.get('message', '')
    context = data.get('context', {})
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    context_str = ""
    if context:
        if 'current_route' in context:
            context_str += f"\nContext: Current Route: {context['current_route']}"
        if 'distance' in context:
            context_str += f", Distance: {context['distance']} km"
    
    prompt = f"""You are an AI assistant for a logistics route optimization system in India. 
Provide concise, practical advice for logistics operations.
{context_str}

User Question: {user_message}

Answer briefly and actionably."""
    
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
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    route_path = data.get('path', [])
    season = data.get('season', 'current')
    
    prompt = f"""Weather impact analysis for Indian logistics route:

Route: {' -> '.join(route_path)}
Season: {season}

Provide in markdown:
1. **Weather Risks:** Per route segment
2. **Precautions:** Safety recommendations
3. **Alternatives:** If conditions are severe
4. **Best Time:** Optimal travel window

Keep it actionable and brief."""
    
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
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    distance = data.get('distance', 0)
    vehicle_type = data.get('vehicle_type', 'truck')
    cargo_weight = data.get('cargo_weight', 0)
    fuel_price = data.get('fuel_price', 100)
    
    prompt = f"""Cost estimate for Indian logistics delivery:

Distance: {distance} km
Vehicle: {vehicle_type}, Load: {cargo_weight} kg
Fuel Price: ₹{fuel_price}/liter

Estimate breakdown: fuel (based on vehicle mileage), tolls (Indian highways), driver costs, maintenance, operations.

JSON format only:
{{"total_cost": 0, "breakdown": {{"fuel": 0, "tolls": 0, "driver": 0, "maintenance": 0, "other": 0}}, "cost_per_km": 0, "recommendations": ["tip1", "tip2"]}}"""
    
    try:
        response = gemini_model.generate_content(prompt)
        response_text = response.text.strip()
        
        json_match = re.search(r'``````', response_text, re.DOTALL)
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
    """Comprehensive safety and compliance check for the route."""
    if not gemini_model:
        return jsonify({"error": "Gemini API is not configured"}), 503
    
    data = request.json
    route_path = data.get('path', [])
    cargo_type = data.get('cargo_type', 'general')
    distance = data.get('distance', 0)
    
    prompt = f"""Safety & compliance check for Indian logistics:

Route: {' -> '.join(route_path)} ({distance} km)
Cargo Type: {cargo_type}

Provide in markdown:
1. **Required Documentation:** Permits, licenses
2. **Restricted Zones:** Timing/routing restrictions
3. **Safety Considerations:** Specific to cargo type
4. **Mandatory Stops:** Rest stops per regulations
5. **Emergency Contacts:** Key services

Brief and actionable."""
    
    try:
        response = gemini_model.generate_content(prompt)
        return jsonify({"safety_report": response.text})
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return jsonify({"error": f"Could not generate safety report: {str(e)}"}), 500

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# ============================================
# RUN APPLICATION
# ============================================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    
    print("\n" + "="*50)
    print("🚚 AI-Powered Logistics Route Optimizer")
    print("="*50)
    print(f"✓ Server running on http://localhost:{port}")
    print(f"✓ Debug mode: {debug}")
    print(f"✓ Gemini AI: {'Enabled' if gemini_model else 'Disabled'}")
    print("="*50 + "\n")
    
    app.run(debug=debug, port=port, host='0.0.0.0')
    
@app.route('/api/calculate_toll', methods=['POST'])
def calculate_toll():
    """Calculate toll charges for the route."""
    data = request.json
    distance = data.get('distance', 0)
    vehicle_type = data.get('vehicle_type', 'truck')
    
    # Toll rates per 100 km (NHAI approximate rates in INR)
    toll_rates = {
        'car': 80,
        'lcv': 130,
        'truck': 270,
        'multi-axle': 400
    }
    
    rate_per_km = toll_rates.get(vehicle_type, 270) / 100
    total_toll = round(distance * rate_per_km)
    estimated_plazas = max(1, round((distance / 100) * 1.5))
    
    return jsonify({
        'total_toll': total_toll,
        'estimated_plazas': estimated_plazas,
        'cost_per_100km': toll_rates.get(vehicle_type, 270),
        'vehicle_type': vehicle_type
    })

#   ============================================