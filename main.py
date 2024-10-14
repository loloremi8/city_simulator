import pygame
import json
from grid import initialize_grid, place_zone, draw_grid, place_infrastructure, draw_infrastructure, is_zone_connected, colours, colours_transparent
from economy import get_player_money, get_player_resources, set_player_money, set_player_resources, generate_income, deduct_operational_costs
from ui import draw_ui, draw_statistics_ui, handle_zone_selection



# Save the game state
def save_game(above_ground_level, underground_level, player_money, player_resources, file_name="savegame.json"):
    game_state = {
        "above_ground_level": above_ground_level,
        "underground_level": underground_level,
        "player_money": player_money,
        "player_resources": player_resources
    }
    with open(file_name, 'w') as save_file:
        json.dump(game_state, save_file)
    print("Game saved successfully!")



# Load the game state
def load_game(file_name="savegame.json"):
    with open(file_name, 'r') as load_file:
        game_state = json.load(load_file)
    print("Game loaded successfully!")
    return game_state["above_ground_level"], game_state["underground_level"], game_state["player_money"], game_state["player_resources"]



# Initialize Pygame
pygame.init()

# Basic window settings
window_width, window_height = 1366, 705
ui_height = 50
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE, pygame.SRCALPHA)

# Initialze the clock
clock = pygame.time.Clock()

# Separate timer for income generation
income_timer = pygame.time.get_ticks()

# Timer for cost deduction (8 seconds)
deduction_timer = pygame.time.get_ticks()
deduction_interval = 8000  # 8 seconds

# Game initialization
grid_size = 50  # Map is 150x150 now
above_ground_level, underground_level = initialize_grid(grid_size) # Initialize both layers
grid = above_ground_level

selected_zone = 1
selected_tiers = [1, 1, 1, 1, 1]  # Default to Tier 1 for all zones

auto_save_interval = 300000  # 5 minutes (in milliseconds)
auto_save_timer = pygame.time.get_ticks()

# Initialize font
font = pygame.font.Font(None, 36)

# Map movement and zoom variables
offset_x, offset_y = 0, 0  # Map offset for panning
is_panning = False  # Flag to check if we're panning the map
last_mouse_pos = None  # Store the previous mouse position for panning

cell_size = 20  # Initial cell size for the grid
min_cell_size = 5  # Minimum zoom level
max_cell_size = 60  # Maximum zoom level

# Timer for generating income
income_timer = pygame.time.get_ticks()

# Flag for toggling the statistics window
show_statistics = False

is_underground_mode = False  # Flag to track whether underground mode is active



# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle zone selection and tier cycling
        selected_zone, selected_tiers, is_underground_mode = handle_zone_selection(event, selected_zone, selected_tiers, is_underground_mode)

        # Handle mouse wheel for zooming
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scrolling up (zoom in)
                cell_size = min(cell_size + 2, max_cell_size)
            elif event.y < 0:  # Scrolling down (zoom out)
                cell_size = max(cell_size - 2, min_cell_size)

        # Handle right mouse button for panning
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if event.button == 3:  # Right mouse button
                is_panning = True
                last_mouse_pos = pos  # Set initial mouse position for panning

            elif event.button == 1:  # Left mouse button for placing zones
                if pos[1] >= ui_height:
                    if selected_zone in [1, 2, 4, 5]:  # Place zones (residential, industrial, power, water)
                        place_zone(above_ground_level, pos, selected_zone, selected_tiers[selected_zone - 1], cell_size, ui_height, offset_x, offset_y)
                    elif selected_zone == 3:  # Road placement
                        place_zone(above_ground_level, pos, selected_zone, 1, cell_size, ui_height, offset_x, offset_y)
                    elif selected_zone == 6:  # Assuming 6 is power line infrastructure
                        place_infrastructure(underground_level, pos, 'power_line', cell_size, ui_height, offset_x, offset_y)
                    elif selected_zone == 7:  # Assuming 7 is water pipe infrastructure
                        place_infrastructure(underground_level, pos, 'water_pipe', cell_size, ui_height, offset_x, offset_y)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Stop panning when RMB is released
                is_panning = False
                last_mouse_pos = None  # Reset mouse position when panning ends

        if event.type == pygame.KEYDOWN:
            # Save/Load game
            if event.key == pygame.K_s:  # Save game with 'S' key
                save_game(above_ground_level, underground_level, get_player_money(), get_player_resources())
            elif event.key == pygame.K_l:  # Load game with 'L' key
                above_ground_level, underground_level, player_money, player_resources = load_game()
                set_player_money(player_money)
                set_player_resources(player_resources)

                # Recalculate income based on loaded game
                generate_income(above_ground_level)  # Now using above_ground_level instead of grid
                deduct_operational_costs(above_ground_level)  # Recalculate operational costs

            elif event.key == pygame.K_t:  # Toggle statistics window with 'T' key
                show_statistics = not show_statistics

    # Range check for power and water
    for row in range(grid_size):
        for col in range(grid_size):
            zone_type, tier = above_ground_level[row][col]
            if zone_type == 1 or zone_type == 2:  # Residential or Industrial
                connected_to_power = is_zone_connected(above_ground_level, underground_level, row, col, 'power')
                connected_to_water = is_zone_connected(above_ground_level, underground_level, row, col, 'water')
                if not connected_to_power:
                    print(f"Zone at ({row}, {col}) not connected to power!")
                if not connected_to_water:
                    print(f"Zone at ({row}, {col}) not connected to water!")

    # Handle panning
    if is_panning:
        current_mouse_pos = pygame.mouse.get_pos()

        # Calculate the movement offset based on mouse movement
        dx = current_mouse_pos[0] - last_mouse_pos[0]
        dy = current_mouse_pos[1] - last_mouse_pos[1]

        # Update the map's offset based on mouse movement
        offset_x += dx
        offset_y += dy

        # Update the last mouse position for continuous panning
        last_mouse_pos = current_mouse_pos

    # Generate income every 2 seconds using the above_ground_level
    if current_time - income_timer >= 2000:  # Every 2 seconds
        generate_income(above_ground_level)
        income_timer = current_time

    # Timer for deducting operational costs (every 8 seconds) using the above_ground_level
    if current_time - deduction_timer >= deduction_interval:  # Every 8 seconds
        deduct_operational_costs(above_ground_level)
        deduction_timer = current_time

    # Get current window size
    window_width, window_height = pygame.display.get_surface().get_size()

    # Clear the screen
    screen.fill((0, 0, 0))

    # If underground mode is active
    if is_underground_mode:
        # Draw the above-ground layer with transparency when underground mode is active
        draw_grid(screen, above_ground_level, cell_size, ui_height, offset_x, offset_y, colours_transparent)
        # Draw the underground layer (pipes and power lines)
        draw_infrastructure(screen, underground_level, cell_size, ui_height, offset_x, offset_y)
    else:
        # Draw the normal above-ground layer
        draw_grid(screen, above_ground_level, cell_size, ui_height, offset_x, offset_y, colours)


    # Draw the main UI using the correct grids
    draw_ui(screen, get_player_money(), get_player_resources(), selected_zone, selected_tiers, font, ui_height, above_ground_level, underground_level, grid_size)

    # Draw the statistics window if toggled on using the correct grids
    if show_statistics:
        draw_statistics_ui(screen, font, ui_height, above_ground_level, underground_level, grid_size)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()