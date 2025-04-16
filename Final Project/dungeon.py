import random
from room import Room

class Dungeon:
    """Represents the dungeon, containing multiple randomly generated rooms, including shortcuts and other paths."""

    def __init__(self, num_rooms=5, num_shortcut_rooms=2, num_mystery_rooms=2):
        """
        Initializes the dungeon with:
        - Normal rooms (standard difficulty)
        - Shortcut rooms (higher difficulty, better rewards)
        - Mystery rooms (random chance of good or bad events)
        """
        self.rooms = [Room() for _ in range(num_rooms)]  
        self.shortcut_rooms = [Room(is_shortcut=True) for _ in range(num_shortcut_rooms)]  
        self.mystery_rooms = [Room() for _ in range(num_mystery_rooms)]  
        self.current_room_index = 0  
        self.in_shortcut = False
        self.in_mystery = False
        self.in_treasure_path = False

    def get_current_room(self):
        """Returns the current room where the player is."""
        if self.in_shortcut:
            return self.shortcut_rooms[self.current_room_index]
        if self.in_mystery:
            return self.mystery_rooms[self.current_room_index]
        return self.rooms[self.current_room_index]

    def move_to_next_room(self, choice, player):
        """
        Moves the player to the next room based on the dynamically generated choices.
        """
        if choice not in self.available_paths:
            print("Invalid choice! Choose a valid path.")
            return False  

        if choice == "1":
            if self.current_room_index < len(self.rooms) - 1:
                self.current_room_index += 1
                self.in_shortcut = False
                self.in_mystery = False
                return True

        elif choice == "2" and "2" in self.available_paths:
            if self.shortcut_rooms:
                self.current_room_index = 0  
                self.in_shortcut = True
                self.in_mystery = False
                return True

        elif choice == "3" and "3" in self.available_paths:
            if self.mystery_rooms:
                self.current_room_index = 0  
                self.in_mystery = True
                self.in_shortcut = False
                return True

        elif choice == "4" and "4" in self.available_paths:
            if random.random() < 0.2:
                print("\nYou found a secret passage leading to a Hidden Treasure Room!")
                survived = self.handle_hidden_treasure_event(player)  
                return survived  # ← False if dead


        return False   
    def handle_hidden_treasure_event(self, player):
        """
        Handles what happens when the player enters a Hidden Treasure Room.
        - 70% chance of instant death.
        - 30% chance of massive rewards.
        """
        print("\nYou enter the Hidden Treasure Room...")

        if random.random() < 0.7:  # 70% chance of instant death
            print("\n⚠️ You triggered a deadly trap! The ceiling collapses, crushing you instantly.")
            player.health = 0  # Instant death
            return False  
        else:
            gold_found = random.randint(100, 300)
            print(f"\n💰 You find a treasure chest filled with {gold_found} gold!")
            player.earn_gold(gold_found)

            rare_items = ["Warrior's Fury", "Titan's Elixir", "Elixir of Life"]
            if random.random() < 0.5:  # 50% chance to find a rare item
                item_name = random.choice(rare_items)
                print(f"\n🎁 You also find a rare item: {item_name}!")
                from item import Item
                player.pick_item(Item(name=item_name, effect="special", value=0))

        self.in_treasure_path = False  # Exit treasure path after event
        return True
    
    def display_room_choices(self):
        """
        Shows the player's available paths dynamically based on RNG.
        """
        self.available_paths = {}  # Reset available paths

        print("\nYou have the following choices:")
        self.available_paths["1"] = "Normal path - A standard dungeon room."
        print("[1] Normal path - A standard dungeon room.")

        if random.random() < 0.7:  
            self.available_paths["2"] = "Shortcut - A HIGH-RISK, HIGH-REWARD path (more enemies, harder puzzles, better loot)."
            print("[2] Shortcut - A HIGH-RISK, HIGH-REWARD path (more enemies, harder puzzles, better loot).")

        if random.random() < 0.5:  
            self.available_paths["3"] = "Mystery Path - Unknown danger or treasure!"
            print("[3] Mystery Path - Unknown danger or treasure!")

        if random.random() < 0.2:  
            self.available_paths["4"] = "Hidden Treasure Path - A rare path that might contain a fortune but has high chances of instant death!"
            print("[4] Hidden Treasure Path - A rare path that might contain a fortune but has high chances of instant death!")

    def display_dungeon_status(self):
        """
        Displays the current state of the dungeon for debugging or UI purposes.
        """
        print("\n=== Dungeon Map ===")
        for i, room in enumerate(self.rooms):
            status = " (You are here)" if i == self.current_room_index and not (self.in_shortcut or self.in_mystery) else ""
            print(f"Room {i + 1}: {room.description}{status}")

        if self.shortcut_rooms:
            for i, room in enumerate(self.shortcut_rooms):
                status = " (You are here)" if i == self.current_room_index and self.in_shortcut else ""
                print(f"Shortcut Room {i + 1}: {room.description}{status}")

        if self.mystery_rooms:
            for i, room in enumerate(self.mystery_rooms):
                status = " (You are here)" if i == self.current_room_index and self.in_mystery else ""
                print(f"Mystery Room {i + 1}: {room.description}{status}")

        print("===================")

    def handle_room_events(self, player):
        """
        Handles what happens when the player enters a room.
        Could trigger a trap, puzzle, treasure, or even gold rewards.
        """
        current_room = self.get_current_room()

        # Handle finding gold
        if random.random() < 0.3:  
            gold_found = random.randint(10, 50)
            print(f"\nYou found {gold_found} gold coins in this room!")
            player.gold += gold_found

        # Handle trap
        if current_room.trap:
            print(f"Oh no! It's a trap! You take {current_room.trap_damage} damage.")
            player.health -= current_room.trap_damage
            if player.health <= 0:
                print("You succumbed to the trap... Game over.")
                return False  

        # Handle puzzle event
        if current_room.puzzle:
            print(f"\nYou encounter a puzzle: {current_room.puzzle['question']}")
            answer = input("Your answer: ").strip().lower()
            if answer == current_room.puzzle['answer']:
                print("Correct! You are rewarded!")

                # extra gold
                bonus_gold = random.randint(20, 100)
                print(f"You received {bonus_gold} gold for solving the puzzle!")
                player.earn_gold(bonus_gold)

                # more % for items
                if current_room.item or random.random() < 0.5:
                    if not current_room.item:
                        from item import Item
                        current_room.item = Item()  # Generar un nuevo ítem aleatorio
                    print(f"You found an extra item: {current_room.item.name}!")
                    player.pick_item(current_room.item)

                # temporal Buff 
                buff_type = random.choice(["attack", "defense", "luck"])
                buff_value = random.randint(2, 5)
                player.temporary_buffs[buff_type] += buff_value
                print(f"You feel empowered! Your {buff_type} increased by {buff_value} for the next turns.")

            else:
                print("Wrong answer! The puzzle remains unsolved.")

        return True

    def is_exit_reached(self):
        """
        Returns True if the player has reached the last room (exit).
        """
        if self.in_shortcut:
            return self.current_room_index >= len(self.shortcut_rooms) - 1
        if self.in_mystery:
            return self.current_room_index >= len(self.mystery_rooms) - 1
        return self.current_room_index >= len(self.rooms) - 1

    def to_dict(self):
        """Converts the dungeon's state into a dictionary for saving."""
        return {
            "rooms": [room.to_dict() for room in self.rooms],
            "shortcut_rooms": [room.to_dict() for room in self.shortcut_rooms],
            "mystery_rooms": [room.to_dict() for room in self.mystery_rooms],
            "current_room_index": self.current_room_index,
            "in_shortcut": self.in_shortcut,
            "in_mystery": self.in_mystery
        }

    @classmethod
    def from_dict(cls, data):
        """Restores a dungeon from a saved dictionary state."""
        dungeon = cls(len(data["rooms"]), len(data["shortcut_rooms"]), len(data["mystery_rooms"]))
        dungeon.rooms = [Room.from_dict(room) for room in data["rooms"]]
        dungeon.shortcut_rooms = [Room.from_dict(room) for room in data["shortcut_rooms"]]
        dungeon.mystery_rooms = [Room.from_dict(room) for room in data["mystery_rooms"]]
        dungeon.current_room_index = data["current_room_index"]
        dungeon.in_shortcut = data["in_shortcut"]
        dungeon.in_mystery = data["in_mystery"]
        return dungeon
