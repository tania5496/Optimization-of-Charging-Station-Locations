def update_particle(particle, velocity, max_ports_per_station):
    """
    Applies the velocity update to the particle, modifying the number of charging ports at each location.
    Returns: dict (updated particle)
    """
    new_particle = particle.copy()
    all_stations = velocity.keys()

    for station in all_stations:
        change = velocity[station]

        if station in new_particle.keys():
            cs_ports = new_particle[station]
        else: 
            cs_ports = 0

        new_cs_ports = max(0, min(cs_ports + change, max_ports_per_station))
        new_particle[station] = new_cs_ports

        if new_particle[station] == 0:
            new_particle.pop(station)
        
    return new_particle