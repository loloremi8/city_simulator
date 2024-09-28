import pygame
import json
from grid import initialize_grid, place_zone, draw_grid
from economy import get_player_money, get_player_resources, set_player_money, set_player_resources, generate_income, deduct_operational_costs
from ui import draw_ui, draw_statistics_ui, handle_zone_selection



# Save the game state
def save_game(grid, player_money, player_resources, file_name="savegame.json"):
    game_state = {
        "grid": grid,
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
    return game_state["grid"], game_state["player_money"], game_state["player_resources"]



# Initialize Pygame
pygame.init()

# Basic window settings
window_width, window_height = 1366, 705
ui_height = 50
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)

# Initialze the clock
clock = pygame.time.Clock()

# Separate timer for income generation
income_timer = pygame.time.get_ticks()

# Timer for cost deduction (8 seconds)
deduction_timer = pygame.time.get_ticks()
deduction_interval = 8000  # 8 seconds

# Game initialization
grid_size = 150  # Map is 200x200 now
grid = initialize_grid(grid_size)
selected_zone = 1
selected_tiers = [1, 1, 1, 1, 1]  # Default to Tier 1 for all zones

auto_save_interval = 300000  # 5 minutes (in milliseconds)
auto_save_timer = pygame.time.get_ticks()

# Initialize font
font = pygame.font.Font(None, 36)

# Initial zone for placement
selected_zone = 1

# Map movement and zoom variables
offset_x, offset_y = 0, 0  # Map offset for panning
is_panning = False  # Flag to check if we're panning the map
last_mouse_pos = (0, 0)  # Store the previous mouse position for panning

cell_size = 20  # Initial cell size for the grid
min_cell_size = 5  # Minimum zoom level (adjusted)
max_cell_size = 60  # Maximum zoom level

# Timer for generating income
income_timer = pygame.time.get_ticks()

# Flag for toggling the statistics window
show_statistics = False



# Main game loop
running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle zone selection and tier cycling
        selected_zone, selected_tiers = handle_zone_selection(event, selected_zone, selected_tiers)

        # Handle mouse wheel for zooming
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # Scrolling up (zoom in)
                cell_size = min(cell_size + 2, max_cell_size)
            elif event.y < 0:  # Scrolling down (zoom out)
                cell_size = max(cell_size - 2, min_cell_size)

        # Handle right mouse button for panning
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                is_panning = True
                last_mouse_pos = pygame.mouse.get_pos()
            elif event.button == 1:  # Left mouse button for placing zones
                pos = pygame.mouse.get_pos()
                if pos[1] >= ui_height:  # Ensure click is below the UI
                    place_zone(grid, pos, selected_zone, selected_tiers[selected_zone - 1], cell_size, ui_height, offset_x, offset_y)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Stop panning when RMB is released
                is_panning = False

        if event.type == pygame.KEYDOWN:
            # Save/Load game
            if event.key == pygame.K_s:  # Save game with 'S' key
                save_game(grid, get_player_money(), get_player_resources())
            elif event.key == pygame.K_l:  # Load game with 'L' key
                grid, player_money, player_resources = load_game()
                set_player_money(player_money)
                set_player_resources(player_resources)
            elif event.key == pygame.K_t:  # Toggle statistics window with 'T' key
                show_statistics = not show_statistics

    # Handle panning
    if is_panning:
        current_mouse_pos = pygame.mouse.get_pos()
        dx = current_mouse_pos[0] - last_mouse_pos[0]
        dy = current_mouse_pos[1] - last_mouse_pos[1]
        offset_x += dx
        offset_y += dy
        last_mouse_pos = current_mouse_pos

    # Generate income every 2 seconds
    if current_time - income_timer >= 2000: # Every 2 seconds
        generate_income(grid)
        income_timer = current_time

    # Timer for deducting operational costs (every 8 seconds)
    if current_time - deduction_timer >= deduction_interval:  # Every 8 seconds
        deduct_operational_costs(grid)  # Function to deduct costs (we will implement this)
        deduction_timer = current_time

    # Get current window size
    window_width, window_height = pygame.display.get_surface().get_size()

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the grid
    draw_grid(screen, grid, cell_size, ui_height, offset_x, offset_y)

    # Draw the main UI
    draw_ui(screen, get_player_money(), get_player_resources(), selected_zone, selected_tiers, font, grid, ui_height)

    # Draw the statistics window if toggled on
    if show_statistics:
        draw_statistics_ui(screen, font, ui_height, grid)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()