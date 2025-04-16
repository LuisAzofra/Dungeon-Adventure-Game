import random

class Pet:
    """Represents a pet that helps the player in combat and can be attacked by enemies."""

    def __init__(self, name=None, health=None, attack=None):
        """
        Initializes a pet with random attributes if not provided.
        Some pets are stronger than others.
        """
        pet_types = [
            {"name": "Shadow Wolf", "health": 40, "attack": 8},
            {"name": "Flame Tiger", "health": 50, "attack": 10},
            {"name": "Stone Turtle", "health": 60, "attack": 5},
            {"name": "Lightning Hawk", "health": 35, "attack": 12},
            {"name": "Guardian Spirit", "health": 70, "attack": 6}
        ]

        if name and health and attack:
            self.name = name
            self.health = health
            self.attack = attack
        else:
            pet_data = random.choice(pet_types)
            self.name = pet_data["name"]
            self.health = pet_data["health"]
            self.attack = pet_data["attack"]

    def is_alive(self):
        """Returns True if the pet is still alive (health > 0)."""
        return self.health > 0

    def attack_enemy(self, enemy):
        """
        Pet attacks an enemy. Pets deal consistent damage.
        """
        if self.is_alive():
            print(f"{self.name} attacks {enemy.name} for {self.attack} damage! (Enemy health: {max(0, enemy.health - self.attack)})")
            enemy.health -= self.attack
            if enemy.health <= 0:
                print(f"{enemy.name} has been defeated!")

    def take_damage(self, damage):
        """
        Pet takes damage when an enemy targets it.
        """
        self.health -= damage
        print(f"{self.name} takes {damage} damage! (Health: {max(0, self.health)})")
        if self.health <= 0:
            print(f"{self.name} has fallen in battle!")

    def to_dict(self):
        """Converts the pet's state into a dictionary for saving."""
        return {"name": self.name, "health": self.health, "attack": self.attack}

    @classmethod
    def from_dict(cls, data):
        """Restores a pet from a saved dictionary state."""
        return cls(data["name"], data["health"], data["attack"])
