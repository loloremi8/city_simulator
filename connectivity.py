from collections import deque
from grid import grid_size

# Range system: Define how far power plants and water plants can reach
POWER_RANGE = 4  # 4 tiles in all directions
WATER_RANGE = 4  # 4 tiles in all directions

# Function to check if pipes are fully connected to the water plant
def find_connected_pipes(underground_level, start_row, start_col, grid_size):
    # Set to keep track of visited pipes
    visited = set()

    # Queue for BFS
    queue = deque()
    
    # Start by adding the water plant location to the queue
    queue.append((start_row, start_col))
    
    # Directions for neighboring cells (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        # Get the current cell from the queue
        current_row, current_col = queue.popleft()
        
        # Mark the current pipe as visited
        visited.add((current_row, current_col))
        
        # Explore the neighboring cells
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            
            # Check if the new cell is within grid bounds
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                # If it's a pipe and hasn't been visited, add to queue
                if underground_level[new_row][new_col] == 'water_pipe' and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col))
    
    return visited  # Return all connected pipes



# Function to check if a zone is within range of connected pipes
def is_zone_within_range_of_pipes(connected_pipes, row, col, range_limit=4):
    for pipe_row, pipe_col in connected_pipes:
        distance = abs(pipe_row - row) + abs(pipe_col - col)
        print(f"Checking distance between house at ({row}, {col}) and pipe at ({pipe_row}, {pipe_col}) = {distance}")  # Debug
        if distance <= range_limit:
            print(f"House is within range of connected pipe at ({pipe_row}, {pipe_col})")
            return True
    
    return False



def find_connected_pipes(underground_level, start_row, start_col, grid_size):
    visited = set()
    queue = deque()
    queue.append((start_row, start_col))
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        current_row, current_col = queue.popleft()
        visited.add((current_row, current_col))
        print(f"Checking pipe at: ({current_row}, {current_col})")  # Debug print to track pipes
        
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            if 0 <= new_row < grid_size and 0 <= new_col < grid_size:
                if underground_level[new_row][new_col] == 'water_pipe' and (new_row, new_col) not in visited:
                    queue.append((new_row, new_col))
    
    print(f"Connected pipes: {visited}")  # Debug print for connected pipes
    return visited



def is_power_connected(above_ground_level, underground_level, row, col, grid_size):
    # Check for power lines and plants within range of the house
    for r in range(max(0, row - POWER_RANGE), min(grid_size, row + POWER_RANGE + 1)):
        for c in range(max(0, col - POWER_RANGE), min(grid_size, col + POWER_RANGE + 1)):
            if underground_level[r][c] == 'power_line':
                print(f"Power line found at ({r}, {c}) near house at ({row}, {col})") # Debuging
            if above_ground_level[r][c][0] == 4:  # Power plant
                print(f"Power plant found at ({r}, {c}) near house at ({row}, {col})") # Debuging
            
            if underground_level[r][c] == 'power_line' or above_ground_level[r][c][0] == 4:
                return True

    print(f"House at ({row}, {col}) is NOT connected to power") # Debuging
    return False



def is_water_connected(above_ground_level, underground_level, row, col, grid_size):
    # Set to store all connected pipes
    connected_pipes = set()
    
    # Step 1: Flood-fill all pipes connected to water plants
    for r in range(grid_size):
        for c in range(grid_size):
            if above_ground_level[r][c][0] == 5:  # Water plant found
                connected_pipes.update(find_connected_pipes(underground_level, r, c, grid_size))
    
    # Step 2: Check if the house is within range of any connected pipes
    for pipe_row, pipe_col in connected_pipes:
        distance = abs(pipe_row - row) + abs(pipe_col - col)
        if distance <= WATER_RANGE:
            print(f"House at ({row}, {col}) is connected to water through pipe at ({pipe_row}, {pipe_col})") # Debuging
            return True

    print(f"House at ({row}, {col}) is NOT connected to water") # Debuging
    return False



# Helper function to check if a zone is within range of power/water
def is_zone_connected(above_ground_level, underground_level, row, col, zone_type, grid_size):
    if zone_type == 'power':
        # Power connection: Check both power plant and power lines within range
        for r in range(max(0, row - POWER_RANGE), min(grid_size, row + POWER_RANGE + 1)):
            for c in range(max(0, col - POWER_RANGE), min(grid_size, col + POWER_RANGE + 1)):
                # Check if either a power plant or power line is within range
                if underground_level[r][c] == 'power_line' or above_ground_level[r][c][0] == 4:
                    return True
        return False

    elif zone_type == 'water':
        # Water connection: Check if pipes are connected to a water plant
        connected_pipes = set()  # We will store all the connected pipes

        # First, find all water plants and flood-fill connected pipes
        for r in range(grid_size):
            for c in range(grid_size):
                if above_ground_level[r][c][0] == 5:  # Water plant found
                    connected_pipes.update(find_connected_pipes(underground_level, r, c, grid_size))

        # Now check if the zone is within range of any connected pipes
        return is_zone_within_range_of_pipes(connected_pipes, row, col, range_limit=WATER_RANGE)

    return False