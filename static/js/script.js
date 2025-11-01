// script.js - Complete AI-Powered Logistics Route Optimizer (FIXED)

// ===== GLOBAL STATE =====
let map = null;
let cityCoordinates = {};
let routeLayer = null;
let currentRouteData = null;
let multiStopList = [];

// Toll rates per 100 km (approximate NHAI rates in INR)
const TOLL_RATES = {
    car: 80,           // Car/Jeep/Van
    lcv: 130,          // Light Commercial Vehicle
    truck: 270,        // Heavy Truck (2-Axle)
    'multi-axle': 400  // Multi-Axle Vehicle (3+ Axle)
};

// Average toll plazas per 100 km on national highways
const PLAZAS_PER_100KM = 1.5;

// ===== DOM READY =====
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

// ===== INITIALIZATION =====
function initializeApp() {
    initMap();
    fetchCities();
    attachEventListeners();
    setupFeatureNavigation();
    setupAIHubToggle();
    setupTollCalculator();
}

// ===== MAP FUNCTIONS =====
function initMap() {
    if (map) return;
    
    map = L.map('map').setView([20.5937, 78.9629], 5);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 18
    }).addTo(map);
}

function displayRouteOnMap(routeData) {
    // Remove existing route
    if (routeLayer) {
        map.removeLayer(routeLayer);
    }
    
    // Validate input
    if (!routeData || !routeData.path || !routeData.coordinates) {
        console.error('Invalid route data:', routeData);
        showAlert('Error: Invalid route data received', 'error');
        return;
    }
    
    // Create coordinates array with null check
    const coordinates = [];
    for (const city of routeData.path) {
        const coords = routeData.coordinates[city];
        
        if (!coords) {
            console.error(`Missing coordinates for city: ${city}`);
            showAlert(`Error: Missing coordinates for ${city}`, 'error');
            return;
        }
        
        if (!Array.isArray(coords) || coords.length < 2) {
            console.error(`Invalid coordinates for city: ${city}`, coords);
            showAlert(`Error: Invalid coordinates for ${city}`, 'error');
            return;
        }
        
        coordinates.push([coords[0], coords[1]]);
    }
    
    // Check if we have valid coordinates
    if (coordinates.length === 0) {
        console.error('No valid coordinates found');
        showAlert('Error: No valid coordinates for route', 'error');
        return;
    }
    
    routeLayer = L.layerGroup();
    
    try {
        // Draw route line
        const routeLine = L.polyline(coordinates, {
            color: '#667eea',
            weight: 4,
            opacity: 0.8
        }).addTo(routeLayer);
        
        // Add markers
        routeData.path.forEach((city, index) => {
            const coords = routeData.coordinates[city];
            const isStart = index === 0;
            const isEnd = index === routeData.path.length - 1;
            
            const iconHtml = isStart ? '🟢' : isEnd ? '🔴' : '📍';
            
            const marker = L.marker([coords[0], coords[1]], {
                icon: L.divIcon({
                    html: `<div style="font-size: 24px;">${iconHtml}</div>`,
                    className: 'custom-marker',
                    iconSize: [30, 30]
                })
            }).bindPopup(`<b>${city}</b>`);
            
            marker.addTo(routeLayer);
        });
        
        routeLayer.addTo(map);
        
        // Fit map to route bounds
        map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
        
    } catch (error) {
        console.error('Error displaying route on map:', error);
        showAlert('Error displaying route on map', 'error');
    }
}

// ===== API CALLS =====
async function fetchCities() {
    try {
        showLoader(true);
        const response = await fetch('/api/get_cities');
        
        if (!response.ok) throw new Error('Failed to fetch cities');
        
        const data = await response.json();
        cityCoordinates = data.coordinates;
        populateDropdowns(data.cities);
        
    } catch (error) {
        showAlert('Could not load city data. Please refresh the page.', 'error');
        console.error(error);
    } finally {
        showLoader(false);
    }
}

