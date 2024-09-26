# Power and Water Generation and Needs
power_generation = {
    4: {  # Power Zone
        1: {"generation": 20},  # Tier 1
        2: {"generation": 50},  # Tier 2
        3: {"generation": 100}  # Tier 3
    }
}

water_generation = {
    5: {  # Water Zone
        1: {"generation": 20},  # Tier 1
        2: {"generation": 50},  # Tier 2
        3: {"generation": 100}  # Tier 3
    }
}

# Power and water needs per Residential and Industrial zone
zone_power_water_needs = {
    1: {  # Residential Zone
        1: {"power": 5, "water": 5},    # Tier 1
        2: {"power": 10, "water": 10},  # Tier 2
        3: {"power": 15, "water": 15}   # Tier 3
    },
    2: {  # Industrial Zone
        1: {"power": 10, "water": 10},  # Tier 1
        2: {"power": 20, "water": 20},  # Tier 2
        3: {"power": 30, "water": 30}   # Tier 3
    }
}



# Operational Costs for Power and Water Plants
power_operating_costs = {
    1: 50,  # Tier 1 power plant costs 50 money per cycle
    2: 100,  # Tier 2 power plant costs 100 money per cycle
    3: 150  # Tier 3 power plant costs 150 money per cycle
}

water_operating_costs = {
    1: 40,  # Tier 1 water station costs 40 money per cycle
    2: 80,  # Tier 2 water station costs 80 money per cycle
    3: 120  # Tier 3 water station costs 120 money per cycle
}



# Calculate total power generation
def get_total_power_generation(grid):
    total_power = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type == 4:  # Power zones
                total_power += power_generation[zone_type][tier]["generation"]
    return total_power



# Calculate total water generation
def get_total_water_generation(grid):
    total_water = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type == 5:  # Water zones
                total_water += water_generation[zone_type][tier]["generation"]
    return total_water



# Calculate total power needs (Residential and Industrial Zones)
def get_total_power_needs(grid):
    total_power_needs = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type in zone_power_water_needs:
                total_power_needs += zone_power_water_needs[zone_type][tier]["power"]
    return total_power_needs



# Calculate total water needs (Residential and Industrial Zones)
def get_total_water_needs(grid):
    total_water_needs = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type in zone_power_water_needs:
                total_water_needs += zone_power_water_needs[zone_type][tier]["water"]
    return total_water_needs