"""
Food Polar Bear - Delivery Route Optimization System
This program optimizes delivery routes for multiple riders to deliver orders from 
restaurants to customers in Grid City, minimizing total travel time while respecting 
time constraints.

Author: Data Structures Project
Course: CS2001
"""

from collections import deque, defaultdict
from typing import List, Tuple, Dict, Set
import heapq
import sys


class Graph:
    """
    Graph representation of Grid City using adjacency list.
    Supports efficient shortest path computations using BFS (since all edges have weight 1).
    """
    
    def __init__(self, grid_size: int):
        """
        Initialize the graph for an N x N grid.
        
        Args:
            grid_size: The size N of the N x N grid
        """
        self.grid_size = grid_size
        self.total_nodes = grid_size * grid_size
        self.adj_list = defaultdict(list)
        self._build_grid_graph()
    
    def _build_grid_graph(self):
        """
        Build the grid graph where each node is connected to its 4 neighbors (up, down, left, right).
        Nodes are numbered from 1 to N^2, going left to right, top to bottom.
        """
        n = self.grid_size
        
        for node in range(1, self.total_nodes + 1):
            # Convert node number to (row, col) coordinates (0-indexed)
            row = (node - 1) // n
            col = (node - 1) % n
            
            # Connect to right neighbor
            if col < n - 1:
                right_neighbor = node + 1
                self.adj_list[node].append(right_neighbor)
                self.adj_list[right_neighbor].append(node)
            
            # Connect to bottom neighbor
            if row < n - 1:
                bottom_neighbor = node + n
                self.adj_list[node].append(bottom_neighbor)
                self.adj_list[bottom_neighbor].append(node)
    
    def shortest_path_distance(self, start: int, end: int) -> int:
        """
        Calculate shortest path distance between two nodes using BFS.
        Since all edges have weight 1, BFS gives us the shortest path.
        
        Args:
            start: Starting node
            end: Ending node
            
        Returns:
            Shortest distance between start and end nodes
        """
        if start == end:
            return 0
        
        visited = set()
        queue = deque([(start, 0)])
        visited.add(start)
        
        while queue:
            current, distance = queue.popleft()
            
            for neighbor in self.adj_list[current]:
                if neighbor == end:
                    return distance + 1
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return float('inf')  # No path exists
    
    def shortest_path(self, start: int, end: int) -> List[int]:
        """
        Return the list of nodes along a shortest path from start to end (inclusive).
        Uses BFS; returns [start, ..., end] or [start] if start == end.
        
        Args:
            start: Starting node
            end: Ending node
            
        Returns:
            List of nodes from start to end (inclusive)
        """
        if start == end:
            return [start]
        
        parent = {}
        queue = deque([start])
        parent[start] = None
        
        while queue:
            current = queue.popleft()
            for neighbor in self.adj_list[current]:
                if neighbor == end:
                    parent[end] = current
                    # Reconstruct path from end to start
                    path = []
                    node = end
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]
                if neighbor not in parent:
                    parent[neighbor] = current
                    queue.append(neighbor)
        
        return []  # No path exists
    
    def get_neighbors(self, node: int) -> List[int]:
        """Get all neighbors of a given node."""
        return self.adj_list[node]


class Order:
    """Represents a delivery order with customer location and time constraint."""
    
    def __init__(self, name: str, location: int, time_limit: int):
        """
        Initialize an order.
        
        Args:
            name: Customer/order name
            location: Node location for delivery
            time_limit: Maximum time allowed for delivery
        """
        self.name = name
        self.location = location
        self.time_limit = time_limit
    
    def __repr__(self):
        return f"Order({self.name}, loc={self.location}, limit={self.time_limit})"


class Restaurant:
    """Represents a restaurant with its location and orders."""
    
    def __init__(self, name: str, location: int):
        """
        Initialize a restaurant.
        
        Args:
            name: Restaurant name
            location: Node location of the restaurant
        """
        self.name = name
        self.location = location
        self.orders = []
    
    def add_order(self, order: Order):
        """Add an order to this restaurant."""
        self.orders.append(order)
    
    def __repr__(self):
        return f"Restaurant({self.name}, loc={self.location}, orders={len(self.orders)})"