async function findRoute() {
    const source = document.getElementById('source-city').value;
    const destination = document.getElementById('destination-city').value;
    
    if (!source || !destination) {
        showAlert('Please select both source and destination cities', 'error');
        return;
    }
    
    if (source === destination) {
        showAlert('Source and destination cannot be the same', 'error');
        return;
    }
    
    closeAlert();
    showLoader(true);
    hideTollCalculator();
    document.getElementById('find-route-btn').disabled = true;
    
    try {
        const response = await fetch(`/api/get_shortest_route?src=${encodeURIComponent(source)}&dest=${encodeURIComponent(destination)}`);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to find route');
        }
        
        const routeData = await response.json();
        
        // Debug logging
        console.log('=== Route Data ===');
        console.log('Path:', routeData.path);
        console.log('Coordinates:', routeData.coordinates);
        console.log('==================');
        
        currentRouteData = routeData;
        
        displayRouteSummary(routeData);
        displayRouteOnMap(routeData);
        await fetchAIInsights(routeData);
        
    } catch (error) {
        showAlert(error.message, 'error');
        console.error(error);
    } finally {
        showLoader(false);
        document.getElementById('find-route-btn').disabled = false;
    }
}

async function fetchAIInsights(routeData) {
    const insightsPanel = document.getElementById('ai-insights-content');
    insightsPanel.innerHTML = '<div class="empty-state"><p>⏳ Generating AI insights...</p></div>';
    
    try {
        const response = await fetch('/api/get_gemini_insights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: routeData.path,
                distance: routeData.distance
            })
        });
        
        const data = await response.json();
        
        // Format markdown-style text to HTML
        let insightsHtml = data.insights
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
        
        insightsPanel.innerHTML = `<div class="insights-text">${insightsHtml}</div>`;
        
    } catch (error) {
        insightsPanel.innerHTML = '<div class="empty-state"><p>⚠️ Could not generate AI insights</p></div>';
        console.error(error);
    }
}

// ===== AI FEATURES =====

// AI Chat
async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    const chatMessages = document.getElementById('chat-messages');
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Add loading indicator
    const loadingId = 'loading-' + Date.now();
    chatMessages.innerHTML += `<div id="${loadingId}" class="chat-message ai"><div class="typing-indicator"><span></span><span></span><span></span></div></div>`;
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    try {
        const context = currentRouteData ? {
            current_route: currentRouteData.path.join(' → '),
            distance: currentRouteData.distance
        } : {};
        
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, context })
        });
        
        const data = await response.json();
        
        // Remove loading indicator
        document.getElementById(loadingId)?.remove();
        
        if (data.response) {
            addChatMessage(data.response, 'ai');
        } else {
            addChatMessage('Sorry, I could not process your request.', 'ai');
        }
        
    } catch (error) {
        document.getElementById(loadingId)?.remove();
        addChatMessage('Error: Could not connect to AI assistant.', 'ai');
        console.error(error);
    }
}

