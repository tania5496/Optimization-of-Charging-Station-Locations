import osmnx as ox
import numpy as np
import geopandas as gpd
from shapely.geometry import box, Point, LineString
from scipy.spatial import cKDTree

def division_into_secors(city_params):
    """
    Divides the city's geographical area into grid-based sectors using a fixed grid size.
    Returns: 
        geopandas.GeoDataFrame (the clipped grid cells within the city's boundary), 
        geopandas.GeoDataFrame (the boundary of the city)
    """
    city_boundary = ox.geocode_to_gdf(city_params["name"])

    xmin, ymin, xmax, ymax = city_boundary.total_bounds
    grid_size = 0.0125

    grid_cells = []
    for x in np.arange(xmin, xmax, grid_size):
        for y in np.arange(ymin, ymax, grid_size):
            grid_cells.append(box(x, y, x + grid_size, y + grid_size))

    grid = gpd.GeoDataFrame(geometry=grid_cells, crs=city_boundary.crs)
    map_with_grid = gpd.clip(grid, city_boundary)

    return map_with_grid, city_boundary

def nodes_to_region(G, map_with_grid):
    """
    Assigns graph nodes to spatial regions (grid cells) using a spatial join.
    If some nodes fall outside any grid cell, they are assigned to the nearest region.
    Returns:
        list of int (list of region IDs),
        dict (mapping from region ID to list of node OSM IDs within that region),
        dict (mapping from node OSM ID to its corresponding region (grid cell) ID)
    """
    nodes_gdf, edges_gdf = ox.graph_to_gdfs(G, nodes=True, edges=True)
    nodes_gdf = nodes_gdf.set_geometry(nodes_gdf.geometry)

    nodes_in_grid = gpd.sjoin(nodes_gdf, map_with_grid, how="left", predicate="within")
    nodes_in_grid = nodes_in_grid.reset_index()

    # Handling nodes that are not assigned to any grid cell. Creating node to region dictionary and region to nodes dictiionary
    assigned_nodes = nodes_in_grid.dropna(subset=["index_right"]) 
    missing_nodes = nodes_in_grid[nodes_in_grid["index_right"].isna()]

    tree = cKDTree(assigned_nodes[["x", "y"]].values)
    _, nearest_idx = tree.query(missing_nodes[["x", "y"]].values)

    nodes_in_grid.loc[nodes_in_grid["index_right"].isna(), "index_right"] = assigned_nodes.iloc[nearest_idx]["index_right"].values
    nodes_in_grid["index_right"] = nodes_in_grid["index_right"].astype(int)

    # region -> list of nodes
    region_to_nodes = nodes_in_grid.groupby(nodes_in_grid.index_right)["osmid"].apply(list).to_dict()
    # node -> region DI
    node_to_region = nodes_in_grid.set_index("osmid")["index_right"].to_dict()
    regions = [region for region in region_to_nodes]

    return regions, region_to_nodes, node_to_region


