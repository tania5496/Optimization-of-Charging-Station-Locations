import rasterio
from rasterstats import zonal_stats
import contextily as ctx

def population_estimation(regions, map_with_grid, city_params):
    """
    Estimates population per region using a raster population dataset
    Returns: dict (mapping from region (grid cell) ID to estimated population count)
    """
    
    # Population count for each sector
    raster_file_population = city_params["raster_file_population"]
    with rasterio.open(raster_file_population) as data:
        affine = data.transform
        array = data.read(1)
    stats = zonal_stats(map_with_grid, raster_file_population, stats=["sum"], affine=affine)
    map_with_grid["population"] = [s["sum"] if s["sum"] is not None else 0 for s in stats]
    map_with_grid = map_with_grid.reset_index()

    # Creating dictionary: region -> population
    region_to_populatoin = dict()
    for grid_cell in range(len(map_with_grid)):
        region_id = map_with_grid.iloc[grid_cell]["index"]
        if region_id in regions:
            population = map_with_grid.iloc[grid_cell]["population"]
            region_to_populatoin[region_id] = population
    
    return region_to_populatoin