function addChatMessage(message, type) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${type}`;
    messageDiv.innerHTML = `<p>${message.replace(/\n/g, '<br>')}</p>`;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Delivery Time Prediction
async function predictDeliveryTime() {
    if (!currentRouteData) {
        showAlert('Please calculate a route first', 'error');
        return;
    }
    
    const vehicleType = document.getElementById('vehicle-type').value;
    const cargoWeight = document.getElementById('cargo-weight').value;
    const departureTime = document.getElementById('departure-time').value;
    
    if (!cargoWeight || !departureTime) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    const resultDiv = document.getElementById('predict-result');
    resultDiv.innerHTML = '<p>⏳ Analyzing delivery factors...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/ai/predict_delivery_time', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: currentRouteData.path,
                distance: currentRouteData.distance,
                vehicle_type: vehicleType,
                cargo_weight: cargoWeight,
                departure_time: departureTime
            })
        });
        
        const data = await response.json();
        
        if (data.estimated_hours) {
            resultDiv.innerHTML = `
                <h4>🚚 Delivery Time Prediction</h4>
                <p><strong>Estimated Time:</strong> ${data.estimated_hours}</p>
                <p><strong>Best Departure:</strong> ${data.best_departure || departureTime}</p>
                ${data.risk_factors ? `<p><strong>Risk Factors:</strong></p><ul>${data.risk_factors.map(r => `<li>${r}</li>`).join('')}</ul>` : ''}
            `;
        } else {
            resultDiv.innerHTML = `<p>${data.raw_response || 'Prediction unavailable'}</p>`;
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<p>⚠️ Could not generate prediction</p>';
        console.error(error);
    }
}

// Multi-Stop Optimization
function addStop() {
    const stopCity = document.getElementById('stop-city').value;
    
    if (!stopCity) {
        showAlert('Please select a city to add', 'error');
        return;
    }
    
    if (multiStopList.includes(stopCity)) {
        showAlert('City already added', 'error');
        return;
    }
    
    multiStopList.push(stopCity);
    updateStopsDisplay();
    document.getElementById('stop-city').value = '';
}

function removeStop(city) {
    multiStopList = multiStopList.filter(c => c !== city);
    updateStopsDisplay();
}

function updateStopsDisplay() {
    const stopsDisplay = document.getElementById('stops-display');
    
    if (multiStopList.length === 0) {
        stopsDisplay.innerHTML = '';
        return;
    }
    
    stopsDisplay.innerHTML = multiStopList.map(city => `
        <div class="stop-chip">
            <span>${city}</span>
            <button class="remove-chip" onclick="removeStop('${city}')">×</button>
        </div>
    `).join('');
}

async function optimizeMultiStop() {
    const startCity = document.getElementById('start-city').value;
    
    if (!startCity) {
        showAlert('Please select a starting city', 'error');
        return;
    }
    
    if (multiStopList.length < 2) {
        showAlert('Please add at least 2 stops', 'error');
        return;
    }
    
    const resultDiv = document.getElementById('multistop-result');
    resultDiv.innerHTML = '<p>⏳ Optimizing route...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/ai/optimize_multi_stop', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                start_city: startCity,
                stops: multiStopList
            })
        });
        
        const data = await response.json();
        
        if (data.optimized_order) {
            resultDiv.innerHTML = `
                <h4>🗺️ Optimized Route</h4>
                <p><strong>Suggested Order:</strong></p>
                <ol>${data.optimized_order.map(city => `<li>${city}</li>`).join('')}</ol>
                <p><strong>Reasoning:</strong> ${data.reasoning}</p>
                <p><strong>Estimated Distance:</strong> ${data.estimated_total_distance} km</p>
            `;
        } else {
            resultDiv.innerHTML = `<p>${data.raw_response || 'Optimization unavailable'}</p>`;
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<p>⚠️ Could not optimize route</p>';
        console.error(error);
    }
}

// Cost Estimation
async function estimateCost() {
    if (!currentRouteData) {
        showAlert('Please calculate a route first', 'error');
        return;
    }
    
    const vehicleType = document.getElementById('cost-vehicle-type').value;
    const cargoWeight = document.getElementById('cost-cargo-weight').value;
    const fuelPrice = document.getElementById('fuel-price').value;
    
    if (!cargoWeight || !fuelPrice) {
        showAlert('Please fill in all fields', 'error');
        return;
    }
    
    const resultDiv = document.getElementById('cost-result');
    resultDiv.innerHTML = '<p>⏳ Calculating costs...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/ai/cost_estimate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                distance: currentRouteData.distance,
                vehicle_type: vehicleType,
                cargo_weight: cargoWeight,
                fuel_price: fuelPrice
            })
        });
        
        const data = await response.json();
        
        if (data.total_cost) {
            let breakdownHtml = '';
            if (data.breakdown) {
                breakdownHtml = '<div class="cost-breakdown">';
                for (const [key, value] of Object.entries(data.breakdown)) {
                    breakdownHtml += `<div class="cost-item"><strong>${key}:</strong> ₹${value}</div>`;
                }
                breakdownHtml += '</div>';
            }
            
            resultDiv.innerHTML = `
                <h4>💰 Cost Estimate</h4>
                <p><strong>Total Cost:</strong> ₹${data.total_cost}</p>
                <p><strong>Cost per km:</strong> ₹${data.cost_per_km || 'N/A'}</p>
                ${breakdownHtml}
                ${data.recommendations ? `<p><strong>Cost-saving Tips:</strong></p><ul>${data.recommendations.map(r => `<li>${r}</li>`).join('')}</ul>` : ''}
            `;
        } else {
            resultDiv.innerHTML = `<p>${data.raw_response || 'Cost estimation unavailable'}</p>`;
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<p>⚠️ Could not estimate costs</p>';
        console.error(error);
    }
}

// Weather Impact
async function analyzeWeather() {
    if (!currentRouteData) {
        showAlert('Please calculate a route first', 'error');
        return;
    }
    
    const season = document.getElementById('season').value;
    
    const resultDiv = document.getElementById('weather-result');
    resultDiv.innerHTML = '<p>⏳ Analyzing weather impact...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/ai/weather_impact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: currentRouteData.path,
                season: season
            })
        });
        
        const data = await response.json();
        
        if (data.analysis) {
            resultDiv.innerHTML = `<div class="weather-analysis">${data.analysis.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</div>`;
        } else {
            resultDiv.innerHTML = '<p>Weather analysis unavailable</p>';
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<p>⚠️ Could not analyze weather impact</p>';
        console.error(error);
    }
}

// Safety Check
async function runSafetyCheck() {
    if (!currentRouteData) {
        showAlert('Please calculate a route first', 'error');
        return;
    }
    
    const cargoType = document.getElementById('cargo-type').value;
    
    const resultDiv = document.getElementById('safety-result');
    resultDiv.innerHTML = '<p>⏳ Running safety check...</p>';
    resultDiv.classList.remove('hidden');
    
    try {
        const response = await fetch('/api/ai/safety_check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: currentRouteData.path,
                cargo_type: cargoType,
                distance: currentRouteData.distance
            })
        });
        
        const data = await response.json();
        
        if (data.safety_report) {
            resultDiv.innerHTML = `<div class="safety-report">${data.safety_report.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')}</div>`;
        } else {
            resultDiv.innerHTML = '<p>Safety report unavailable</p>';
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<p>⚠️ Could not generate safety report</p>';
        console.error(error);
    }
}

