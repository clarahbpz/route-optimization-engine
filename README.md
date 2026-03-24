# Route Optimization Engine: Spatial Data & Graph Search

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](SUBSTITUA_PELO_SEU_LINK_AQUI)

---

This project is an **End-to-End Data Engineering & Intelligence Pipeline** designed to ingest, process, and optimize routes using real-world geospatial data. It compares classic search algorithms over a graph-based representation of urban infrastructure, simulating a professional routing engine environment.

## Project Objective
To demonstrate technical proficiency in **Geospatial Data Engineering**, **Graph Theory**, and **Relational Persistence (SQL)**, providing a visual and analytical comparison between optimization heuristics.

## Architecture & Data Flow
The system follows a modular architecture divided into four main layers:

1.  **Ingestion (Extract):** Python scripts consuming the **OpenStreetMap (OSM)** via the `OSMnx` library to extract the street network of *Setor Universitário, Goiânia*.
2.  **Processing (Transform):** * Conversion of raw OSM data into a **MultiDiGraph** (NetworkX).
    * Implementation of the **Haversine Formula** to calculate great-circle distances between geographic coordinates (Lat/Lon).
3.  **Intelligence (Routing):**
    * **A* (A-Star):** An informed search algorithm using distance heuristics for optimal pathfinding.
    * **BFS (Breadth-First Search):** An uninformed search focused on minimizing "hops" (intersections) regardless of physical distance.
4.  **Storage & Persistence (Load):** * **GraphML:** Persistence of the spatial network structure for fast local loading.
    * **SQLite:** Relational database logging every query execution for performance auditing and historical analysis.
5.  **Visualization (BI):** An interactive dashboard built with **Streamlit** and **Folium**, featuring real-time map rendering and a data analytics dashboard.

## Tech Stack
* **Language:** Python 3.10+
* **Geospatial Analysis:** OSMnx, Geopy
* **Graph Processing:** NetworkX
* **Data Manipulation:** Pandas, NumPy
* **Database:** SQLite 3
* **Frontend/UI:** Streamlit, Folium (Leaflet.js wrapper)

## Project Structure
```text
route-optimization-engine/
├── data/
│   ├── universitario_map.graphml 
│   └── routing_logs.db         
├── src/
│   ├── __init__.py
│   ├── data_loader.py          
│   ├── routing.py              
│   └── database.py                
├── app.py                         
├── requirements.txt      
└── README.md                    
```

## How to Run

1. Prerequisites
Ensure you have Python installed. Clone the repository and install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Download the Map Data
To ingest the latest road network data from OpenStreetMap:
    ```bash
    python src/data_loader.py
    ```

3. Initialize the Database
Set up the local SQLite environment for logging:
    ```bash
    python src/database.py
    ```

4. Launch the Engine
Run the interactive dashboard to visualize and compare routes:
    ```bash
    streamlit run app.py
    ```

## Key Insights
- A vs BFS:* The engine demonstrates that while BFS finds the path with the fewest intersections, A* consistently provides the shortest route in meters by using spatial heuristics.

- Auditability: Every route calculated is stored in the routing_logs.db, allowing for future analysis of "Most Requested Nodes" or "Average Route Distance" in the region.

**Author:** Clara Hilbert Polizel
Computer Engineering Student at Universidade Federal de Goiás (UFG) 