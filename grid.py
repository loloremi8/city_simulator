import pygame
from economy import can_afford_zone, pay_for_zone, infrastructure_costs



grid_size = 50  # Grid size (150x150)

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



# Range system: Define how far power plants and water plants can reach
POWER_RANGE = 4  # Example: 4 tiles in all directions
WATER_RANGE = 4  # Example: 4 tiles in all directions

# Helper function to check if a zone is within range of power/water
def is_zone_connected(above_ground_level, underground_level, row, col, zone_type):
    for r in range(max(0, row - POWER_RANGE), min(grid_size, row + POWER_RANGE + 1)):
        for c in range(max(0, col - POWER_RANGE), min(grid_size, col + POWER_RANGE + 1)):
            # Check for power/water zone or lines/pipes
            if zone_type == 'power' and (underground_level[r][c] == 'power_line' or above_ground_level[r][c][0] == 4):
                return True
            if zone_type == 'water' and (underground_level[r][c] == 'water_pipe' or above_ground_level[r][c][0] == 5):
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



# Adjusted colors for each zone and tier
colors = {
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



# Draw the grid with different shades based on the tier
def draw_grid(screen, grid, cell_size, ui_height, offset_x, offset_y, is_underground_mode=False):
    for y, row in enumerate(grid):
        for x, (zone_type, tier) in enumerate(row):
            # Check if the cell is empty
            if zone_type == 0:
                color = colors[0]  # Use white for empty cells
            else:
                color = colors[zone_type][tier]

            # If in underground mode, make the above-ground layer semi-transparent
            if is_underground_mode:
                # Create a temporary surface with transparency (SRCALPHA flag)
                temp_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

                # Adjust color to make it semi-transparent (alpha 128)
                semi_transparent_color = (*color[:3], 128)  # Keep RGB, adjust alpha

                # Fill the temporary surface with the semi-transparent color
                temp_surface.fill(semi_transparent_color)

                # Draw the semi-transparent cell onto the screen
                rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
                screen.blit(temp_surface, rect)
            else:
                # Normal mode: draw without transparency
                rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
                pygame.draw.rect(screen, color, rect)

            # Draw grid lines (optional)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)



def draw_infrastructure(screen, underground_layer, cell_size, ui_height, offset_x, offset_y):
    for y, row in enumerate(underground_layer):
        for x, infrastructure in enumerate(row):
            # Create a temporary surface for drawing the underground cell with transparency
            temp_surface = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

            # Fill the temporary surface with white for empty cells or specific colors for lines/pipes
            if infrastructure is None:
                temp_surface.fill((255, 255, 255))  # White for empty cells
            elif infrastructure == 'power_line':
                temp_surface.fill((255, 255, 0))  # Yellow for power lines
            elif infrastructure == 'water_pipe':
                temp_surface.fill((0, 0, 255))  # Blue for water pipes

            # Draw the underground cell
            rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
            screen.blit(temp_surface, rect)  # Blit the surface onto the screen
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Optional: draw grid lines