class RouteOptimizer:
    """
    Optimizes delivery routes for multiple riders.
    Uses a greedy approach with nearest neighbor heuristic and time constraint checking.
    """
    
    def __init__(self, graph: Graph, restaurants: List[Restaurant], num_riders: int):
        """
        Initialize the route optimizer.
        
        Args:
            graph: The city graph
            restaurants: List of restaurants with orders
            num_riders: Number of available riders
        """
        self.graph = graph
        self.restaurants = restaurants
        self.num_riders = num_riders
        self.routes = [[] for _ in range(num_riders)]
        self.route_times = [0] * num_riders
    
    def optimize_routes(self) -> Tuple[List[List[Tuple]], List[int]]:
        """
        Optimize delivery routes for all riders.
        
        Strategy:
        1. Collect all orders from all restaurants
        2. For each order, calculate feasibility considering time constraints
        3. Assign orders to riders using a greedy approach that minimizes total time
        4. Build efficient routes for each rider
        
        Returns:
            Tuple of (routes, route_times) where routes is a list of routes for each rider
            and route_times is the time taken by each rider
        """
        # Collect all orders with their restaurant information
        all_orders = []
        for restaurant in self.restaurants:
            for order in restaurant.orders:
                all_orders.append((restaurant, order))
        
        if not all_orders:
            return self.routes, self.route_times
        
        # Sort orders by time limit (ascending) to prioritize urgent deliveries
        all_orders.sort(key=lambda x: x[1].time_limit)
        
        # Assign orders to riders
        assigned_orders = [[] for _ in range(self.num_riders)]
        
        for restaurant, order in all_orders:
            # Find the best rider for this order (one who can complete it with minimum additional time)
            best_rider = self._find_best_rider(restaurant, order, assigned_orders)
            
            if best_rider != -1:
                assigned_orders[best_rider].append((restaurant, order))
        
        # Build optimized routes for each rider
        for rider_idx in range(self.num_riders):
            if assigned_orders[rider_idx]:
                route, time = self._build_route_for_rider(assigned_orders[rider_idx])
                self.routes[rider_idx] = route
                self.route_times[rider_idx] = time
        
        return self.routes, self.route_times
    
    def _find_best_rider(self, restaurant: Restaurant, order: Order, 
                         assigned_orders: List[List[Tuple]]) -> int:
        """
        Find the best rider to assign this order to.
        
        Args:
            restaurant: Restaurant where order originates
            order: The order to assign
            assigned_orders: Current assignment of orders to riders
            
        Returns:
            Index of best rider, or -1 if no rider can fulfill the order within time limit
        """
        best_rider = -1
        min_additional_time = float('inf')
        
        for rider_idx in range(self.num_riders):
            # Calculate time if this order is added to this rider's route
            test_orders = assigned_orders[rider_idx] + [(restaurant, order)]
            _, estimated_time = self._build_route_for_rider(test_orders)
            
            # Check if order can be delivered within time limit
            # The time limit applies from the restaurant to the customer
            time_from_restaurant = self.graph.shortest_path_distance(
                restaurant.location, order.location
            )
            
            if time_from_restaurant <= order.time_limit:
                additional_time = estimated_time - self.route_times[rider_idx]
                
                if additional_time < min_additional_time:
                    min_additional_time = additional_time
                    best_rider = rider_idx
        
        return best_rider
    
    def _build_route_for_rider(self, orders: List[Tuple[Restaurant, Order]]) -> Tuple[List[Tuple], int]:
        """
        Build an optimized route for a rider given their assigned orders.
        
        Uses a greedy nearest-neighbor approach with restaurant grouping:
        1. Group orders by restaurant
        2. Visit restaurants in an order that minimizes travel
        3. From each restaurant, deliver orders efficiently
        
        Args:
            orders: List of (restaurant, order) tuples assigned to this rider
            
        Returns:
            Tuple of (route, total_time) where route is a list of (location, name, type) tuples
        """
        if not orders:
            return [], 0
        
        # Group orders by restaurant
        restaurant_orders = defaultdict(list)
        for restaurant, order in orders:
            restaurant_orders[restaurant].append(order)
        
        route = []
        total_time = 0
        current_location = None
        
        # Visit restaurants in order that minimizes travel
        visited_restaurants = set()
        remaining_restaurants = list(restaurant_orders.keys())
        
        while remaining_restaurants:
            # Find nearest unvisited restaurant
            if current_location is None:
                # Start with first restaurant
                next_restaurant = remaining_restaurants[0]
                distance_to_restaurant = 0
            else:
                next_restaurant = min(
                    remaining_restaurants,
                    key=lambda r: self.graph.shortest_path_distance(current_location, r.location)
                )
                distance_to_restaurant = self.graph.shortest_path_distance(
                    current_location, next_restaurant.location
                )
            
            total_time += distance_to_restaurant
            current_location = next_restaurant.location
            route.append((current_location, next_restaurant.name, 'restaurant'))
            
            # Deliver orders from this restaurant using nearest neighbor
            orders_to_deliver = restaurant_orders[next_restaurant][:]
            
            while orders_to_deliver:
                # Find nearest undelivered order
                nearest_order = min(
                    orders_to_deliver,
                    key=lambda o: self.graph.shortest_path_distance(current_location, o.location)
                )
                
                distance = self.graph.shortest_path_distance(current_location, nearest_order.location)
                total_time += distance
                current_location = nearest_order.location
                route.append((current_location, nearest_order.name, 'customer'))
                
                orders_to_deliver.remove(nearest_order)
            
            remaining_restaurants.remove(next_restaurant)
            visited_restaurants.add(next_restaurant)
        
        return route, total_time
    
    def get_total_time(self) -> int:
        """Get the total time across all riders (sum of all rider times)."""
        return sum(self.route_times) if self.route_times else 0
    
    def _route_to_full_path(self, route: List[Tuple]) -> List[Tuple]:
        """
        Expand a route (list of stops) into a full path (every node).
        Each element is (node, name, type) where name is None for intermediate nodes.
        """
        if not route:
            return []
        
        full_path = []
        prev_location = None
        
        for location, name, loc_type in route:
            if prev_location is None:
                full_path.append((location, name, loc_type))
            else:
                path_nodes = self.graph.shortest_path(prev_location, location)
                for i, node in enumerate(path_nodes[1:], 1):  # skip first (same as prev)
                    if node == location:
                        full_path.append((node, name, loc_type))
                    else:
                        full_path.append((node, None, None))
            prev_location = location
        
        return full_path
    
    def print_routes(self):
        """Print formatted routes for all riders (full path: every node)."""
        for rider_idx in range(self.num_riders):
            if self.routes[rider_idx]:
                full_path = self._route_to_full_path(self.routes[rider_idx])
                path_parts = []
                for node, name, loc_type in full_path:
                    if name:
                        path_parts.append(f"{node} ({name})")
                    else:
                        path_parts.append(str(node))
                route_str = f"Rider {rider_idx + 1}: " + " -> ".join(path_parts)
                route_str += f" = {self.route_times[rider_idx]} time units"
                print(route_str)
        
        print(f"Total: {self.get_total_time()} time units")


