from needs import water_operating_costs, power_operating_costs

# Economy initialization
_money = 1000
_resources = 1000

# Function to get the current money
def get_player_money():
    return _money

# Function to get the current resources
def get_player_resources():
    return _resources

# Function to set the current money
def set_player_money(amount):
    global _money
    _money = amount

# Function to set the current resources
def set_player_resources(amount):
    global _resources
    _resources = amount



# Costs and revenue for each zone by tier
zone_costs = {
    1: {  # Residential Zone
        1: {"money": 50, "resources": 20},   # Tier 1
        2: {"money": 100, "resources": 40},  # Tier 2
        3: {"money": 150, "resources": 60},  # Tier 3
    },
    2: {  # Industrial Zone
        1: {"money": 100, "resources": 50},   # Tier 1
        2: {"money": 200, "resources": 100},  # Tier 2
        3: {"money": 300, "resources": 150},  # Tier 3
    },
    3: {  # Road (no tiers)
        1: {"money": 20, "resources": 10}
    },
    4: {  # Power Zone
        1: {"money": 200, "resources": 100},   # Tier 1
        2: {"money": 400, "resources": 200},   # Tier 2
        3: {"money": 600, "resources": 300},   # Tier 3
    },
    5: {  # Water Zone
        1: {"money": 150, "resources": 75},   # Tier 1
        2: {"money": 300, "resources": 150},  # Tier 2
        3: {"money": 450, "resources": 225},  # Tier 3
    }
}

zone_income = {
    1: {  # Residential Zone
        1: {"money": 5, "resources": 2},   # Tier 1
        2: {"money": 10, "resources": 4},  # Tier 2
        3: {"money": 15, "resources": 6},  # Tier 3
    },
    2: {  # Industrial Zone
        1: {"money": 10, "resources": 5},   # Tier 1
        2: {"money": 20, "resources": 10},  # Tier 2
        3: {"money": 30, "resources": 15},  # Tier 3
    },
    3: {  # Road (no income)
        1: {"money": 0, "resources": 0}
    }
}



# Function to check if the player can afford a zone of a specific tier
def can_afford_zone(zone_type, tier):
    return get_player_money() >= zone_costs[zone_type][tier]["money"] and \
           get_player_resources() >= zone_costs[zone_type][tier]["resources"]



# Deduct the cost of the zone
def pay_for_zone(zone_type, tier):
    set_player_money(get_player_money() - zone_costs[zone_type][tier]["money"])
    set_player_resources(get_player_resources() - zone_costs[zone_type][tier]["resources"])



# Generate income for Residential and Industrial zones (money and resources)
def generate_income(grid):
    money = get_player_money()
    resources = get_player_resources()
    total_power_gen = 0
    total_water_gen = 0
    
    for row in grid:
        for zone_type, tier in row:
            if zone_type in zone_income:
                # Handle Residential and Industrial zones income
                if zone_type in [1, 2]:  # Residential or Industrial
                    money += zone_income[zone_type][tier]["money"]
                    resources += zone_income[zone_type][tier]["resources"]
                
                # Handle Power Plants: Deduct operational costs
                elif zone_type == 4:  # Power zone
                    total_power_gen += zone_income[zone_type][tier]["power"]
                    cost = power_operating_costs.get(tier, 0)
                    money -= cost  # Deduct operating costs for power plants
                    print(f"Power Plant Tier {tier}: Deducting {cost} money")

                # Handle Water Plants: Deduct operational costs
                elif zone_type == 5:  # Water zone
                    total_water_gen += zone_income[zone_type][tier]["water"]
                    cost = water_operating_costs.get(tier, 0)
                    money -= cost  # Deduct operating costs for water plants
                    print(f"Water Plant Tier {tier}: Deducting {cost} money")

    # Update player money and resources
    set_player_money(money)
    set_player_resources(resources)

    return total_power_gen, total_water_gen  # Return total production



# Calculate total money income from the grid
def get_money_income(grid):
    total_income = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type in zone_income:
                # Only count Residential and Industrial zones for money income
                if zone_type in [1, 2]:  # Residential or Industrial
                    total_income += zone_income[zone_type][tier]["money"]
    return total_income

# Calculate total resource income from the grid
def get_resource_income(grid):
    total_resources_income = 0
    for row in grid:
        for zone_type, tier in row:
            if zone_type in zone_income:
                # Only count Residential and Industrial zones for resource income
                if zone_type in [1, 2]:  # Residential or Industrial
                    total_resources_income += zone_income[zone_type][tier]["resources"]
    return total_resources_income



# Funkce pro zkrácení čísel na formát X.Xk, X.XM apod.
def format_number(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"  # Zobrazení v milionech
    elif value >= 10_000:
        return f"{value / 1_000:.1f}k"      # Zobrazení v deseti tisících
    else:
        return str(value)  # Zobrazení normálně, pokud je méně než 1000