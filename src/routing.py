import networkx as nx
import math
import os
import osmnx as ox
import random

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points 
    on the Earth's surface using the Haversine formula.
    """
    R = 6371000  # Radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0)**2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0)**2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def astar_heuristic(node1, node2, G):
    """
    Heuristic function for A* Search.
    Estimates the distance from node1 to node2 using Haversine.
    """
    n1 = G.nodes[node1]
    n2 = G.nodes[node2]
    return haversine_distance(n1['y'], n1['x'], n2['y'], n2['x'])

def get_route_astar(G, origin_node, destination_node, weight='length'):
    """
    Finds the shortest path using the A* algorithm based on physical distance.
    """
    try:
        route = nx.astar_path(
            G, 
            origin_node, 
            destination_node, 
            heuristic=lambda u, v: astar_heuristic(u, v, G), 
            weight=weight
        )
        return route
    except nx.NetworkXNoPath:
        print("No path found between the selected nodes.")
        return None

def get_route_bfs(G, origin_node, destination_node):
    """
    Finds a path using Breadth-First Search (BFS).
    Note: BFS finds the path with the fewest edges (intersections), not necessarily the shortest physical distance.
    """
    try:
        route = nx.shortest_path(G, origin_node, destination_node, weight=None)
        return route
    except nx.NetworkXNoPath:
        print("No path found between the selected nodes.")
        return None

def calculate_route_distance(G, route):
    """
    Calculates the total physical length of a given route.
    """
    distance = 0.0
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i+1]
        # OSMnx graphs are MultiDiGraphs, meaning there can be multiple parallel edges between two nodes.
        # We get all edges between u and v, and pick the shortest one.
        edge_data = G.get_edge_data(u, v)
        min_length = min([data.get('length', 0) for data in edge_data.values()])
        distance += min_length
    return distance

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    GRAPH_FILE = os.path.join(BASE_DIR, "data", "universitario_map.graphml")
    
    if not os.path.exists(GRAPH_FILE):
        print("Graph file not found! Please run data_loader.py first.")
    else:
        print("Loading graph for routing tests...")
        G = ox.load_graphml(GRAPH_FILE)
        
        nodes = list(G.nodes())
        origin = random.choice(nodes)
        destination = random.choice(nodes)
        
        print(f"\nCalculating routes from Node ID {origin} to Node ID {destination}...\n")
        
        # Test A* Route
        route_astar = get_route_astar(G, origin, destination)
        if route_astar:
            distance_astar = calculate_route_distance(G, route_astar)
            print(f"✅ A* Route found! Passes through {len(route_astar)} intersections. Distance: {distance_astar:.2f} meters.")
            
        # Test BFS Route
        route_bfs = get_route_bfs(G, origin, destination)
        if route_bfs:
            distance_bfs = calculate_route_distance(G, route_bfs)
            print(f"✅ BFS Route found! Passes through {len(route_bfs)} intersections. Distance: {distance_bfs:.2f} meters.")