// ===== TOLL CALCULATOR =====
function setupTollCalculator() {
    const tollVehicleSelect = document.getElementById('toll-vehicle-type');
    if (tollVehicleSelect) {
        tollVehicleSelect.addEventListener('change', () => {
            if (currentRouteData) {
                calculateTollCharges(currentRouteData);
            }
        });
    }
}

function showTollCalculator(routeData) {
    const tollSection = document.getElementById('toll-calculator');
    tollSection.classList.remove('hidden');
    calculateTollCharges(routeData);
}

function hideTollCalculator() {
    const tollSection = document.getElementById('toll-calculator');
    tollSection.classList.add('hidden');
}

function calculateTollCharges(routeData) {
    const distance = routeData.distance;
    const vehicleType = document.getElementById('toll-vehicle-type').value;
    const ratePerKm = TOLL_RATES[vehicleType] / 100;
    
    // Calculate total toll
    const totalToll = Math.round(distance * ratePerKm);
    
    // Calculate estimated toll plazas
    const estimatedPlazas = Math.ceil((distance / 100) * PLAZAS_PER_100KM);
    
    // Calculate cost per 100km
    const costPer100km = TOLL_RATES[vehicleType];
    
    // Update display
    document.getElementById('total-toll').textContent = `₹${totalToll.toLocaleString('en-IN')}`;
    document.getElementById('toll-plaza-count').innerHTML = `
        <span class="plaza-number">${estimatedPlazas}</span>
        <span class="plaza-text">plazas estimated</span>
    `;
    document.getElementById('cost-per-100km').textContent = `₹${costPer100km}`;
    
    // Generate route segments
    generateTollSegments(routeData, vehicleType);
}

