import osmnx as ox
import networkx as nx
import os

def download_and_save_graph(place_name, filepath):
    """
    Downloads the street network graph for a specific region and saves it locally.
    """
    print(f"Fetching road network data for: {place_name}...")
    
    try:
        # Download the graph focusing only on drivable roads
        G = ox.graph_from_place(place_name, network_type='drive')
        print(f"Graph downloaded successfully! Nodes (intersections): {len(G.nodes)}, Edges (streets): {len(G.edges)}")
        
        # Save the graph to the data folder to avoid redundant downloads
        ox.save_graphml(G, filepath)
        print(f"Graph saved to: {filepath}")
        
        return G
    except Exception as e:
        print(f"Error downloading the map: {e}")
        return None

def load_graph(filepath):
    """
    Loads the locally saved graph.
    """
    print(f"Loading graph from {filepath}...")
    return ox.load_graphml(filepath)

if __name__ == "__main__":
    # Define the search region
    PLACE = "Setor Universitário, Goiânia, Goiás, Brazil"
    
    # Get the absolute path of the current file (src/data_loader.py) 
    # and go up one level to the project root dynamically
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Path where the file will be saved (exactly inside the project's data folder)
    DATA_DIR = os.path.join(BASE_DIR, "data")
    GRAPH_FILE = os.path.join(DATA_DIR, "universitario_map.graphml")
    
    # Ensure the data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Check if the map was already downloaded to save time and API requests
    if not os.path.exists(GRAPH_FILE):
        G = download_and_save_graph(PLACE, GRAPH_FILE)
    else:
        G = load_graph(GRAPH_FILE)
        print(f"Graph loaded! Nodes: {len(G.nodes)}, Edges: {len(G.edges)}")