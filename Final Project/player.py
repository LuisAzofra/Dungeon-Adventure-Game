import random 
from item import Item

class Player:
    """Defines the player character with health, attack power, inventory, gold, and temporary buffs."""

    def __init__(self, name="Hero", health=100, attack=10, gold=0):
        """
        Initializes the player with a name, health, attack power, inventory, gold, and buff system.
        """
        self.name = name
        self.max_health = health  
        self.health = health
        self.attack = attack
        self.gold = gold  # Player can collect and spend gold
        self.inventory = []  
        self.temporary_buffs = {"attack": 0, "defense": 0, "luck": 0, "poison": 0, "burn": 0, "stunned": 0}
        self.pet = None  #Player can have a pet that helps in combat

    def is_alive(self):
        """Returns True if the player's health is above 0, otherwise False."""
        return self.health > 0

    def pick_item(self, item):
        """Adds an item to the player's inventory and displays its effect."""
        self.inventory.append(item)
        print(f"You picked up a {item.name} ({self.get_item_description(item)}).")

    def get_item_description(self, item):
        """Returns a description of an item based on its effect."""
        if item.effect == "heal":
            return f"Restores {item.value} HP"
        elif item.effect == "attack":
            return f"Increases attack by {item.value} for {item.duration} turns"
        elif item.effect == "defense":
            return f"Increases defense by {item.value} for {item.duration} turns"
        elif item.effect == "max_health":
            return f"Permanently increases max health by {item.value}"
        elif item.effect == "luck":
            return f"Increases luck for {item.duration} turns"
        return "Unknown effect"

    def show_inventory(self):
        """Displays the player's inventory with item effects."""
        print("\n=== Inventory ===")
        if not self.inventory:
            print("You have no items.")
        else:
            for i, item in enumerate(self.inventory, 1):
                print(f"[{i}] {item.name} ({self.get_item_description(item)})")
        print("==================")

    def use_item(self, item_choice):
        """
        Uses an item from the inventory based on user selection.
        """
        try:
            item_choice = int(item_choice) - 1  
            if 0 <= item_choice < len(self.inventory):
                item = self.inventory[item_choice]
                item.use(self)
                self.inventory.pop(item_choice)  # Delete item after use
                return
        except ValueError:
            pass

    print("You don't have that item.")

    def earn_gold(self, amount):
        """Adds gold to the player's total."""
        self.gold += amount
        print(f"You collected {amount} gold! You now have {self.gold} gold.")

    def spend_gold(self, amount):
        """Spends gold if the player has enough."""
        if self.gold >= amount:
            self.gold -= amount
            return True
        print("You don't have enough gold!")
        return False

    def adopt_pet(self, pet):
        """Assigns a pet to the player."""
        if self.pet is None:
            self.pet = pet
            print(f"You have adopted {pet.name}! They will now help you in battle.")
        else:
            print("You already have a pet!")

    def show_stats(self):
        """Displays player stats including gold and pet status."""
        print("\n=== Player Stats ===")
        print(f"Name: {self.name}")
        print(f"Health: {self.health}/{self.max_health}")
        print(f"Attack Power: {self.attack}")
        print(f"Gold: {self.gold} coins")
        if self.pet:
            print(f"Pet: {self.pet.name} (Health: {self.pet.health}, Attack: {self.pet.attack})")
        print("====================")

    def update_buffs(self):
        """
        Reduces the duration of temporary buffs after each turn.
        """
        for buff in self.temporary_buffs:
            if self.temporary_buffs[buff] > 0:
                self.temporary_buffs[buff] -= 1
                if self.temporary_buffs[buff] == 0:
                    print(f"{buff.capitalize()} effect has worn off!")

    def fight(self, enemy):
        """Handles turn-based combat between the player and an enemy."""
        while self.is_alive() and enemy.is_alive():
            damage_dealt = self.attack + (5 if self.temporary_buffs["attack"] > 0 else 0)
            print(f"You attack {enemy.name} for {damage_dealt} damage! (Enemy health: {enemy.health - damage_dealt})")
            enemy.health -= damage_dealt

            if enemy.is_alive():
                damage_taken = max(1, enemy.attack - self.temporary_buffs["defense"])
                print(f"{enemy.name} attacks you for {damage_taken} damage! (Your health: {self.health - damage_taken})")
                self.health -= damage_taken
            
            self.update_buffs()  

        if self.is_alive():
            print(f"Congratulations! You defeated {enemy.name}.")
            gold_reward = random.randint(10, 50)
            self.earn_gold(gold_reward)  
        else:
            print("You have been defeated...")

    def to_dict(self):
        """Converts the player's state to a dictionary for saving."""
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "gold": self.gold,
            "inventory": [item.to_dict() for item in self.inventory],
            "temporary_buffs": self.temporary_buffs,
            "pet": self.pet.to_dict() if self.pet else None  
        }

    @classmethod
    def from_dict(cls, data):
        """Loads a player from a dictionary (used when loading a saved game)."""
        player = cls(data["name"], data["max_health"], data["attack"], data["gold"])
        player.health = data["health"]
        player.inventory = [Item.from_dict(item) for item in data["inventory"]]
        player.temporary_buffs = data["temporary_buffs"]
        if data["pet"]:
            from pet import Pet  
            player.pet = Pet.from_dict(data["pet"])  
        return player
