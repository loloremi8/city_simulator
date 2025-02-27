from needs import water_operating_costs, power_operating_costs

# Economy initialization
_money = 10000
_resources = 10000

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
    },
    6: {  # Powe lines
        1: {"money": 10, "resources": 5}
    },
    7: {  # Pipe lines
        1: {"money": 8, "resources": 4}
    }
}

# Add costs for power lines and water pipes
infrastructure_costs = {
    'power_line': {"money": 10, "resources": 5},  # Cost to place a power line
    'water_pipe': {"money": 8, "resources": 4}   # Cost to place a water pipe
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
    },
    4: {  # Power Zone
        1: {"generation": 20},  # Tier 1
        2: {"generation": 50},  # Tier 2
        3: {"generation": 100}  # Tier 3
    },
    5: {  # Water Zone
        1: {"generation": 20},  # Tier 1
        2: {"generation": 50},  # Tier 2
        3: {"generation": 100}  # Tier 3
    }
}

zones_placed = {
    1: 0,  # Residential Zones placed
    2: 0,  # Industrial Zones placed
    3: 0,  # Roads placed
    4: 0,  # Power plants placed
    5: 0,  # Water plants placed
    6: 0,  # Power lines placed
    7: 0,  # Water lines placed
}

inflation_rate = 0.05  # 5% cost increase per zone placed



def get_dynamic_zone_cost(zone_type, tier=None):
    # Get the base costs of the zone (money and resources)
    if zone_type in infrastructure_costs:
        base_money_cost = infrastructure_costs[zone_type]["money"]  # Infrastructure only has money cost
        base_resource_cost = infrastructure_costs[zone_type]["resources"]
    else:
        base_money_cost = zone_costs[zone_type][tier]["money"]
        base_resource_cost = zone_costs[zone_type][tier]["resources"]
    
    # Calculate the inflation factor based on how many zones of this type have been placed
    inflation_factor = 1 + (inflation_rate * zones_placed.get(zone_type, 0))
    
    # Apply inflation to both money and resource costs
    dynamic_money_cost = int(base_money_cost * inflation_factor)
    dynamic_resource_cost = int(base_resource_cost * inflation_factor)
    
    return dynamic_money_cost, dynamic_resource_cost



def get_dynamic_zone_price(zone_type, tier=None):
    # Get dynamic money and resource costs based on inflation
    dynamic_money_cost, dynamic_resource_cost = get_dynamic_zone_cost(zone_type, tier)

    # Get resource cost
    if zone_type in infrastructure_costs:
        resource_cost = infrastructure_costs[zone_type]["resources"]
    else:
        resource_cost = zone_costs[zone_type][tier]["resources"]

    return dynamic_money_cost, dynamic_resource_cost



# Function to check if the player can afford a zone of a specific tier
def can_afford_zone(zone_type, tier=None):
    # Get dynamic costs based on inflation (money and resources)
    dynamic_money_cost, dynamic_resource_cost = get_dynamic_zone_cost(zone_type, tier)

    # Check if it's a zone or infrastructure for resources
    if zone_type in infrastructure_costs:
        resource_cost = infrastructure_costs[zone_type]["resources"]
    else:
        resource_cost = zone_costs[zone_type][tier]["resources"]
    
    # Check if the player has enough money and resources
    return get_player_money() >= dynamic_money_cost and get_player_resources() >= dynamic_resource_cost



# Deduct the cost of the zone
def pay_for_zone(zone_type, tier=None):
    # Get dynamic costs based on inflation (money and resources)
    dynamic_money_cost, dynamic_resource_cost = get_dynamic_zone_cost(zone_type, tier)
    
    # Deduct money from the player
    set_player_money(get_player_money() - dynamic_money_cost)
    # Deduct resources from the player
    set_player_resources(get_player_resources() - dynamic_resource_cost)

    # Deduct resources
    if zone_type in infrastructure_costs:
        resource_cost = infrastructure_costs[zone_type]["resources"]
    else:
        resource_cost = zone_costs[zone_type][tier]["resources"]
    set_player_resources(get_player_resources() - resource_cost)

    # Increment the number of zones placed for inflation tracking
    if zone_type in zones_placed:
        zones_placed[zone_type] += 1



# Generate income for Residential and Industrial zones (money and resources)
def generate_income(above_ground_level):
    money = get_player_money()
    resources = get_player_resources()
    total_power_gen = 0
    total_water_gen = 0

    # Helper function for operational cost deduction
    def deduct_cost(zone_type, tier, money):
        if zone_type == 4:  # Power zone
            cost = power_operating_costs.get(tier, 0)
            money -= cost
        elif zone_type == 5:  # Water zone
            cost = water_operating_costs.get(tier, 0)
            money -= cost
        return money

    # Loop through the above_ground_level and calculate income
    for row in above_ground_level:
        for zone_type, tier in row:
            if zone_type in [1, 2]:  # Residential or Industrial zones
                money += zone_income[zone_type][tier]["money"]
                resources += zone_income[zone_type][tier]["resources"]
            elif zone_type == 4:  # Power zone
                total_power_gen += zone_income[zone_type][tier]["generation"]
            elif zone_type == 5:  # Water zone
                total_water_gen += zone_income[zone_type][tier]["generation"]

            # Deduct operational cost for power/water zones
            if zone_type in [4, 5]:
                money = deduct_cost(zone_type, tier, money)

    # Update player money and resources
    set_player_money(money)
    set_player_resources(resources)

    return total_power_gen, total_water_gen  # Return total production



# Function to deduct operational costs for power and water zones
def deduct_operational_costs(above_ground_level):
    money = get_player_money()  # Get current money

    for row in above_ground_level:
        for zone_type, tier in row:
            # Handle operational costs for power plants
            if zone_type == 4:  # Power zone
                cost = power_operating_costs.get(tier, 0)
                money -= cost  # Deduct operating cost for power plant

            # Handle operational costs for water plants
            elif zone_type == 5:  # Water zone
                cost = water_operating_costs.get(tier, 0)
                money -= cost  # Deduct operating cost for water plant

    # Update player money
    set_player_money(money)



# Calculate total money income from the grid
def get_money_income(above_ground_level):
    total_income = 0
    for row in above_ground_level:
        for zone_type, tier in row:
            if zone_type in zone_income:
                # Only count Residential and Industrial zones for money income
                if zone_type in [1, 2]:  # Residential or Industrial
                    total_income += zone_income[zone_type][tier]["money"]
    return total_income

# Calculate total resource income from the grid
def get_resource_income(above_ground_level):
    total_resources_income = 0
    for row in above_ground_level:
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