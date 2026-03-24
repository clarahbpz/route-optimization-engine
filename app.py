import streamlit as st
import osmnx as ox
import folium
import streamlit.components.v1 as components
import os
import random
import pandas as pd

# Importing our custom routing engine AND database functions
from src.routing import get_route_astar, get_route_bfs, calculate_route_distance
from src.database import log_route, get_all_logs, init_db

# Page configuration
st.set_page_config(page_title="Route Optimization Engine", layout="wide")

st.title("🗺️ Route Optimization Engine")
st.markdown("Comparing Spatial Graph Search Algorithms: **A*** vs **BFS**")

@st.cache_resource 
def load_graph_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    graph_path = os.path.join(data_dir, "universitario_map.graphml")
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    init_db()

    if not os.path.exists(graph_path):
        with st.spinner("Downloading map data for Goiânia (first time only)..."):
            place_name = "Setor Universitário, Goiânia, Goiás, Brazil"
            G = ox.graph_from_place(place_name, network_type='drive')
            ox.save_graphml(G, graph_path)
            return G
    
    return ox.load_graphml(graph_path)

G = load_graph_data()

if G is None:
    st.error("Graph not found! Please run `src/data_loader.py` first.")
    st.stop()

nodes = list(G.nodes())

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Route Settings")

if 'origin' not in st.session_state:
    st.session_state.origin = random.choice(nodes)
    st.session_state.destination = random.choice(nodes)

if st.sidebar.button("Generate Random Route"):
    st.session_state.origin = random.choice(nodes)
    st.session_state.destination = random.choice(nodes)

orig_node = st.sidebar.number_input("Origin Node ID", value=st.session_state.origin, format="%d")
dest_node = st.sidebar.number_input("Destination Node ID", value=st.session_state.destination, format="%d")

# The trigger to save data to SQLite
log_button = st.sidebar.button("Calculate & Save to Database", type="primary")

# --- APP TABS ---
# This creates a professional layout separating the visual map from the data analytics
tab1, tab2 = st.tabs(["Live Map", "Data Analytics"])

# Calculate routes for both tabs
route_astar = get_route_astar(G, orig_node, dest_node)
route_bfs = get_route_bfs(G, orig_node, dest_node)

with tab1:
    col1, col2 = st.columns(2)

    # Center the map at the origin node
    center_lat = G.nodes[orig_node]['y']
    center_lon = G.nodes[orig_node]['x']
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14, tiles="cartodbpositron")

    # Plot A* Route (Blue)
    if route_astar:
        dist_astar = calculate_route_distance(G, route_astar)
        coords_astar = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route_astar]
        folium.PolyLine(coords_astar, color="#1E90FF", weight=5, opacity=0.8, tooltip="A* Route").add_to(m)
        
        with col1:
            st.info(f"**A* Algorithm** \nDistance: **{dist_astar:.2f} meters** | Intersections: {len(route_astar)}")
            
        # Log to database if button was clicked
        if log_button:
            log_route("A*", orig_node, dest_node, dist_astar, len(route_astar))

    # Plot BFS Route (Red)
    if route_bfs:
        dist_bfs = calculate_route_distance(G, route_bfs)
        coords_bfs = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in route_bfs]
        folium.PolyLine(coords_bfs, color="#FF4500", weight=5, opacity=0.6, dash_array='10', tooltip="BFS Route").add_to(m)
        
        with col2:
            st.warning(f"**BFS Algorithm** \nDistance: **{dist_bfs:.2f} meters** | Intersections: {len(route_bfs)}")
            
        # Log to database if button was clicked
        if log_button:
            log_route("BFS", orig_node, dest_node, dist_bfs, len(route_bfs))

    if log_button:
        st.sidebar.success("Data successfully saved to SQLite!")

    # Add Markers
    folium.Marker([G.nodes[orig_node]['y'], G.nodes[orig_node]['x']], popup="Origin", icon=folium.Icon(color="green", icon="play")).add_to(m)
    folium.Marker([G.nodes[dest_node]['y'], G.nodes[dest_node]['x']], popup="Destination", icon=folium.Icon(color="red", icon="stop")).add_to(m)

    # Display Map
    components.html(m._repr_html_(), height=600)

with tab2:
    st.subheader("Route Execution Logs")
    st.markdown("All queries are persisted locally in SQLite for performance analysis.")
    
    try:
        # Fetching data using our database.py function
        df_logs = get_all_logs()
        
        if not df_logs.empty:
            st.dataframe(df_logs, use_container_width=True, hide_index=True)
            
            # Simple aggregations using Pandas
            st.markdown("### Efficiency Metrics")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Queries Processed", len(df_logs))
            
            avg_astar = df_logs[df_logs['algorithm'] == 'A*']['distance_meters'].mean()
            c2.metric("Avg A* Route Distance", f"{avg_astar:.0f} m" if not pd.isna(avg_astar) else "N/A")
            
            avg_bfs = df_logs[df_logs['algorithm'] == 'BFS']['distance_meters'].mean()
            c3.metric("Avg BFS Route Distance", f"{avg_bfs:.0f} m" if not pd.isna(avg_bfs) else "N/A")
            
        else:
            st.info("No logs found yet. Go to the Live Map and click 'Save to Database' to generate data!")
    except Exception as e:
        st.error("Database connection error. Ensure routing_logs.db exists.")