# City Simulator

Welcome to the City Simulator game! This project is a simple city-building game created in Python using Pygame. The game allows you to build and manage a city, balancing resources, infrastructure, and economy.

## How to Play the Game

### Key Actions

- **T**: Toggle the statistics menu.
- **B**: Toggle the bank menu.
- **S**: Save the game.
- **L**: Load the game.
- **1**: Select Residential zone.
- **2**: Select Industrial zone.
- **3**: Select Road.
- **4**: Select Power zone.
- **5**: Select Water zone.
- **6**: Select Power lines.
- **7**: Select Water pipes.
- **8**: Take a small loan (when bank menu is open).
- **9**: Take a medium loan (when bank menu is open).
- **0**: Take a large loan (when bank menu is open).
- **Arrow Up/Down**: Change the tier of the selected zone (only for Residential, Industrial, Power, and Water zones).

### Interaction with the Map

- **Right Mouse Button**: Pan the map by clicking and dragging.
- **Mouse Wheel**: Zoom in and out of the map.
- **Left Mouse Button**: Place zones or infrastructure on the map.

### Game Mechanics

#### Zones

1. **Residential (1)**: Houses for citizens. Residential zones generate income based on the number of residents.
2. **Industrial (2)**: Factories and workplaces. Industrial zones generate income based on production.
3. **Road (3)**: Roads for transportation. Roads are necessary for connecting different zones.
4. **Power (4)**: Power plants. Power zones generate electricity for the city.
5. **Water (5)**: Water facilities. Water zones provide water to the city.
6. **Power Lines (6)**: Infrastructure for power distribution. Power lines connect power plants to other zones.
7. **Water Pipes (7)**: Infrastructure for water distribution. Water pipes connect water facilities to other zones.

#### Economy

- **Income Generation**: Income is generated every 2 seconds based on the zones you have built. Residential and Industrial zones are primary sources of income.
- **Operational Costs**: Costs are deducted every 8 seconds for maintaining infrastructure. Ensure you have enough income to cover these costs.
- **Loans**: Players can take small, medium, or large loans using keys 8, 9, and 0 respectively when the bank menu is open. Loans provide immediate funds but must be repaid over time.

#### Statistics

- The statistics menu shows various metrics about the city's performance and resources, including income, expenses, and resource availability.

#### Bank

- The bank menu allows players to take loans to support city development. Loans come in three sizes: small, medium, and large. Use loans wisely to avoid financial difficulties.

#### Saving and Loading

- The game state can be saved and loaded using the S and L keys. The game state includes the above-ground level, underground level, player money, and player resources. This allows you to continue your game from where you left off.

### Detailed Gameplay Instructions

1. **Starting the Game**:
   - Launch the game, and you will see an empty map with a grid.
   - Use the arrow keys to select the tier of the zones you want to place.

2. **Building Zones**:
   - Select a zone type using keys 1 to 7.
   - Click on the map to place the selected zone. Ensure that power lines and water pipes are within a 4-block radius of buildings or power houses for connectivity.

3. **Managing Resources**:
   - Keep an eye on your income and operational costs. Ensure that your city generates enough income to cover the costs of maintaining infrastructure.
   - Use the statistics menu (T key) to monitor your city's performance and resources.

4. **Taking Loans**:
   - If you need additional funds, open the bank menu using the B key.
   - Take a loan by pressing keys 8, 9, or 0 for small, medium, or large loans, respectively. Remember to repay loans to avoid financial penalties.

5. **Saving and Loading**:
   - Save your game progress using the S key.
   - Load a previously saved game using the L key.

6. **Expanding Your City**:
   - Continue building and expanding your city by placing different zones and infrastructure.
   - Balance the needs of your city, such as power and water supply, to ensure smooth operation.

### Future and Completed Plans for the Game

- [x] Create the game environment and basic interactions.
- [x] Implement 3 basic zones (Residential, Industrial, Road).
- [x] Develop the economics system.
- [x] Rework the map system.
- [x] Implement the system of needs.
- [x] Optimize the UI (show statistics, rework the UI).
- [x] Implement needs (check production, warnings, costs of operation, reach line/pipe system).
- [x] Implement saving/loading for both layers of the map.
- [x] Rework the economy system (loan-repayment system, costs-increasing prices for new zones).
- [x] Balance the economy system (balance prices/costs to make it playable).

### Bonus Work (not needed, but planned for future updates)

- [] Rework the economy system (taxes-productivity/happiness).
- [] Implement multiple maps for a player.
- [] Add game progress (tiers, unlocking new zones).
- [] Develop a new UI ("menu" type selection zone).
- [] Improve graphics and animations.

### Now Working On

For now, the project is done. There may be future updates, but not likely. Feel free to branch it and work on it by yourself.

### Additional Notes

- **Map Movement and Zoom**: Use the right mouse button to pan the map and the mouse wheel to zoom in and out.
- **Zone Placement**: Use the left mouse button to place zones or infrastructure. Ensure that power lines and water pipes are within a 4-block radius of buildings or power houses for connectivity.
- **Income and Costs**: Keep an eye on your income and operational costs to ensure your city remains financially stable.
- **Loans**: Use loans wisely to support city growth, but remember to repay them to avoid financial penalties.

Enjoy building your city!