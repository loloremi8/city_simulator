import pygame
from connectivity import is_zone_connected
from economy import get_money_income, get_resource_income, format_number, get_dynamic_zone_price
from needs import get_total_power_generation, get_total_water_generation, get_total_power_needs, get_total_water_needs, water_operating_costs, power_operating_costs
from bank import get_loan_status



def draw_icon(screen, icon_path, x, y):
    # Load the image from the given path
    icon = pygame.image.load(icon_path).convert_alpha()  # Make sure it has an alpha channel for transparency
    icon = pygame.transform.scale(icon, (30, 30))  # Resize the icon if needed (adjust size as per your UI)
    screen.blit(icon, (x, y))  # Draw the icon on the screen



# Draw the compact UI with icons for money, resources, and income
def draw_ui(screen, money, resources, selected_zone, selected_tiers, font, ui_height, above_ground_level, underground_level, grid_size):
    # Set a box background for the row UI
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, screen.get_width(), ui_height))

    # Adjusted spacing for icons and tiers
    start_x = 10  # Initial x position for icons

    # Money Icon and Value (including income)
    money_income = get_money_income(above_ground_level)  # Use both layers
    draw_icon(screen, "icons/money.png", start_x, 6)  # Money icon
    money_text = font.render(f"{format_number(money)} (+{format_number(money_income)})", True, (255, 255, 255))
    screen.blit(money_text, (start_x + 40, 10))  # Moved text a bit farther from the icon

    # Resources Icon and Value (including income)
    resource_income = get_resource_income(above_ground_level)  # Use both layers
    draw_icon(screen, "icons/resources.png", start_x + 210, 6)  # Resources icon
    resources_text = font.render(f"{format_number(resources)} (+{format_number(resource_income)})", True, (255, 255, 255))
    screen.blit(resources_text, (start_x + 210 + 40, 10))  # Moved text a bit farther from the icon

    # Residential Icon and Tier (House, green for selected)
    draw_icon(screen, "icons/house.png", start_x + 420, 6)  # House icon for Residential
    res_zone_text = font.render(f"T{selected_tiers[0]}", True, (0, 255, 0) if selected_zone == 1 else (255, 255, 255))  # Green for selected
    screen.blit(res_zone_text, (start_x + 420 + 40, 10))  # Adjusted text spacing

    # Industrial Icon and Tier (Factory, gray for selected)
    draw_icon(screen, "icons/factory.png", start_x + 510, 6)  # Factory icon for Industrial
    ind_zone_text = font.render(f"T{selected_tiers[1]}", True, (128, 128, 128) if selected_zone == 2 else (255, 255, 255))  # Gray for selected
    screen.blit(ind_zone_text, (start_x + 510 + 40, 10))  # Adjusted text spacing

    # Road Icon (No tiers, with "R" to indicate selection, spaced more)
    draw_icon(screen, "icons/road.png", start_x + 600, 6)  # Road icon
    road_zone_text = font.render("R", True, (255, 0, 0) if selected_zone == 3 else (255, 255, 255))  # Red "R" if road is selected
    screen.blit(road_zone_text, (start_x + 600 + 40, 10))  # Adjusted text spacing

    # Power Icon and Tier (use yellow for selected)
    draw_icon(screen, "icons/power.png", start_x + 690, 6)  # Power icon
    power_zone_text = font.render(f"T{selected_tiers[3]}", True, (255, 255, 0) if selected_zone == 4 else (255, 255, 255))  # Yellow for Power if selected
    screen.blit(power_zone_text, (start_x + 690 + 40 + 5, 10))  # Show power zone tier

    # Water Icon and Tier (use blue for selected)
    draw_icon(screen, "icons/water.png", start_x + 780, 6)  # Water icon
    water_zone_text = font.render(f"T{selected_tiers[4]}", True, (0, 0, 255) if selected_zone == 5 else (255, 255, 255))  # Blue for Water if selected
    screen.blit(water_zone_text, (start_x + 780 + 40 + 5, 10))  # Show water zone tier

    # Power lines
    draw_icon(screen, "icons/power_lines.png", start_x + 880, 6)  # Power line icon
    power_line_text = font.render(f"P", True, (255, 255, 0) if selected_zone == 6 else (255, 255, 255))  # Yellow "P" if power lines are selected
    screen.blit(power_line_text, (start_x + 880 + 40 + 5, 10))  # Show power lines text

    # Pipe lines
    draw_icon(screen, "icons/pipe_lines.png", start_x + 970, 6)  # Pipe line icon
    pipe_line_text = font.render(f"P", True, (0, 0, 255) if selected_zone == 7 else (255, 255, 255))  # Blue "P" if pipe lines are selected
    screen.blit(pipe_line_text, (start_x + 970 + 40 + 5, 10))  # Show pipe line text

    # Get dynamic price for the selected zone and tier
    dynamic_money_cost, resource_cost = get_dynamic_zone_price(selected_zone, selected_tiers[selected_zone - 1])
    # Display the cost in the middle underneath the zone icons
    cost_text = font.render(f"Cost: {dynamic_money_cost} money, {resource_cost} resources", True, (255, 255, 255))
    # Display the cost text
    screen.blit(cost_text, (500, 50))

    # Check if total generation meets total needs (resource shortage check)
    total_power_gen = get_total_power_generation(above_ground_level)  # Use above ground layer for power plants
    total_power_need = get_total_power_needs(above_ground_level, underground_level, grid_size)
    total_water_gen = get_total_water_generation(above_ground_level)  # Use above ground layer for water plants
    total_water_need = get_total_water_needs(above_ground_level, underground_level, grid_size)

    # Display warnings if there's a resource shortage (generation < needs)
    if total_power_gen < total_power_need:
        draw_icon(screen, "icons/warning.png", start_x + 690 + 20, 6)  # Warning icon for power shortage
        # print(f"Power generation shortfall: {total_power_gen} generated, {total_power_need} needed") # Debuging

    if total_water_gen < total_water_need:
        draw_icon(screen, "icons/warning.png", start_x + 780 + 20, 6)  # Warning icon for water shortage
        # print(f"Water generation shortfall: {total_water_gen} generated, {total_water_need} needed") # Debuging

    # Check for connection status for each zone (whether they are connected to power and water)
    for row in range(grid_size):
        for col in range(grid_size):
            zone_type, tier = above_ground_level[row][col]
            if zone_type == 1 or zone_type == 2:  # Residential or Industrial zones
                connected_to_power = is_zone_connected(above_ground_level, underground_level, row, col, 'power', grid_size)
                connected_to_water = is_zone_connected(above_ground_level, underground_level, row, col, 'water', grid_size)

                # Show warning icons if not connected to power or water
                if not connected_to_power:
                    draw_icon(screen, "icons/warning.png", start_x + 690 + 20, 6)  # Warning icon for power connection issue
                    # print(f"Zone at ({row}, {col}) is NOT connected to power") # Debuging

                if not connected_to_water:
                    draw_icon(screen, "icons/warning.png", start_x + 780 + 20, 6)  # Warning icon for water connection issue
                    # print(f"Zone at ({row}, {col}) is NOT connected to water") # Debuging



