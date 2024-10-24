# city-simulator
Fun project to create a simple city simulator game in Python. The project idea went from a simulation, where it was randomized how the city would grow to a simulator/game. It is my first game project in Python using Pygame.

## How to play the game:

For now there is no in-game help, so everything will be written here. The economy system is not balanced yet, but now you can lose money, since the adding of the infrastructure costs.

To make lines and pipes conected to buildings or power houses make sure they are in 4-block radius.

Future and completed plans for the game:

- [x] To create the game environment, basic interactions with it.
- [x] Create 3 basic zones (Residential/Industrial/Road).
- [x] Create the economics system.
- [x] Re-work the map system.
- [x] Create the system of needs.
- [x] Ui optimalization (show statistics, rework the ui).
- [x] Needs (check production, warnings, costs of operation, reach line/pipe system).
- [x] Saving/Loading both layers of the map.
- [x] Re-work the economy system (loan-repayment system, costs-increasing prices for new zones).
- [x] Re-work the economy system (balance prices/costs to make it playable).
------------------------------------
Bonus work (not needed, but I've a crap ton of work to do, so...):
- [] Re-work the economy system (taxes-productivity/happines).
- [] Multiple maps for a player.
- [] Game progress (tiers, unlocking new zones).
- [] New Ui ("menu" type selection zone).
- [] Better graphics and animations ???

Now working on: For now the project is done. There may be future updates, but not likely. Feel free to branch it and work on it by yourself.
  
**Key actions:**

T - Opens/Closes statistic menu.

B - Opens/Closes bank menu.

S/L - Save/Load the game file.

1/2/3/4/5/6/7 - Chooses zones (Residential/Industrail/Road/Power/Water/Power lines/Water pipes).

8/9/0 - Chooses loans.

Arrow keys Up/Down - Chooses tiers of zones (Only for Residential/Industial/Power/Water).

**Interaction with the map:**

LMB - Places selected zone.

RMB while holding and dragging - moving the map.

MBW - Zoom on the map.

**Costs:**

*Loans*

Small loan: Amount: 1000, Interest rate: 0.05, Duration: 10,

Medium loan: Amount: 5000, Interest rate: 0.03, Duration: 20,

Large loan: Amount: 10000, Interest rate: 0.02, Duration: 30.

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

*Power line*

Money: 10, Resources: 5.

*Water pipes*

Money: 8, Resources: 4.

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

*Power lines*

No income

*Water pipes*

No income

**Zone power and water needs:**

*Residential Zone*

Tier 1: Power: 5, Water: 5,

Tier 2: Power: 10, Water: 10,

Tier 3: Power: 15, Water: 15.

*Industrial Zone*

Tier 1: Power: 10, Water: 10,

Tier 2: Power: 20, Water: 20,

Tier 3: Power: 30, Water: 30.