#!/usr/bin/env python3

"""
AI-Powered Logistics Route Optimizer
Core Implementation using Dijkstra's Algorithm
Author: AI System
Date: 2025
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
            'Chennai': (13.0827, 80.2707),
            'Kolkata': (22.5726, 88.3639),
            'Hyderabad': (17.3850, 78.4867),
            'Pune': (18.5204, 73.8567),
            'Ahmedabad': (23.0225, 72.5714),
            'Jaipur': (26.9124, 75.7873),
            'Lucknow': (26.8467, 80.9462),
            'Nagpur': (21.1458, 79.0882),
            'Indore': (22.7196, 75.8577),
            'Surat': (21.1702, 72.8311),
            'Vadodara': (22.3072, 73.1812),
            'Bhopal': (23.2599, 77.4126)
        }

        # Weighted edges (bidirectional routes with distances in km)
        routes = [
            ('Mumbai', 'Pune', 150),
            ('Mumbai', 'Surat', 280),
            ('Mumbai', 'Nagpur', 820),
            ('Delhi', 'Jaipur', 280),
            ('Delhi', 'Lucknow', 550),
            ('Delhi', 'Ahmedabad', 950),
            ('Bangalore', 'Chennai', 350),
            ('Bangalore', 'Hyderabad', 575),
            ('Bangalore', 'Mumbai', 985),
            ('Chennai', 'Hyderabad', 625),
            ('Chennai', 'Bangalore', 350),
            ('Kolkata', 'Lucknow', 985),
            ('Hyderabad', 'Nagpur', 500),
            ('Hyderabad', 'Bangalore', 575),
            ('Pune', 'Hyderabad', 560),
            ('Pune', 'Nagpur', 700),
            ('Ahmedabad', 'Surat', 265),
            ('Ahmedabad', 'Indore', 420),
            ('Ahmedabad', 'Vadodara', 110),
            ('Jaipur', 'Ahmedabad', 680),
            ('Nagpur', 'Bhopal', 350),
            ('Nagpur', 'Indore', 520),
            ('Indore', 'Bhopal', 195),
            ('Surat', 'Vadodara', 140),
            ('Lucknow', 'Nagpur', 850),
        ]

        # Build adjacency list (bidirectional graph)
        for city1, city2, distance in routes:
            self._add_edge(city1, city2, distance)
            self._add_edge(city2, city1, distance)  # Bidirectional

    def _add_edge(self, from_city: str, to_city: str, distance: float):
        """Add a directed edge to the graph."""
        if from_city not in self.graph:
            self.graph[from_city] = {}
        self.graph[from_city][to_city] = distance

    def add_custom_route(self, city1: str, city2: str, distance: float, bidirectional: bool = True):
        """
        Add a custom route to the network.

        Args:
            city1: Source city
            city2: Destination city
            distance: Distance in kilometers
            bidirectional: If True, adds route in both directions
        """
        self._add_edge(city1, city2, distance)
        if bidirectional:
            self._add_edge(city2, city1, distance)
        print(f"✓ Route added: {city1} ↔ {city2} ({distance} km)")

    def add_city(self, city_name: str, lat: float = 0.0, lon: float = 0.0):
        """
        Add a new city to the network.

        Args:
            city_name: Name of the city
            lat: Latitude coordinate
            lon: Longitude coordinate
        """
        if city_name not in self.graph:
            self.graph[city_name] = {}
            self.city_coordinates[city_name] = (lat, lon)
            print(f"✓ City added: {city_name}")
        else:
            print(f"⚠ City '{city_name}' already exists in the network.")

    def dijkstra(self, source: str, destination: str) -> Tuple[Optional[List[str]], Optional[float]]:
        """
        Compute shortest path using Dijkstra's algorithm.

        Args:
            source: Starting city
            destination: Target city

        Returns:
            Tuple of (path as list of cities, total distance)
        """
        if source not in self.graph:
            print(f"❌ Source city '{source}' not found in network.")
            return None, None

        if destination not in self.graph:
            print(f"❌ Destination city '{destination}' not found in network.")
            return None, None

        # Priority queue: (distance, current_city)
        pq = [(0, source)]

        # Distance tracker: city -> minimum distance from source
        distances = {city: float('inf') for city in self.graph}
        distances[source] = 0

        # Previous city tracker for path reconstruction
        previous = {city: None for city in self.graph}

        # Visited set
        visited = set()

        while pq:
            current_dist, current_city = heapq.heappop(pq)

            # Skip if already visited
            if current_city in visited:
                continue

            visited.add(current_city)

            # Found destination
            if current_city == destination:
                break

            # Explore neighbors
            for neighbor, edge_weight in self.graph[current_city].items():
                if neighbor in visited:
                    continue

                new_dist = current_dist + edge_weight

                # Update if shorter path found
                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    previous[neighbor] = current_city
                    heapq.heappush(pq, (new_dist, neighbor))

        # Reconstruct path
        if distances[destination] == float('inf'):
            print(f"❌ No path exists between {source} and {destination}")
            return None, None

        path = []
        current = destination
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()

        return path, distances[destination]

    def calculate_estimated_time(self, distance_km: float) -> float:
        """
        Calculate estimated delivery time in hours.

        Args:
            distance_km: Distance in kilometers

        Returns:
            Estimated time in hours
        """
        return distance_km / self.avg_speed_kmh

    def display_route_details(self, path: List[str], total_distance: float):
        """
        Display detailed route information with formatting.

        Args:
            path: List of cities in the route
            total_distance: Total distance in kilometers
        """
        if not path:
            return

        estimated_time = self.calculate_estimated_time(total_distance)
        estimated_cost = total_distance * 8.5  # Rs. 8.5 per km fuel cost estimate

        print("\n" + "=" * 70)
        print("🚚 OPTIMIZED DELIVERY ROUTE")
        print("=" * 70)
        print(f"📍 Source      : {path[0]}")
        print(f"📍 Destination : {path[-1]}")
        print(f"🛣️  Route Path  : {' → '.join(path)}")
        print(f"📏 Total Distance: {total_distance:.2f} km")
        print(f"⏱️  Estimated Time: {estimated_time:.2f} hours ({estimated_time*60:.0f} minutes)")
        print(f"💰 Estimated Cost: ₹{estimated_cost:.2f}")
        print("=" * 70)

        # Step-by-step breakdown
        print("\n📋 STEP-BY-STEP ITINERARY:")
        print("-" * 70)
        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]
            segment_distance = self.graph[from_city][to_city]
            segment_time = self.calculate_estimated_time(segment_distance)
            print(f"  Step {i+1}: {from_city} → {to_city}")
            print(f"          Distance: {segment_distance:.2f} km | Time: {segment_time:.2f} hrs")
        print("-" * 70 + "\n")

    def display_city_network(self):
        """Display the complete city network graph."""
        print("\n" + "=" * 70)
        print("🗺️  LOGISTICS NETWORK - CITY CONNECTIONS")
        print("=" * 70)

        for city in sorted(self.graph.keys()):
            connections = self.graph[city]
            if connections:
                print(f"\n📍 {city}:")
                for neighbor, distance in sorted(connections.items()):
                    print(f"   → {neighbor}: {distance} km")

        print("\n" + "=" * 70)
        print(f"Total Cities: {len(self.graph)}")
        total_routes = sum(len(connections) for connections in self.graph.values()) // 2
        print(f"Total Routes: {total_routes}")
        print("=" * 70 + "\n")

    def get_all_cities(self) -> List[str]:
        """Return list of all cities in the network."""
        return sorted(self.graph.keys())

    def export_route_json(self, path: List[str], total_distance: float, filename: str = "route_export.json"):
        """
        Export route details to JSON file.

        Args:
            path: Route path
            total_distance: Total distance
            filename: Output filename
        """
        if not path:
            print("❌ No route to export.")
            return

        route_data = {
            'timestamp': datetime.now().isoformat(),
            'source': path[0],
            'destination': path[-1],
            'route_path': path,
            'total_distance_km': round(total_distance, 2),
            'estimated_time_hours': round(self.calculate_estimated_time(total_distance), 2),
            'estimated_cost_inr': round(total_distance * 8.5, 2),
            'segments': []
        }

        for i in range(len(path) - 1):
            from_city = path[i]
            to_city = path[i + 1]
            segment_distance = self.graph[from_city][to_city]
            route_data['segments'].append({
                'from': from_city,
                'to': to_city,
                'distance_km': segment_distance,
                'time_hours': round(self.calculate_estimated_time(segment_distance), 2)
            })

        try:
            with open(filename, 'w') as f:
                json.dump(route_data, f, indent=2)
            print(f"✓ Route exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting route: {e}")


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 70)
    print("🤖 AI-POWERED LOGISTICS ROUTE OPTIMIZER")
    print("=" * 70)
    print("1. 📍 Add New City")
    print("2. 🛣️  Add New Route")
    print("3. 🗺️  View City Network Graph")
    print("4. 🔍 Find Shortest Path")
    print("5. 📋 List All Cities")
    print("6. 📤 Export Last Route (JSON)")
    print("7. 🚪 Exit Program")
    print("=" * 70)


def main():
    """Main program execution."""
    optimizer = LogisticsRouteOptimizer()
    last_route = None
    last_distance = None

    print("\n" + "🚀" * 35)
    print("   Welcome to AI-Powered Logistics Route Optimizer")
    print("   Optimizing delivery routes across Indian cities")
    print("🚀" * 35)

    while True:
        display_menu()
        choice = input("\n👉 Enter your choice (1-7): ").strip()

        if choice == '1':
            # Add new city
            print("\n➕ ADD NEW CITY")
            city_name = input("Enter city name: ").strip()
            try:
                lat = float(input("Enter latitude (optional, press Enter for 0.0): ").strip() or "0.0")
                lon = float(input("Enter longitude (optional, press Enter for 0.0): ").strip() or "0.0")
                optimizer.add_city(city_name, lat, lon)
            except ValueError:
                print("❌ Invalid coordinates. City not added.")

        elif choice == '2':
            # Add new route
            print("\n➕ ADD NEW ROUTE")
            city1 = input("Enter first city: ").strip()
            city2 = input("Enter second city: ").strip()
            try:
                distance = float(input("Enter distance (km): ").strip())
                optimizer.add_custom_route(city1, city2, distance)
            except ValueError:
                print("❌ Invalid distance. Route not added.")

        elif choice == '3':
            # View network
            optimizer.display_city_network()

        elif choice == '4':
            # Find shortest path
            print("\n🔍 FIND SHORTEST PATH")
            print("Available cities:", ", ".join(optimizer.get_all_cities()))
            source = input("\nEnter source city: ").strip().title()
            destination = input("Enter destination city: ").strip().title()

            print("\n⚙️  Computing optimal route using Dijkstra's algorithm...")
            path, distance = optimizer.dijkstra(source, destination)

            if path and distance:
                optimizer.display_route_details(path, distance)
                last_route = path
                last_distance = distance

        elif choice == '5':
            # List all cities
            cities = optimizer.get_all_cities()
            print("\n📋 ALL CITIES IN NETWORK:")
            print("-" * 70)
            for i, city in enumerate(cities, 1):
                print(f"  {i}. {city}")
            print("-" * 70)
            print(f"Total: {len(cities)} cities\n")

        elif choice == '6':
            # Export route
            if last_route and last_distance:
                filename = input("Enter filename (default: route_export.json): ").strip() or "route_export.json"
                optimizer.export_route_json(last_route, last_distance, filename)
            else:
                print("❌ No route to export. Please find a route first (Option 4).")

        elif choice == '7':
            # Exit
            print("\n" + "=" * 70)
            print("👋 Thank you for using AI-Powered Logistics Route Optimizer!")
            print("   Safe travels and optimized routes!")
            print("=" * 70 + "\n")
            break

        else:
            print("❌ Invalid choice. Please select 1-7.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()