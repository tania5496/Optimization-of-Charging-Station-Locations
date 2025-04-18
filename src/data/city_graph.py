import osmnx as ox
def create_graph_network(city_params):
    G = ox.graph_from_place(city_params["name"], city_params["graph_type"])
    return G