class InputParser:
    """Handles parsing and validation of input data."""
    
    @staticmethod
    def parse_input(file_path: str) -> List[Tuple]:
        """
        Parse input file and extract test cases.
        
        Args:
            file_path: Path to input file
            
        Returns:
            List of test case tuples (grid_size, num_riders, restaurants)
        """
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f.readlines() if line.strip()]
            
            if not lines:
                raise ValueError("Input file is empty")
            
            num_test_cases = int(lines[0])
            test_cases = []
            line_idx = 1
            
            for _ in range(num_test_cases):
                if line_idx >= len(lines):
                    raise ValueError("Incomplete test case data")
                
                # Parse test case header
                parts = lines[line_idx].split()
                if len(parts) != 3:
                    raise ValueError(f"Invalid test case header at line {line_idx + 1}")
                
                grid_size = int(parts[0])
                num_riders = int(parts[1])
                num_restaurants = int(parts[2])
                line_idx += 1
                
                # Validate inputs
                if grid_size <= 0:
                    raise ValueError(f"Grid size must be positive, got {grid_size}")
                if num_riders <= 0:
                    raise ValueError(f"Number of riders must be positive, got {num_riders}")
                if num_restaurants <= 0:
                    raise ValueError(f"Number of restaurants must be positive, got {num_restaurants}")
                
                restaurants = []
                
                # Parse each restaurant
                for _ in range(num_restaurants):
                    if line_idx >= len(lines):
                        raise ValueError("Incomplete restaurant data")
                    
                    # Parse restaurant header
                    rest_parts = lines[line_idx].split()
                    if len(rest_parts) != 3:
                        raise ValueError(f"Invalid restaurant header at line {line_idx + 1}")
                    
                    rest_name = rest_parts[0]
                    rest_location = int(rest_parts[1])
                    num_orders = int(rest_parts[2])
                    line_idx += 1
                    
                    # Validate restaurant location
                    if rest_location < 1 or rest_location > grid_size * grid_size:
                        raise ValueError(f"Restaurant location {rest_location} out of grid bounds")
                    
                    restaurant = Restaurant(rest_name, rest_location)
                    
                    # Parse orders for this restaurant
                    for _ in range(num_orders):
                        if line_idx >= len(lines):
                            raise ValueError("Incomplete order data")
                        
                        order_parts = lines[line_idx].split()
                        if len(order_parts) != 3:
                            raise ValueError(f"Invalid order format at line {line_idx + 1}")
                        
                        order_name = order_parts[0]
                        order_location = int(order_parts[1])
                        time_limit = int(order_parts[2])
                        line_idx += 1
                        
                        # Validate order data
                        if order_location < 1 or order_location > grid_size * grid_size:
                            raise ValueError(f"Order location {order_location} out of grid bounds")
                        if time_limit < 0:
                            raise ValueError(f"Time limit must be non-negative, got {time_limit}")
                        
                        order = Order(order_name, order_location, time_limit)
                        restaurant.add_order(order)
                    
                    restaurants.append(restaurant)
                
                test_cases.append((grid_size, num_riders, restaurants))
            
            return test_cases
        
        except FileNotFoundError:
            print(f"Error: Input file '{file_path}' not found.")
            sys.exit(1)
        except ValueError as e:
            print(f"Error parsing input: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            sys.exit(1)


def main():
    """Main function to run the delivery route optimization."""
    
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python food_delivery_optimizer.py <input_file>")
        print("\nExample: python food_delivery_optimizer.py input.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Parse input
    print("="*60)
    print("Food Polar Bear - Delivery Route Optimization System")
    print("="*60)
    print(f"\nReading input from: {input_file}\n")
    
    test_cases = InputParser.parse_input(input_file)
    
    # Process each test case
    for case_num, (grid_size, num_riders, restaurants) in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"Test Case {case_num}")
        print(f"{'='*60}")
        print(f"Grid Size: {grid_size}x{grid_size}")
        print(f"Number of Riders: {num_riders}")
        print(f"Number of Restaurants: {len(restaurants)}")
        
        # Display restaurant information
        total_orders = sum(len(r.orders) for r in restaurants)
        print(f"Total Orders: {total_orders}\n")
        
        for restaurant in restaurants:
            print(f"  {restaurant.name} (Location: {restaurant.location})")
            for order in restaurant.orders:
                print(f"    - {order.name}: Location {order.location}, Time Limit: {order.time_limit}")
        
        # Create graph
        graph = Graph(grid_size)
        
        # Optimize routes
        print(f"\n{'-'*60}")
        print("Optimized Routes:")
        print(f"{'-'*60}")
        
        optimizer = RouteOptimizer(graph, restaurants, num_riders)
        routes, times = optimizer.optimize_routes()
        optimizer.print_routes()
        
        print(f"\n")


if __name__ == "__main__":
    main()
