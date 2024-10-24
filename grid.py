import pygame
from economy import can_afford_zone, pay_for_zone, infrastructure_costs



grid_size = 150  # Grid size (150x150)

# Initialize a double-layer grid system
def initialize_grid(grid_size):
    # Layer 1: Above-ground grid for zones
    above_ground_level = [[(0, 1) for _ in range(grid_size)] for _ in range(grid_size)]

    # Layer 0: Underground grid for pipes and power lines
    underground_level = [[None for _ in range(grid_size)] for _ in range(grid_size)]

    return above_ground_level, underground_level



# Place a zone on the grid (with tier)
def place_zone(above_ground_level, pos, selected_zone, selected_tier, cell_size, ui_height, offset_x, offset_y):
    # Adjust click position by subtracting the offsets
    adjusted_x = pos[0] - offset_x
    adjusted_y = pos[1] - offset_y - ui_height

    # Calculate the column and row based on the adjusted click position
    col = adjusted_x // cell_size
    row = adjusted_y // cell_size

    # Check if the click is within the grid
    if 0 <= col < grid_size and 0 <= row < grid_size:
        zone_type, current_tier = above_ground_level[row][col]
        if zone_type == 0:  # Only place zones on empty cells
            if can_afford_zone(selected_zone, selected_tier):  # Check if the player can afford the zone
                above_ground_level[row][col] = (selected_zone, selected_tier)  # Place the zone with the selected tier
                pay_for_zone(selected_zone, selected_tier)       # Deduct the cost
                return True
    return False



# Place infrastructure (pipes/power lines) in the underground layer
def place_infrastructure(underground_level, pos, infrastructure_type, cell_size, ui_height, offset_x, offset_y):
    # Adjust click position by subtracting the offsets
    adjusted_x = pos[0] - offset_x
    adjusted_y = pos[1] - offset_y - ui_height

    # Calculate the column and row based on the adjusted click position
    col = adjusted_x // cell_size
    row = adjusted_y // cell_size

    # Check if the click is within the grid bounds
    if 0 <= col < grid_size and 0 <= row < grid_size:
        if underground_level[row][col] is None:  # Only place infrastructure on empty underground tiles
            # Check if the player can afford the infrastructure
            infrastructure_cost = infrastructure_costs.get(infrastructure_type)
            if infrastructure_cost and can_afford_zone(infrastructure_type, 1):  # Passing None for tier (not applicable)
                # Deduct the cost for the infrastructure
                pay_for_zone(infrastructure_type, 1)
                underground_level[row][col] = infrastructure_type  # Place pipe or power line
                return True
    return False



# Adjusted colours for each zone and tier
colours = {
    0: (255, 255, 255, 255),      # White for empty cells
    1: {  # Residential Zone
        1: (64, 228, 32, 255),    # Light Green (Tier 1)
        2: (50, 205, 50, 255),    # Medium Green (Tier 2)
        3: (0, 128, 0, 255)       # Dark Green (Tier 3)
    },
    2: {  # Industrial Zone
        1: (192, 192, 192, 255),  # Light Gray (Tier 1)
        2: (128, 128, 128, 255),  # Medium Gray (Tier 2)
        3: (64, 64, 64, 255)      # Dark Gray (Tier 3)
    },
    3: {  # Road (no tier distinctions)
        1: (255, 0, 0, 255)       # Red for Roads
    },
    4: {  # Power Zone
        1: (255, 255, 102, 255),   # Light Yellow (Tier 1)
        2: (255, 255, 0, 255),     # Medium Yellow (Tier 2)
        3: (204, 204, 0, 255)      # Dark Yellow (Tier 3)
    },
    5: {  # Water Zone
        1: (102, 178, 255, 255),   # Light Blue (Tier 1)
        2: (51, 153, 255, 255),    # Medium Blue (Tier 2)
        3: (0, 102, 204, 255)      # Dark Blue (Tier 3)
    }
}



# Semi-transparent colours for underground mode
colours_transparent = {
    0: (255, 255, 255, 255),      # Semi-transparent white for empty cells
    1: {  # Residential Zone
        1: (64, 228, 32, 128),    # Light Green (Tier 1, semi-transparent)
        2: (50, 205, 50, 128),    # Medium Green (Tier 2, semi-transparent)
        3: (0, 128, 0, 128)       # Dark Green (Tier 3, semi-transparent)
    },
    2: {  # Industrial Zone
        1: (192, 192, 192, 128),  # Light Gray (Tier 1, semi-transparent)
        2: (128, 128, 128, 128),  # Medium Gray (Tier 2, semi-transparent)
        3: (64, 64, 64, 128)      # Dark Gray (Tier 3, semi-transparent)
    },
    3: {  # Road (no tier distinctions)
        1: (255, 0, 0, 128)       # Red for Roads (semi-transparent)
    },
    4: {  # Power Zone
        1: (255, 255, 102, 128),   # Light Yellow (Tier 1, semi-transparent)
        2: (255, 255, 0, 128),     # Medium Yellow (Tier 2, semi-transparent)
        3: (204, 204, 0, 128)      # Dark Yellow (Tier 3, semi-transparent)
    },
    5: {  # Water Zone
        1: (102, 178, 255, 128),   # Light Blue (Tier 1, semi-transparent)
        2: (51, 153, 255, 128),    # Medium Blue (Tier 2, semi-transparent)
        3: (0, 102, 204, 128)      # Dark Blue (Tier 3, semi-transparent)
    }
}



# Draw the grid with different shades based on the tier
def draw_grid(screen, grid, cell_size, ui_height, offset_x, offset_y, colors):
    for y, row in enumerate(grid):
        for x, (zone_type, tier) in enumerate(row):
            # Get the color for the current zone type and tier
            color = colors[zone_type][tier] if zone_type != 0 else colors[0]

            # Create a temporary surface for the grid cell (with transparency)
            temp_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)  
            # Fill the surface with the zone color, including the alpha channel (for transparency)
            temp_surface.fill(color)
            # Define the position where this cell should be drawn on the screen
            rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
            # Blit the cell (semi-transparent surface) onto the main screen
            screen.blit(temp_surface, rect)
            # Optionally draw grid lines (optional, but can be helpful for clarity)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)




def draw_infrastructure(screen, underground_layer, cell_size, ui_height, offset_x, offset_y):
    for y, row in enumerate(underground_layer):
        for x, infrastructure in enumerate(row):
            # Define colors for infrastructure (e.g., yellow for power lines, blue for water pipes)
            if infrastructure == 'power_line':
                color = (255, 255, 0)  # Yellow for power lines
            elif infrastructure == 'water_pipe':
                color = (0, 0, 255)  # Blue for water pipes
            else:
                continue  # Skip if there's no infrastructure

            # Create the rectangle for the current infrastructure cell
            rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
            # Draw the infrastructure directly on the screen
            pygame.draw.rect(screen, color, rect)
            # Optionally draw grid lines over the infrastructure
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)