function generateTollSegments(routeData, vehicleType) {
    const segmentsContainer = document.getElementById('toll-segments');
    const path = routeData.path;
    const ratePerKm = TOLL_RATES[vehicleType] / 100;
    
    if (path.length < 2) {
        segmentsContainer.innerHTML = '<p style="color: var(--text-tertiary);">No segments to display</p>';
        return;
    }
    
    let segmentsHTML = '';
    const totalDistance = routeData.distance;
    
    // Calculate approximate distance per segment
    const avgSegmentDistance = totalDistance / (path.length - 1);
    
    for (let i = 0; i < path.length - 1; i++) {
        const fromCity = path[i];
        const toCity = path[i + 1];
        
        // Estimate segment distance
        const segmentDistance = Math.round(avgSegmentDistance);
        const segmentCost = Math.round(segmentDistance * ratePerKm);
        
        segmentsHTML += `
            <div class="toll-segment-item">
                <div class="segment-route">
                    <div class="segment-cities">${fromCity} → ${toCity}</div>
                    <div class="segment-distance">${segmentDistance} km</div>
                </div>
                <div class="segment-cost">₹${segmentCost.toLocaleString('en-IN')}</div>
            </div>
        `;
    }
    
    segmentsContainer.innerHTML = segmentsHTML;
}

// ===== UI HELPER FUNCTIONS =====
function populateDropdowns(cities) {
    const sourceSelect = document.getElementById('source-city');
    const destinationSelect = document.getElementById('destination-city');
    const startCitySelect = document.getElementById('start-city');
    const stopCitySelect = document.getElementById('stop-city');
    
    cities.forEach(city => {
        sourceSelect.add(new Option(city, city));
        destinationSelect.add(new Option(city, city));
        startCitySelect.add(new Option(city, city));
        stopCitySelect.add(new Option(city, city));
    });
}

function displayRouteSummary(data) {
    const summaryDiv = document.getElementById('route-summary');
    const pathString = data.path.join(' → ');
    
    summaryDiv.innerHTML = `
        <div class="route-info">
            <div class="info-item">
                <span class="info-label">Route</span>
                <span class="info-value">${pathString}</span>
            </div>
            <div class="info-item">
                <span class="info-label">Distance</span>
                <span class="info-value">${data.distance} km</span>
            </div>
            <div class="info-item">
                <span class="info-label">Estimated Time</span>
                <span class="info-value">${data.time_hours} hours</span>
            </div>
        </div>
    `;
    
    // Show toll calculator
    showTollCalculator(data);
}

function showLoader(show) {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.classList.toggle('hidden', !show);
    }
}

function showAlert(message, type = 'error') {
    const alertBanner = document.getElementById('alert-banner');
    const alertMessage = document.getElementById('alert-message');
    
    if (alertMessage) {
        alertMessage.textContent = message;
        alertBanner.classList.remove('hidden');
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            closeAlert();
        }, 5000);
    }
}

function closeAlert() {
    const alertBanner = document.getElementById('alert-banner');
    if (alertBanner) {
        alertBanner.classList.add('hidden');
    }
}

