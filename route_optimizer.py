#!/usr/bin/env python3
"""
AI-Powered Logistics Route Optimizer
Core Implementation using Dijkstra's Algorithm
"""

import heapq
import json
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class LogisticsRouteOptimizer:
    """
    Graph-based route optimization system for Indian cities logistics network.
    Uses Dijkstra's algorithm for shortest path computation.
    """
    
    def __init__(self):
        """Initialize the logistics network graph."""
        self.graph: Dict[str, Dict[str, float]] = {}
        self.city_coordinates: Dict[str, Tuple[float, float]] = {}
        self.avg_speed_kmh = 60  # Average delivery vehicle speed
        self._initialize_indian_cities_network()
    
    def _initialize_indian_cities_network(self):
        """
        Initialize graph with major Indian cities and realistic distances.
        Graph structure: {city: {neighbor: distance_km, ...}, ...}
        """
        # City coordinates (lat, lon) for map visualization
        self.city_coordinates = {
    'Mumbai': (19.0760, 72.8777),
    'Delhi': (28.7041, 77.1025),
    'Bangalore': (12.9716, 77.5946),
    'Hyderabad': (17.3850, 78.4867),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Pune': (18.5204, 73.8567),
    'Ahmedabad': (23.0225, 72.5714),
    'Jaipur': (26.9124, 75.7873),
    'Surat': (21.1702, 72.8311),
    'Lucknow': (26.8467, 80.9462),
    'Kanpur': (26.4499, 80.3319),
    'Nagpur': (21.1458, 79.0882),
    'Indore': (22.7196, 75.8577),
    'Bhopal': (23.2599, 77.4126),
    'Gwalior': (26.2183, 78.1828),
    'Visakhapatnam': (17.6868, 83.2185),
    'Patna': (25.5941, 85.1376),
    'Vadodara': (22.3072, 73.1812),
    'Ghaziabad': (28.6692, 77.4538),
    'Agra': (27.1767, 78.0081)
}
        
        
        # Network connections with distances (in kilometers)
        # Format: {city: {neighbor_city: distance_km}}
        self.graph = {
            'Mumbai': {
                'Pune': 150,
                'Surat': 280,
                'Nashik': 167,
                'Nagpur': 820,
                'Indore': 590
            },
            'Delhi': {
                'Jaipur': 280,
                'Agra': 230,
                'Lucknow': 550,
                'Chandigarh': 244,
                'Ghaziabad': 20
            },
            'Bangalore': {
                'Chennai': 350,
                'Hyderabad': 570,
                'Mysore': 145,
                'Pune': 840
            },
            'Hyderabad': {
                'Bangalore': 570,
                'Chennai': 630,
                'Nagpur': 500,
                'Visakhapatnam': 620
            },
            'Chennai': {
                'Bangalore': 350,
                'Hyderabad': 630,
                'Coimbatore': 500
            },
            'Kolkata': {
                'Patna': 590,
                'Bhubaneswar': 440,
                'Asansol': 210
            },
            'Pune': {
                'Mumbai': 150,
                'Bangalore': 840,
                'Hyderabad': 560,
                'Nashik': 210
            },
            'Ahmedabad': {
                'Surat': 265,
                'Vadodara': 110,
                'Rajkot': 220,
                'Indore': 420
            },
            'Jaipur': {
                'Delhi': 280,
                'Agra': 240,
                'Udaipur': 400,
                'Ajmer': 135
            },
            'Surat': {
                'Mumbai': 280,
                'Ahmedabad': 265,
                'Vadodara': 150
            },
            'Lucknow': {
                'Delhi': 550,
                'Kanpur': 85,
                'Agra': 330,
                'Patna': 540
            },
            'Kanpur': {
                'Lucknow': 85,
                'Agra': 300,
                'Allahabad': 200
            },
            'Nagpur': {
                'Mumbai': 820,
                'Hyderabad': 500,
                'Bhopal': 350,
                'Raipur': 290
            },
            'Indore': {
                'Mumbai': 590,
                'Bhopal': 195,
                'Ahmedabad': 420,
                'Ujjain': 55
            },
            'Bhopal': {
                'Indore': 195,
                'Nagpur': 350,
                'Gwalior': 420
            },
            'Visakhapatnam': {
                'Hyderabad': 620,
                'Vijayawada': 350
            },
            'Patna': {
                'Kolkata': 590,
                'Lucknow': 540,
                'Gaya': 100
            },
            'Vadodara': {
                'Ahmedabad': 110,
                'Surat': 150
            },
            'Ghaziabad': {
                'Delhi': 20,
                'Meerut': 70
            },
            'Agra': {
                'Delhi': 230,
                'Jaipur': 240,
                'Lucknow': 330,
                'Kanpur': 300,
                'Gwalior': 120
            }
        }
        
        # Make graph bidirectional
        self._make_graph_bidirectional()
    
    def _make_graph_bidirectional(self):
        """Ensure all edges in the graph are bidirectional."""
        for city in list(self.graph.keys()):
            for neighbor, distance in list(self.graph[city].items()):
                if neighbor not in self.graph:
                    self.graph[neighbor] = {}
                if city not in self.graph[neighbor]:
                    self.graph[neighbor][city] = distance
    
    def get_all_cities(self) -> List[str]:
        """Returns a list of all cities in the network."""
        return sorted(list(self.graph.keys()))
    
    def dijkstra(self, start: str, end: str) -> Tuple[Optional[List[str]], Optional[float]]:
        """
        Find shortest path between two cities using Dijkstra's algorithm.
        
        Args:
            start: Starting city name
            end: Destination city name
            
        Returns:
            Tuple of (path_list, total_distance) or (None, None) if no path exists
        """
        if start not in self.graph or end not in self.graph:
            return None, None
        
        # Priority queue: (distance, current_city, path)
        pq = [(0, start, [start])]
        visited = set()
        
        while pq:
            current_dist, current_city, path = heapq.heappop(pq)
            
            if current_city in visited:
                continue
            
            visited.add(current_city)
            
            # Destination reached
            if current_city == end:
                return path, current_dist
            
            # Explore neighbors
            for neighbor, distance in self.graph.get(current_city, {}).items():
                if neighbor not in visited:
                    new_dist = current_dist + distance
                    new_path = path + [neighbor]
                    heapq.heappush(pq, (new_dist, neighbor, new_path))
        
        return None, None
    
    def calculate_estimated_time(self, distance_km: float) -> float:
        """
        Calculate estimated travel time in hours.
        
        Args:
            distance_km: Total distance in kilometers
            
        Returns:
            Estimated time in hours
        """
        return distance_km / self.avg_speed_kmh
    
    def get_route_details(self, start: str, end: str) -> Dict:
        """
        Get comprehensive route details including path, distance, and time.
        
        Args:
            start: Starting city
            end: Destination city
            
        Returns:
            Dictionary with route information
        """
        path, distance = self.dijkstra(start, end)
        
        if path and distance:
            estimated_time = self.calculate_estimated_time(distance)
            return {
                'path': path,
                'distance_km': round(distance, 2),
                'estimated_time_hours': round(estimated_time, 2),
                'coordinates': {
                    city: self.city_coordinates.get(city) 
                    for city in path
                }
            }
        
        return {
            'error': f'No route found between {start} and {end}'
        }
    
    def find_alternative_routes(self, start: str, end: str, max_routes: int = 3) -> List[Dict]:
        """
        Find multiple alternative routes between cities.
        
        Args:
            start: Starting city
            end: Destination city
            max_routes: Maximum number of alternative routes to find
            
        Returns:
            List of route dictionaries
        """
        routes = []
        visited_paths = set()
        
        # This is a simplified version - for production, implement k-shortest paths
        main_path, main_distance = self.dijkstra(start, end)
        
        if main_path and main_distance:
            routes.append({
                'path': main_path,
                'distance_km': round(main_distance, 2),
                'estimated_time_hours': round(self.calculate_estimated_time(main_distance), 2)
            })
        
        return routes

# Example usage
if __name__ == "__main__":
    optimizer = LogisticsRouteOptimizer()
    
    print("Available cities:", optimizer.get_all_cities())
    print("\n" + "="*50)
    
    # Test route
    start_city = "Mumbai"
    end_city = "Delhi"
    
    print(f"\nFinding route from {start_city} to {end_city}...")
    route_details = optimizer.get_route_details(start_city, end_city)
    
    if 'error' not in route_details:
        print(f"\nOptimal Route: {' -> '.join(route_details['path'])}")
        print(f"Total Distance: {route_details['distance_km']} km")
        print(f"Estimated Time: {route_details['estimated_time_hours']} hours")
    else:
        print(route_details['error'])
