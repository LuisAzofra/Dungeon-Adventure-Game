import json
import random
from player import Player
from dungeon import Dungeon
from save_system import SaveSystem
from battle import Battle
from vendor import Vendor

def main():
    print("Welcome to Roguelike Dungeon Adventure!")

    # Load game if a save file exists
    save_data = SaveSystem.load_game()
    if save_data:
        choice = input("Do you want to continue your saved game? (y/n): ").lower()
        if choice == 'y':
            player = Player.from_dict(save_data['player'])
            dungeon = Dungeon.from_dict(save_data['dungeon'])
        else:
            player = create_new_character()
            dungeon = Dungeon()
    else:
        player = create_new_character()
        dungeon = Dungeon()

    # Display player stats at the start
    display_player_stats(player)

    while player.is_alive() and not dungeon.is_exit_reached():
        # Show room choices
        dungeon.display_room_choices()

        # Create a valid input prompt based on available paths
        valid_choices = list(dungeon.available_paths.keys())
        choice_prompt = f"\nWhich path do you choose? ({', '.join(valid_choices)}): "
        
        # Ensure player selects a valid path
        while True:
            choice = input(choice_prompt).strip()
            if choice in valid_choices:
                break
            print("Invalid choice! Choose a valid path.")

        if not dungeon.move_to_next_room(choice, player):
            if not player.is_alive():  # if dead instantly ends game
                print("You have died... Game Over.")
                break  
            print("You have reached the exit of the dungeon! Victory!")
            break  


        current_room = dungeon.get_current_room()
        print(f"\nYou enter: {current_room.description}")

        # Handle gold rewards
        if random.random() < 0.3:
            gold_found = random.randint(10, 50)
            print(f"You found {gold_found} gold coins!")
            player.earn_gold(gold_found)

        # Handle room events
        survived = dungeon.handle_room_events(player)
        if not survived:
            break  # Player died, game over

        # Handle combat if an enemy is in the room
        if current_room.enemy:
            print(f"A {current_room.enemy.name} appears!")
            battle = Battle(player, [current_room.enemy])  # supports multiple enemies
            battle.start()
            if not player.is_alive():
                print("You have been defeated. Game over.")
                break

        # Handle item pickup
        if current_room.item:
            print(f"You found a {current_room.item.name}!")
            player.pick_item(current_room.item)

        # 20% chance of finding a vendor
        if random.random() < 0.2:
            print("\nYou encounter a mysterious vendor in this room!")
            vendor = Vendor()
            vendor.show_shop(player)

        # Save progress after each turn
        SaveSystem.save_game(player, dungeon)

    if dungeon.is_exit_reached():
        print("Congratulations! You successfully escaped the dungeon!")

def create_new_character():
    """Handles the character creation process."""
    name = input("Enter your character's name: ").strip()
    return Player(name=name, health=100, attack=10, gold=50)  # Start with some gold

def display_player_stats(player):
    """Displays the player's stats at the beginning of the game."""
    print("\n=== Player Stats ===")
    print(f"Name: {player.name}")
    print(f"Health: {player.health}/{player.max_health}")
    print(f"Attack Power: {player.attack}")
    print(f"Gold: {player.gold} coins")
    if player.pet:
        print(f"Pet: {player.pet.name} (Health: {player.pet.health}, Attack: {player.pet.attack})")
    print("====================")

if __name__ == "__main__":
    main()
