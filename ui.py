import pygame
from economy import generate_income, get_money_income, get_resource_income, format_number
from needs import get_total_power_generation, get_total_water_generation, get_total_power_needs, get_total_water_needs



def draw_icon(screen, icon_path, x, y):
    # Load the image from the given path
    icon = pygame.image.load(icon_path).convert_alpha()  # Make sure it has an alpha channel for transparency
    icon = pygame.transform.scale(icon, (30, 30))  # Resize the icon if needed (adjust size as per your UI)
    screen.blit(icon, (x, y))  # Draw the icon on the screen



# Draw the compact UI with icons for money, resources, and income
def draw_ui(screen, money, resources, selected_zone, selected_tiers, font, grid, ui_height):
    # Set a box background for the row UI
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, screen.get_width(), ui_height))

    # Adjusted spacing for icons and tiers
    start_x = 10  # Initial x position for icons

    # Money Icon and Value (including income)
    money_income = get_money_income(grid)
    draw_icon(screen, "icons/money.png", start_x, 6)  # Money icon
    money_text = font.render(f"{format_number(money)} (+{format_number(money_income)})", True, (255, 255, 255))
    screen.blit(money_text, (start_x + 40, 10))  # Moved text a bit farther from the icon

    # Resources Icon and Value (including income)
    resource_income = get_resource_income(grid)
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
    screen.blit(power_zone_text, (start_x + 690 + 40, 10))  # Show power zone tier

    # Water Icon and Tier (use blue for selected)
    draw_icon(screen, "icons/water.png", start_x + 780, 6)  # Water icon
    water_zone_text = font.render(f"T{selected_tiers[4]}", True, (0, 0, 255) if selected_zone == 5 else (255, 255, 255))  # Blue for Water if selected
    screen.blit(water_zone_text, (start_x + 780 + 40, 10))  # Show water zone tier


# Cycle through zone tiers using keys
def handle_zone_selection(event, selected_zone, selected_tiers):
    # Handle zone selection
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1:
            selected_zone = 1  # Residential zone
        elif event.key == pygame.K_2:
            selected_zone = 2  # Industrial zone
        elif event.key == pygame.K_3:
            selected_zone = 3  # Road (no tier changes)
        elif event.key == pygame.K_4:
            selected_zone = 4  # Power
        elif event.key == pygame.K_5:
            selected_zone = 5  # Water

        # Handle tier cycling for Residential and Industrial zones (using up/down arrow keys)
        if selected_zone in [1, 2, 4, 5]:  # Only allow tier changes for Residential (1), Industrial (2), Water (4) and Power (5)
            index = selected_zone - 1
            if event.key == pygame.K_UP:  # Increase tier for the selected zone
                selected_tiers[selected_zone - 1] = min(selected_tiers[selected_zone - 1] + 1, 3)  # Max 3 tiers
            elif event.key == pygame.K_DOWN:  # Decrease tier for the selected zone
                selected_tiers[selected_zone - 1] = max(selected_tiers[selected_zone - 1] - 1, 1)  # Min 1 tier
    
    return selected_zone, selected_tiers



# Statistics window remains unchanged from before
def draw_statistics_ui(screen, font, ui_height, grid):
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
    loan_text = font.render("Loan: None", True, (255, 255, 255))  # Placeholder for future loan system

    # Power and Water statistics from needs.py
    total_power_gen = get_total_power_generation(grid)
    total_power_need = get_total_power_needs(grid)
    power_text = font.render(f"Power: Generated = {total_power_gen}, Needed = {total_power_need}", True, (255, 255, 255))

    total_water_gen = get_total_water_generation(grid)
    total_water_need = get_total_water_needs(grid)
    water_text = font.render(f"Water: Generated = {total_water_gen}, Needed = {total_water_need}", True, (255, 255, 255))

    # Render these texts in the statistics window
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, ui_height + 50))
    screen.blit(tax_text, (50, ui_height + 100))    # Tax statistics
    screen.blit(pop_text, (50, ui_height + 150))    # Population statistics
    screen.blit(loan_text, (50, ui_height + 200))   # Loan statistics
    screen.blit(power_text, (50, ui_height + 250))  # Power statistics
    screen.blit(water_text, (50, ui_height + 300))  # Water statistics