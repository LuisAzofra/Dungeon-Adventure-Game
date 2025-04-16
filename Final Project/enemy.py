import random

class Enemy:
    """Represents an enemy that the player can encounter in a dungeon room."""

    def __init__(self, name=None, health=None, attack=None, ability=None):
        """
        Initializes an enemy with random attributes if not provided.
        Some enemies have special abilities like poisoning, stunning, or draining health.
        """
        enemy_types = [
            {"name": "Goblin", "health": 30, "attack": 5, "ability": None},
            {"name": "Skeleton", "health": 40, "attack": 7, "ability": None},
            {"name": "Orc", "health": 50, "attack": 10, "ability": None},
            {"name": "Dark Mage", "health": 35, "attack": 12, "ability": "drain"},
            {"name": "Demon", "health": 60, "attack": 15, "ability": "fire"},
            {"name": "Venomous Spider", "health": 25, "attack": 6, "ability": "poison"},
            {"name": "Stone Golem", "health": 80, "attack": 12, "ability": "stun"},
            {"name": "Shadow Assassin", "health": 45, "attack": 14, "ability": "double_attack"},
            {"name": "Ancient Dragon", "health": 120, "attack": 25, "ability": "fire"},
        ]

        if name and health and attack:
            self.name = name
            self.health = health
            self.attack = attack
            self.ability = ability
        else:
            enemy_data = random.choice(enemy_types)
            self.name = enemy_data["name"]
            self.health = enemy_data["health"]
            self.attack = enemy_data["attack"]
            self.ability = enemy_data["ability"]

    def is_alive(self):
        """Returns True if the enemy is still alive (health > 0)."""
        return self.health > 0

    def attack_player(self, player):
        """
        Attacks the player and applies special effects if the enemy has an ability.
        """
        damage = self.attack
        print(f"{self.name} attacks you for {damage} damage!")
        player.health -= damage

        # Apply ability effects
        if self.ability == "poison":
            print(f"{self.name} poisons you! You will take 3 extra damage for 3 turns.")
            player.temporary_buffs["poison"] = 3  # Poison lasts 3 turns

        elif self.ability == "stun":
            print(f"{self.name} stuns you! You will miss your next turn.")
            player.temporary_buffs["stunned"] = 1  # Player skips next turn

        elif self.ability == "drain":
            drain_amount = int(damage * 0.5)  # Steals 50% of attack damage
            print(f"{self.name} drains {drain_amount} HP from you!")
            self.health += drain_amount

        elif self.ability == "fire":
            print(f"{self.name} engulfs you in flames! You take 5 extra damage for 2 turns.")
            player.temporary_buffs["burn"] = 2  # Fire effect lasts 2 turns

        elif self.ability == "double_attack":
            print(f"{self.name} strikes twice!")
            player.health -= damage  # Extra hit for the same amount
            
        print(f"(Your health: {max(0, player.health)})")  # Always show updated health

    def to_dict(self):
        """Converts the enemy's state into a dictionary for saving."""
        return {"name": self.name, "health": self.health, "attack": self.attack, "ability": self.ability}

    @classmethod
    def from_dict(cls, data):
        """Restores an enemy from a saved dictionary state."""
        return cls(data["name"], data["health"], data["attack"], data["ability"])
