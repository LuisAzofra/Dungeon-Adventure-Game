# Roguelike Dungeon Adventure Game

## Overview
This project is a **text-based Roguelike Dungeon Adventure Game** developed in Python. It follows Object-Oriented Programming (OOP) principles and incorporates advanced concepts such as iterators, JSON file storage, exception handling, and randomized dungeon generation. The goal is for the player to explore a procedurally generated dungeon, battle enemies, collect items, solve puzzles, and ultimately reach the exit.

## Features
- **Character System:** Players have a name, health points (HP), attack power, an inventory, and can pick up and use items.
- **Dungeon System:** The dungeon consists of multiple rooms, each with random events such as enemies, treasures, or traps.
- **Combat System:** Turn-based battle mechanics where players can attack, flee, or use items.
- **Item System:** Weapons, armor, and potions can be collected and used to enhance player abilities.
- **Save & Load System:** Player progress is stored in a JSON file, allowing resuming from the last saved state.
- **Event System:** Random encounters including puzzles, merchants, and hidden events.
- **Extra Features:** The game includes a pet companion system and an in-game vendor for purchasing items.

## Project Structure
```
/Final Project/
├── battle.py        # Handles turn-based combat mechanics
├── dungeon.py       # Manages dungeon generation and room navigation
├── enemy.py         # Defines enemy attributes and behaviors
├── item.py          # Manages collectible and usable items
├── main.py          # Main game loop and logic
├── pet.py           # Implements a pet companion system (Bonus Feature)
├── player.py        # Defines player attributes, inventory, and actions
├── room.py          # Represents individual dungeon rooms
├── savegame.json    # Stores game progress (if saved)
├── save_system.py   # Handles save/load functionality with JSON
├── vendor.py        # Implements an in-game merchant (Bonus Feature)
└── __pycache__/     # Compiled Python files for optimization
```

## Class Descriptions

### **1️⃣ Player (player.py)**
This class represents the player character.
- **Attributes:**
  - `name`: Player’s name.
  - `health`: Player’s current HP.
  - `attack`: The player's attack power.
  - `inventory`: A list of collected items.
  - `gold`: The amount of gold the player has.
  - `pet`: A pet companion (Useful in combat, can attack or receive damage).
  - `temporary_buffs`: Dictionary storing temporary power-ups.
- **Methods:**
  - `pick_item(item)`: Adds an item to the inventory.
  - `use_item(item_name)`: Uses an item from the inventory.
  - `earn_gold(amount)`: Increases the player’s gold.
  - `is_alive()`: Checks if the player is still alive.
  - `to_dict()`, `from_dict()`: Save/load player data.

### **2️⃣ Dungeon (dungeon.py)**
This class manages dungeon exploration.
- **Attributes:**
  - `rooms`: A list of randomly generated rooms.
  - `current_room_index`: The index of the room the player is currently in.
- **Methods:**
  - `generate_rooms(num_rooms)`: Creates random rooms with different characteristics.
  - `next_room()`: Moves the player to the next room.
  - `is_exit_reached()`: Checks if the player has reached the dungeon exit.
  - `to_dict()`, `from_dict()`: Save/load dungeon state.

### **3️⃣ Enemy (enemy.py)**
Represents different enemies in the game.
- **Attributes:**
  - `name`: Enemy’s name (e.g., Goblin, Orc, Dark Mage).
  - `health`: Enemy’s HP.
  - `attack`: Enemy’s attack power.
  - `ability`: Some enemies have special abilities (fire, poison, stun, etc.).
- **Methods:**
  - `is_alive()`: Checks if the enemy is still alive.
  - `attack_player(player)`: Executes an attack on the player.
  - `to_dict()`, `from_dict()`: Save/load enemy data.

### **4️⃣ Battle (battle.py)**
Handles turn-based combat.
- **Methods:**
  - `player_turn()`: Player chooses to attack, use an item, or flee.
  - `enemy_turn()`: Enemies attack the player.
  - `attack_enemy(enemy)`: Executes a standard attack.
  - `counterattack_enemy(enemy)`: High-risk counterattack option. (May miss or may do double damage to enemy)
  - `flee()`: Attempts to escape from battle. (Chances of escaping change when there is more enemies)
  - `apply_status_effects()`: Applies status effects like poison or burn.

### **5️⃣ Item (item.py)**
Manages items.
- **Types of Items:**
  - Healing potions: Restore HP.
  - Attack-boosting potions: Increase attack power.
  - Defense-boosting potions: Gives extra defense.
  - Special items: Remove fire/poison effects, increase max health, increase luck. 
- **Methods:**
  - `use(player)`: Applies an item effect to the player.
  - `get_item_description()`: Describes an item.
  - `to_dict()`, `from_dict()`: Save/load items.

### **6️⃣ Save System (save_system.py)**
Handles game save and load functions.
- **Methods:**
  - `save_game(player, dungeon)`: Saves the game state into a JSON file.
  - `load_game()`: Loads the game state from JSON.

### **7️⃣ Vendor (vendor.py) - Bonus Feature**
Implements an in-game merchant where players can buy items or pets. (Less powerfull objects have more chances to be available for buying)
- **Methods:**
  - `display_items()`: Shows available items for purchase.
  - `buy_item(player, item_name)`: Allows players to purchase items.

### **8️⃣ Pet (pet.py) - Bonus Feature**
Adds a pet companion to assist in battles. (There is 5 possible pets to find, chances are low but can also be bought in vendor)
- **Attributes:**
  - `name`: Pet’s name.
  - `health`: Pet’s HP.
  - `attack`: Pet’s attack power.
- **Methods:**
  - `is_alive()`: Checks if the pet is alive.
  - `attack_enemy(enemy)`: Allows the pet to attack enemies.

## How to Play
1. **Run the Game:**
   ```sh
   python main.py
   ```
2. If a saved game is detected, the player can **continue** or start a **new game**.
3. Explore the dungeon room by room.
4. Engage in **turn-based combat** when encountering enemies.
5. Collect items, solve puzzles, and interact with merchants.
6. The game saves progress automatically after major actions.
7. The game ends when the player **reaches the exit** or **dies in battle**.

## Controls
- **Navigation:** Progress through dungeon rooms.
- **Combat:** Choose actions such as attack, flee, or use items.
- **Inventory:** Pick up, use, or purchase items from vendors.

## Technical Features
- **OOP Design:** Modular structure with multiple classes.
- **Iterators:** Used in dungeon room navigation.
- **File Storage:** JSON-based save/load system.
- **Exception Handling:** Manages invalid input and corrupted save files.
- **Randomization:** Procedural dungeon generation and enemy/item placement.

## Possible Improvements
- Add a skill tree or leveling system for the player.
- Enhance enemy with different attacks
- Enemys with pets

Enjoy your dungeon adventure!