// Feature Navigation
function setupFeatureNavigation() {
    const navPills = document.querySelectorAll('.nav-pill');
    const featurePanels = document.querySelectorAll('.feature-panel');
    
    navPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const feature = pill.dataset.feature;
            
            // Update active pill
            navPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');
            
            // Show corresponding panel
            featurePanels.forEach(panel => {
                panel.classList.remove('active');
                if (panel.id === `${feature}-feature`) {
                    panel.classList.add('active');
                }
            });
        });
    });
}

// AI Hub Toggle
function setupAIHubToggle() {
    const toggleHeader = document.getElementById('ai-hub-toggle');
    const aiHub = document.querySelector('.ai-hub');
    
    if (!toggleHeader || !aiHub) return;
    
    // Load saved state from localStorage
    const isCollapsed = localStorage.getItem('aiHubCollapsed') === 'true';
    if (isCollapsed) {
        aiHub.classList.add('collapsed');
    }
    
    toggleHeader.addEventListener('click', () => {
        aiHub.classList.toggle('collapsed');
        
        // Save state to localStorage
        const collapsed = aiHub.classList.contains('collapsed');
        localStorage.setItem('aiHubCollapsed', collapsed);
        
        // Smooth scroll to section if expanding
        if (!collapsed) {
            setTimeout(() => {
                toggleHeader.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'nearest' 
                });
            }, 100);
        }
    });
}

// ===== EVENT LISTENERS =====
function attachEventListeners() {
    // Main route finder
    const findRouteBtn = document.getElementById('find-route-btn');
    if (findRouteBtn) {
        findRouteBtn.addEventListener('click', findRoute);
    }
    
    // AI Chat
    const chatSendBtn = document.getElementById('chat-send-btn');
    const chatInput = document.getElementById('chat-input');
    
    if (chatSendBtn) {
        chatSendBtn.addEventListener('click', sendChatMessage);
    }
    if (chatInput) {
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendChatMessage();
        });
    }
    
    // ETA Prediction
    const predictBtn = document.getElementById('predict-btn');
    if (predictBtn) {
        predictBtn.addEventListener('click', predictDeliveryTime);
    }
    
    // Multi-Stop
    const addStopBtn = document.getElementById('add-stop-btn');
    const optimizeStopsBtn = document.getElementById('optimize-stops-btn');
    
    if (addStopBtn) {
        addStopBtn.addEventListener('click', addStop);
    }
    if (optimizeStopsBtn) {
        optimizeStopsBtn.addEventListener('click', optimizeMultiStop);
    }
    
    // Cost Estimation
    const costBtn = document.getElementById('cost-btn');
    if (costBtn) {
        costBtn.addEventListener('click', estimateCost);
    }
    
    // Weather Analysis
    const weatherBtn = document.getElementById('weather-btn');
    if (weatherBtn) {
        weatherBtn.addEventListener('click', analyzeWeather);
    }
    
    // Safety Check
    const safetyBtn = document.getElementById('safety-btn');
    if (safetyBtn) {
        safetyBtn.addEventListener('click', runSafetyCheck);
    }
}

// Make functions globally accessible
window.removeStop = removeStop;
window.closeAlert = closeAlert;
window.showAlert = showAlert;
window.showLoader = showLoader;
window.displayRouteSummary = displayRouteSummary;
window.displayRouteOnMap = displayRouteOnMap;
window.fetchCities = fetchCities;
window.fetchAIInsights = fetchAIInsights;
window.generateTollSegments = generateTollSegments;
window.calculateTollCharges = calculateTollCharges;
window.showTollCalculator = showTollCalculator;
window.hideTollCalculator = hideTollCalculator;
window.setupTollCalculator = setupTollCalculator;
window.setupFeatureNavigation = setupFeatureNavigation;
window.setupAIHubToggle = setupAIHubToggle;
window.initializeApp = initializeApp;
window.initMap = initMap;
window.attachEventListeners = attachEventListeners;
window.findRoute = findRoute;
window.predictDeliveryTime = predictDeliveryTime;
window.addStop = addStop;
window.optimizeMultiStop = optimizeMultiStop;