# Cycle through zone tiers using keys
def handle_zone_selection(event, selected_zone, selected_tiers, is_undergroung_mode):
    # Handle zone selection
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            selected_zone = 1  # Residential zone
            is_undergroung_mode = False
        elif event.key == pygame.K_2:
            selected_zone = 2  # Industrial zone
            is_undergroung_mode = False
        elif event.key == pygame.K_3:
            selected_zone = 3  # Road (no tier changes)
            is_undergroung_mode = False
        elif event.key == pygame.K_4:
            selected_zone = 4  # Power
            is_undergroung_mode = False
        elif event.key == pygame.K_5:
            selected_zone = 5  # Water
            is_undergroung_mode = False
        elif event.key == pygame.K_6:
            selected_zone = 6  # Power lines
            is_undergroung_mode = True
        elif event.key == pygame.K_7:
            selected_zone = 7  # Pipe lines
            is_undergroung_mode = True

        # Handle tier cycling for Residential and Industrial zones (using up/down arrow keys)
        if selected_zone in [1, 2, 4, 5]:  # Only allow tier changes for Residential (1), Industrial (2), Water (4) and Power (5)
            index = selected_zone - 1
            if event.key == pygame.K_UP:  # Increase tier for the selected zone
                selected_tiers[selected_zone - 1] = min(selected_tiers[selected_zone - 1] + 1, 3)  # Max 3 tiers
            elif event.key == pygame.K_DOWN:  # Decrease tier for the selected zone
                selected_tiers[selected_zone - 1] = max(selected_tiers[selected_zone - 1] - 1, 1)  # Min 1 tier
    
    return selected_zone, selected_tiers, is_undergroung_mode



