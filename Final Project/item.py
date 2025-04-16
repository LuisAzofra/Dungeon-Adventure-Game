import random

class Item:
    """Represents an item that the player can collect, use, or buy in shops."""

    def __init__(self, name=None, effect=None, value=None, duration=None, price=None):
        """
        Initializes an item with random attributes if not provided.
        Items can be healing potions, attack boosters, defense potions, or rare effects.
        """
        items = [
            # Healing potions
            ("Small Healing Potion", "heal", 20, None, 10),
            ("Medium Healing Potion", "heal", 50, None, 25),
            ("Large Healing Potion", "heal", 100, None, 50),
            ("Elixir of Life", "heal", 200, None, 100),  

            # Attack-boosting potions
            ("Minor Strength Potion", "attack", 5, 3, 20),
            ("Major Strength Potion", "attack", 10, 5, 40),
            ("Warrior's Fury", "attack", 15, 5, 75),  

            # Defense-boosting potions
            ("Iron Skin Potion", "defense", 3, 4, 25),
            ("Titan's Elixir", "defense", 5, 6, 50),

            # Special items
            ("Max Health Elixir", "max_health", 50, None, 150),  
            ("Luck Charm", "luck", 2, 5, 60),  
            ("Anti-Poison Potion", "remove_poison", None, None, 30),  
            ("Fire Resistance Potion", "remove_burn", None, None, 30)  
        ]

        if name and effect and value is not None:
            self.name = name
            self.effect = effect
            self.value = value
            self.duration = duration
            self.price = price
        else:
            self.name, self.effect, self.value, self.duration, self.price = random.choice(items)

    def get_item_description(self):
        """Returns a description of an item based on its effect."""
        if self.effect == "heal":
            return f"Restores {self.value} HP"
        elif self.effect == "attack":
            return f"Increases attack by {self.value} for {self.duration} turns"
        elif self.effect == "defense":
            return f"Increases defense by {self.value} for {self.duration} turns"
        elif self.effect == "max_health":
            return f"Permanently increases max health by {self.value}"
        elif self.effect == "luck":
            return f"Increases luck for {self.duration} turns"
        elif self.effect == "remove_poison":
            return "Removes poison effect"
        elif self.effect == "remove_burn":
            return "Removes burning effect"
        return "Unknown effect"

    def use(self, player):
        """
        Applies the item's effect to the player.
        """
        if self.effect == "heal":
            player.health = min(player.health + self.value, player.max_health)
            print(f"You used {self.name}. Your health is now {player.health}/{player.max_health}.")

        elif self.effect == "attack":
            player.attack += self.value
            player.temporary_buffs["attack"] = self.duration
            print(f"You used {self.name}. Your attack increased by {self.value} for {self.duration} turns!")

        elif self.effect == "defense":
            player.temporary_buffs["defense"] = self.value
            print(f"You used {self.name}. Your defense increased by {self.value} for {self.duration} turns!")

        elif self.effect == "max_health":
            player.max_health += self.value
            player.health += self.value  
            print(f"You used {self.name}. Your max health increased by {self.value}!")

        elif self.effect == "luck":
            player.temporary_buffs["luck"] = self.duration
            print(f"You used {self.name}. Your luck increased for {self.duration} turns!")

        elif self.effect == "remove_poison":
            if player.temporary_buffs["poison"] > 0:
                player.temporary_buffs["poison"] = 0
                print(f"You used {self.name}. Poison effect has been removed.")
            else:
                print(f"You used {self.name}, but you were not poisoned.")

        elif self.effect == "remove_burn":
            if player.temporary_buffs["burn"] > 0:
                player.temporary_buffs["burn"] = 0
                print(f"You used {self.name}. Burning effect has been removed.")
            else:
                print(f"You used {self.name}, but you were not burning.")

    def to_dict(self):
        """Converts the item into a dictionary for saving."""
        return {
            "name": self.name,
            "effect": self.effect,
            "value": self.value,
            "duration": self.duration,
            "price": self.price
        }

    @classmethod
    def from_dict(cls, data):
        """Restores an item from a saved dictionary state."""
        return cls(data["name"], data["effect"], data["value"], data["duration"], data["price"])
