import random
from enemy import Enemy
from item import Item

class Room:
    """Represents a single room in the dungeon. It may contain enemies, items, traps, or puzzles."""

    def __init__(self, is_shortcut=False):
        """
        Initializes a randomly generated room with a description, 
        and possibly an enemy, an item, a trap, or a puzzle.
        Shortcut rooms have harder enemies, stronger traps, or better loot.
        """
        self.description = random.choice([
            "A dark chamber with glowing runes on the walls.",
            "A damp corridor with strange whispers in the air.",
            "A hall filled with ancient statues staring at you.",
            "A treasure vault illuminated by golden light.",
            "A narrow tunnel with bones scattered on the floor."
        ])
        
        # 50% chance to spawn an enemy (70% if in a shortcut)
        self.enemy = Enemy() if random.random() < (0.5 if not is_shortcut else 0.7) else None  

        # 40% chance to contain an item (50% if in a shortcut)
        self.item = Item() if random.random() < (0.4 if not is_shortcut else 0.5) else None  

        # 30% chance for a trap (50% if in a shortcut)
        self.trap = random.random() < (0.3 if not is_shortcut else 0.5)
        self.trap_damage = random.randint(5, 15) if self.trap else 0  

        # 25% chance for a puzzle (40% if in a shortcut)
        self.puzzle = self.generate_puzzle() if random.random() < (0.25 if not is_shortcut else 0.4) else None

    def generate_puzzle(self):
        """Generates a random puzzle that the player can solve to get a reward."""
        puzzles = [
            {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "echo"},
            {"question": "The more of me you take, the more you leave behind. What am I?", "answer": "footsteps"},
            {"question": "What has to be broken before you can use it?", "answer": "egg"},
            {"question": "I have keys but open no locks. What am I?", "answer": "piano"},
            {"question": "The more you remove from me, the bigger I get. What am I?", "answer": "hole"}
        ]
        return random.choice(puzzles)

    def handle_trap(self, player):
        """Handles trap interaction, allowing the player a chance to dodge or disarm it."""
        if not self.trap:
            return  # No trap in this room

        print("\nOh no! This room has a trap!")
        print(f"You see a dangerous mechanism. If triggered, it will deal {self.trap_damage} damage.")
        print("[1] Try to dodge the trap (50% success)") #not implemented yet would have to increase damage if failed
        print("[2] Try to disarm the trap (30% success)")#not implemented yet would have to increase damage if failed
        print("[3] Accept your fate and take the damage")#not implemented

        choice = input("Choose an option: ").strip()
        if choice == "1":  # Try to dodge
            if random.random() < 0.5:
                print("You successfully dodged the trap!")
                self.trap = False  # Deactivate trap
            else:
                print("You failed to dodge and take full damage!")
                player.health -= self.trap_damage

        elif choice == "2":  # Try to disarm
            if random.random() < 0.3:
                print("You carefully disarm the trap. Safe!")
                self.trap = False  # Deactivate trap
            else:
                print("You failed and triggered the trap!")
                player.health -= self.trap_damage

        else:  # Take damage
            print(f"You accept your fate and take {self.trap_damage} damage.")
            player.health -= self.trap_damage

    def handle_puzzle(self, player):
        """Handles puzzle solving interaction."""
        if not self.puzzle:
            return  # No puzzle in this room

        print(f"\nYou encounter a puzzle: {self.puzzle['question']}")
        answer = input("Your answer: ").strip().lower()
        if answer == self.puzzle['answer']:
            print("Correct! You are rewarded with a treasure!")
            if self.item:
                player.pick_item(self.item)
        else:
            print("Wrong answer! The puzzle remains unsolved.")

    def to_dict(self):
        """Converts the room's state into a dictionary for saving."""
        return {
            "description": self.description,
            "enemy": self.enemy.to_dict() if self.enemy else None,
            "item": self.item.to_dict() if self.item else None,
            "trap": self.trap,
            "trap_damage": self.trap_damage,
            "puzzle": self.puzzle
        }

    @classmethod
    def from_dict(cls, data):
        """Restores a room from a saved dictionary state."""
        room = cls()
        room.description = data["description"]
        room.enemy = Enemy.from_dict(data["enemy"]) if data["enemy"] else None
        room.item = Item.from_dict(data["item"]) if data["item"] else None
        room.trap = data["trap"]
        room.trap_damage = data["trap_damage"]
        room.puzzle = data["puzzle"]
        return room