# Statistics window remains unchanged from before
def draw_statistics_ui(screen, font, ui_height, above_ground_level, underground_level, grid_size):
    width, height = screen.get_size()

    # Create a semi-transparent overlay for the statistics window
    stats_background = pygame.Surface((width, height - ui_height))
    stats_background.set_alpha(200)  # Semi-transparent
    stats_background.fill((30, 30, 30))  # Dark gray background
    screen.blit(stats_background, (0, ui_height))

    # Example statistics
    title_text = font.render("Economy & Statistics", True, (255, 255, 255))
    tax_text = font.render("Tax Rate: 15%", True, (255, 255, 255))  # Placeholder for future tax system
    pop_text = font.render("Population: 1,500", True, (255, 255, 255))  # Placeholder for future population system

    # Update loan status using the bank system
    loan_status = get_loan_status()  # This function is from bank.py
    loan_text = font.render(loan_status, True, (255, 255, 255))

    # Power and Water statistics from needs.py
    total_power_gen = get_total_power_generation(above_ground_level)  # Use above ground layer
    total_power_need = get_total_power_needs(above_ground_level, underground_level, grid_size)
    power_text = font.render(f"Power: Generated = {total_power_gen}, Needed = {total_power_need}", True, (255, 255, 255))

    total_water_gen = get_total_water_generation(above_ground_level)  # Use above ground layer
    total_water_need = get_total_water_needs(above_ground_level, underground_level, grid_size)
    water_text = font.render(f"Water: Generated = {total_water_gen}, Needed = {total_water_need}", True, (255, 255, 255))

    # Operating costs calculation
    power_costs = sum(power_operating_costs.get(tier, 0) for row in above_ground_level for zone_type, tier in row if zone_type == 4)
    water_costs = sum(water_operating_costs.get(tier, 0) for row in above_ground_level for zone_type, tier in row if zone_type == 5)

    costs_text = font.render(f"Operating Costs: Power = {power_costs}, Water = {water_costs}", True, (255, 255, 255))

    # Warning icon if insufficient power or water
    if total_power_gen < total_power_need or total_water_gen < total_water_need:
        draw_icon(screen, "icons/warning.png", width - 50, ui_height + 20)  # Red warning icon

    # Render these texts in the statistics window
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, ui_height + 50))
    screen.blit(tax_text, (50, ui_height + 100))    # Tax statistics
    screen.blit(pop_text, (50, ui_height + 150))    # Population statistics
    screen.blit(loan_text, (50, ui_height + 200))   # Loan statistics
    screen.blit(power_text, (50, ui_height + 250))  # Power statistics
    screen.blit(water_text, (50, ui_height + 300))  # Water statistics
    screen.blit(costs_text, (50, ui_height + 350))  # Operating costs



# Draw the bank menu
def draw_bank_menu(screen, font, ui_height):
    width, height = screen.get_size()

    # Create a semi-transparent overlay for the statistics window
    stats_background = pygame.Surface((width, height - ui_height))
    stats_background.set_alpha(200)  # Semi-transparent
    stats_background.fill((30, 30, 30))  # Dark gray background
    screen.blit(stats_background, (0, ui_height))

    # Display available loans
    small_loan_text = font.render("Small Loan: $1000, 5% interest, 10 cycles", True, (255, 255, 255))
    medium_loan_text = font.render("Medium Loan: $5000, 3% interest, 20 cycles", True, (255, 255, 255))
    large_loan_text = font.render("Large Loan: $10000, 2% interest, 30 cycles", True, (255, 255, 255))
    
    screen.blit(small_loan_text, (100, 100))
    screen.blit(medium_loan_text, (100, 150))
    screen.blit(large_loan_text, (100, 200))

    # Display active loan status
    loan_status_text = font.render(get_loan_status(), True, (255, 255, 255))
    screen.blit(loan_status_text, (100, 250))

    # Placeholder: Add buttons or keypress events to handle taking loans
    instruction_text = font.render("Press 8 for Small Loan, 9 for Medium Loan, 0 for Large Loan", True, (255, 255, 255))
    screen.blit(instruction_text, (100, 300))