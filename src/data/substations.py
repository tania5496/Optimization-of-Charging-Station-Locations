import osmnx as ox
import geopy.distance

def find_substations(city_name):
    """
    Retrieves power substations within a given city boundary using OSM data.
    Returns: geopandas.GeoDataFrame (contains the geometries of electrical substations)
    """
    substations = ox.features_from_place(city_name, tags={"power": "substation"})
    substations = substations[['geometry']].reset_index()
    return substations

def calculate_distance_to_substation(G, substations):
    """
    Calculates the geodesic distance from each node in the graph to the nearest power substation.
    Returns: dict (mapping from node OSM ID to its geodesic distance (in meters) to the nearest substation)
    """
    dist_to_substation = dict()
    for node in G.nodes():
        node_lat, node_lon = G.nodes[node]['y'], G.nodes[node]['x']
        distances = []
        for _, row in substations.iterrows():
            if row.geometry.geom_type == "Point":
                substation_lat, substation_lon = row.geometry.y, row.geometry.x
                distance_m = geopy.distance.geodesic((node_lat, node_lon), (substation_lat, substation_lon)).m
                distances.append(distance_m)
        dist_to_substation[node] = min(distances)
    return dist_to_substation