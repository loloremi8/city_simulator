import pygame
from economy import can_afford_zone, pay_for_zone



grid_size = 150  # Grid size (200x200)

# Initialize grid with tier information
def initialize_grid(grid_size):
    return [[(0, 1) for _ in range(grid_size)] for _ in range(grid_size)]  # Each cell is (zone_type, tier)



# Place a zone on the grid (with tier)
def place_zone(grid, pos, selected_zone, selected_tier, cell_size, ui_height, offset_x, offset_y):
    # Adjust click position by subtracting the offsets
    adjusted_x = pos[0] - offset_x
    adjusted_y = pos[1] - offset_y - ui_height

    # Calculate the column and row based on the adjusted click position
    col = adjusted_x // cell_size
    row = adjusted_y // cell_size

    # Check if the click is within the grid
    if 0 <= col < grid_size and 0 <= row < grid_size:
        zone_type, current_tier = grid[row][col]
        if zone_type == 0:  # Only place zones on empty cells
            if can_afford_zone(selected_zone, selected_tier):  # Check if the player can afford the zone
                grid[row][col] = (selected_zone, selected_tier)  # Place the zone with the selected tier
                pay_for_zone(selected_zone, selected_tier)       # Deduct the cost
                return True
    return False



# Adjusted colors for each zone and tier
colors = {
    0: (255, 255, 255),      # White for empty cells
    1: {  # Residential Zone
        1: (64, 228, 32),    # Light Green (Tier 1)
        2: (50, 205, 50),    # Medium Green (Tier 2)
        3: (0, 128, 0)       # Dark Green (Tier 3)
    },
    2: {  # Industrial Zone
        1: (192, 192, 192),  # Light Gray (Tier 1)
        2: (128, 128, 128),  # Medium Gray (Tier 2)
        3: (64, 64, 64)      # Dark Gray (Tier 3)
    },
    3: {  # Road (no tier distinctions)
        1: (255, 0, 0)       # Red for Roads
    },
    4: {  # Power Zone
        1: (255, 255, 102),   # Light Yellow (Tier 1)
        2: (255, 255, 0),     # Medium Yellow (Tier 2)
        3: (204, 204, 0)      # Dark Yellow (Tier 3)
    },
    5: {  # Water Zone
        1: (102, 178, 255),   # Light Blue (Tier 1)
        2: (51, 153, 255),    # Medium Blue (Tier 2)
        3: (0, 102, 204)      # Dark Blue (Tier 3)
    }
}



# Draw the grid with different shades based on the tier
def draw_grid(screen, grid, cell_size, ui_height, offset_x, offset_y):
    for y, row in enumerate(grid):
        for x, (zone_type, tier) in enumerate(row):
            # Check if the cell is empty
            if zone_type == 0:
                color = colors[0]  # Use white for empty cells
            else:
                color = colors[zone_type][tier]
            
            # Draw the cell
            rect = pygame.Rect(x * cell_size + offset_x, y * cell_size + offset_y + ui_height, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Optional: draw grid lines