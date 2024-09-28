# city-simulator
Fun project to create a simple city simulator game in Python. The project idea went from a simulation, where it was randomizedhow the city would grow to a simulator/game. It is my first game project in Python using Pygame.

## How to play the game:

For now there is no in-game help, so everything will be written here. At this moment you **CANNOT** fail or bankrupt in this game, since there are no such mechanincs to allow you to do so. You can only gain money and resources.

Future and completed plans for the game:

- [x] To create the game environment, basic interactions with it.
- [x] Create 3 basic zones (Residential/Industrial/Road).
- [x] Create the economics system.
- [x] Re-work the map system.
- [x] Create the system of needs.
- [x] Ui optimalization (show statistics, rework the ui).
- [] Needs (check production, warnings, costs of operation, reach line/pipe system)
- [] Re-work the economy system (taxes-productivity/happines, loan-repayment system, costs-incresing prices for new zones).
- [] Multiple maps for a player
- [] Game progress (tiers, unlocking new zones)
- [] New Ui ("menu" type selection zone)
- [] Re-work the economy system (balance prices/costs to make it playable)
- [] Better graphics and animations ???

Now working on: Needs (check production, warnings, costs of operation, reach line/pipe system)
  
**Key actions:**

T - Opens/Closes statistic menu.

S/L - Save/Load the game file.

1/2/3/4/5 - Chooses zones (Residential/Industrail/Road/Power/Water).

Arrow keys Up/Down - Chooses tiers of zones (Only for Residential/Industial/Power/Water).

**Interaction with the map:**

LMB - Places selected zone.

RMB while holding and dragging - moving the map.

MBW - Zoom on the map.

**Zone costs:**

*Residential Zone*

Tier 1: Money: 50, Resources: 20,

Tier 2: Money: 100, Resources: 40,

Tier 3: Money: 150, Resources: 60.

*Industrial zone*

Tier 1: Money: 100, Resources: 50,

Tier 2: Money: 200, Resources: 100,

Tier 3: Money: 300, Resources: 150.

*Road*

Money: 20, Resources: 10.

*Power zone*

Tier 1: Money: 200, Resources: 100,

Tier 2: Money: 400, Resources: 200,

Tier 3: Money: 600, Resources: 300.

*Water Zone*

Tier 1: Money: 150, Resources: 75,
        
Tier 2: Money: 300, Resources: 150,

Tier 3: Money: 450, Resources: 225.

**Zone incomes:**

*Residential Zone*

Tier 1: Money: 5, Resources: 2,

Tier 2: Money: 10, Resources: 4,

Tier 3: Money: 15, Resources: 6.

*Industrial Zone*

Tier 1: Money: 10, Resources: 5,

Tier 2: Money: 20, Resources: 10,

Tier 3: Money: 30, Resources: 15.

*Road*

No income

*Power Zone*

Tier 1: Generation: 20,

Tier 2: Generation: 50,

Tier 3: Generation: 100.

*Water Zone*

Tier 1: Generation: 20,

Tier 2: Generation: 50,

Tier 3: Generation: 100.

**Zone power and water needs:**

*Residential Zone*

Tier 1: Power: 5, Water: 5,

Tier 2: Power: 10, Water: 10,

Tier 3: Power: 15, Water: 15.

*Industrial Zone*

Tier 1: Power: 10, Water: 10,

Tier 2: Power: 20, Water: 20,

Tier 3: Power: 30, Water: 30.
