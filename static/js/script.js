// script.js
document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const sourceSelect = document.getElementById('source-city');
    const destinationSelect = document.getElementById('destination-city');
    const findRouteBtn = document.getElementById('find-route-btn');
    const mapContainer = document.getElementById('map');
    const routeSummaryPanel = document.getElementById('route-summary');
    const aiInsightsPanel = document.getElementById('ai-insights');
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');

    // --- State ---
    let map = null;
    let cityCoordinates = {};
    let routeLayer = null;

    // --- Map Initialization ---
    function initMap() {
        if (map) return; // Prevent re-initialization
        // Initialize map centered on India
        map = L.map(mapContainer).setView([20.5937, 78.9629], 5);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
    }

    // --- API Calls ---
    async function fetchCities() {
        try {
            const response = await fetch('/api/get_cities');
            if (!response.ok) throw new Error('Failed to fetch cities.');
            const data = await response.json();
            cityCoordinates = data.coordinates; // Store coordinates
            populateDropdowns(data.cities);
        } catch (error) {
            showError('Could not load city data. Please try refreshing the page.');
            console.error(error);
        }
    }

    // --- UI Updates ---
    function populateDropdowns(cities) {
        cities.forEach(city => {
            const option1 = new Option(city, city);
            const option2 = new Option(city, city);
            sourceSelect.add(option1);
            destinationSelect.add(option2);
        });
    }

    function showLoader(show) {
        loader.style.display = show ? 'block' : 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
    }

    function clearError() {
        errorMessage.style.display = 'none';
    }
    
    function resetUI() {
        routeSummaryPanel.innerHTML = '<h2>Route Details</h2><p>Select a source and destination to see the optimal route.</p>';
        aiInsightsPanel.innerHTML = '<h2>🧠 AI Insights (from Gemini)</h2><p>AI-powered suggestions will appear here after a route is calculated.</p>';
        if (routeLayer) {
            map.removeLayer(routeLayer);
            routeLayer = null;
        }
        map.setView([20.5937, 78.9629], 5);
    }

    // --- Main Logic ---
    async function findRoute() {
        const source = sourceSelect.value;
        const destination = destinationSelect.value;

        if (source === destination) {
            showError("Source and destination cities cannot be the same.");
            return;
        }

        clearError();
        resetUI();
        showLoader(true);
        findRouteBtn.disabled = true;

        try {
            // Fetch route from backend
            const routeResponse = await fetch(`/api/get_shortest_route?src=${source}&dest=${destination}`);
            if (!routeResponse.ok) {
                const errorData = await routeResponse.json();
                throw new Error(errorData.error || 'Failed to find route.');
            }
            const routeData = await routeResponse.json();
            
            // Display route details and map
            displayRouteSummary(routeData);
            displayRouteOnMap(routeData);
            
            // Fetch and display AI insights
            await fetchAndDisplayAIInsights(routeData);

        } catch (error) {
            showError(error.message);
            console.error(error);
        } finally {
            showLoader(false);
            findRouteBtn.disabled = false;
        }
    }

    function displayRouteSummary(data) {
        const pathString = data.path.join(' → ');
        routeSummaryPanel.innerHTML = `
            <h2>Route Details</h2>
            <ul>
                <li><strong>From:</strong> ${data.path[0]}</li>
                <li><strong>To:</strong> ${data.path[data.path.length - 1]}</li>
                <li><strong>Total Distance:</strong> ${data.distance} km</li>
                <li><strong>Estimated Time:</strong> ${data.time_hours} hours</li>
                <li><strong>Path:</strong> ${pathString}</li>
            </ul>
        `;
    }

    function displayRouteOnMap(data) {
        if (routeLayer) {
            map.removeLayer(routeLayer);
        }
        
        const latLngs = data.path.map(city => data.coordinates[city]);
        const polyline = L.polyline(latLngs, { color: '#1a73e8', weight: 5 }).addTo(map);
        
        const markers = [];
        data.path.forEach((city, index) => {
            const coord = data.coordinates[city];
            let marker;
            if (index === 0) { // Source
                marker = L.marker(coord, { title: `${city} (Source)` }).bindPopup(`<b>Start:</b> ${city}`);
            } else if (index === data.path.length - 1) { // Destination
                marker = L.marker(coord, { title: `${city} (Destination)` }).bindPopup(`<b>End:</b> ${city}`);
            } else { // Waypoint
                marker = L.circleMarker(coord, { radius: 6, color: 'white', fillColor: '#ff7800', fillOpacity: 1, weight: 2 }).bindPopup(city);
            }
            markers.push(marker);
        });

        routeLayer = L.featureGroup([...markers, polyline]).addTo(map);
        map.fitBounds(routeLayer.getBounds().pad(0.1)); // Zoom to fit the route
    }
    
    async function fetchAndDisplayAIInsights(routeData) {
        aiInsightsPanel.innerHTML = '<h2>🧠 AI Insights (from Gemini)</h2><p>Generating insights...</p>';
        try {
            const response = await fetch('/api/get_gemini_insights', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: routeData.path, distance: routeData.distance })
            });
            const data = await response.json();

            // A simple way to format markdown-like text to HTML
            let insightsHtml = data.insights
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
                .replace(/\n/g, '<br>'); // New lines

            aiInsightsPanel.innerHTML = `<h2>🧠 AI Insights (from Gemini)</h2><div>${insightsHtml}</div>`;
        } catch (error) {
            aiInsightsPanel.innerHTML = '<h2>🧠 AI Insights (from Gemini)</h2><p>Could not retrieve AI insights.</p>';
            console.error("AI Insights Error:", error);
        }
    }

    // --- Event Listeners ---
    findRouteBtn.addEventListener('click', findRoute);

    // --- Initial Load ---
    initMap();
    fetchCities();
});