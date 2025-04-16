import random
from item import Item
from pet import Pet

class Vendor:
    """Handles the in-game shop where the player can buy and sell items or adopt pets."""

    def __init__(self):
        """
        Initializes the vendor with random items for sale.
        Some rare items and pets may appear occasionally.
        """
        self.items_for_sale = [
            Item("Small Healing Potion", "heal", 20, None, 10),
            Item("Medium Healing Potion", "heal", 50, None, 25),
            Item("Large Healing Potion", "heal", 100, None, 50),
            Item("Minor Strength Potion", "attack", 5, 3, 20),
            Item("Iron Skin Potion", "defense", 3, 4, 25),
            Item("Max Health Elixir", "max_health", 50, None, 150),
            Item("Luck Charm", "luck", 2, 5, 60),
            Item("Anti-Poison Potion", "remove_poison", None, None, 30),
            Item("Fire Resistance Potion", "remove_burn", None, None, 30)
        ]

        self.rare_items = [
            Item("Warrior's Fury", "attack", 15, 5, 75),
            Item("Titan's Elixir", "defense", 5, 6, 50),
            Item("Elixir of Life", "heal", 200, None, 100)
        ]

        self.pet_for_sale = None
        if random.random() < 0.3:  # 30% chance vendor has a pet for sale
            self.pet_for_sale = Pet()

    def show_shop(self, player):
        """Displays the available items and allows the player to make purchases."""
        print("\n=== Vendor Shop ===")
        print(f"Your Gold: {player.gold} coins")

        for i, item in enumerate(self.items_for_sale, 1):
           print(f"[{i}] {item.name} ({item.get_item_description()}) - {item.price} Gold")

        if random.random() < 0.5:  # 50% chance to sell a rare item
            rare_item = random.choice(self.rare_items)
            self.items_for_sale.append(rare_item)
            print(f"[{len(self.items_for_sale)}] {rare_item.name} ({rare_item.get_item_description()}) - {rare_item.price} Gold")


        if self.pet_for_sale:
            print(f"\n[99] Adopt {self.pet_for_sale.name} (Health: {self.pet_for_sale.health}, Attack: {self.pet_for_sale.attack}) - 100 Gold")

        print("[0] Exit Shop")

        choice = input("\nChoose an item number to buy (or 0 to leave): ").strip()

        if choice == "0":
            print("You leave the shop.")
            return

        if choice == "99" and self.pet_for_sale:
            self.buy_pet(player)
        else:
            try:
                item_index = int(choice) - 1
                self.buy_item(player, self.items_for_sale[item_index])
            except (ValueError, IndexError):
                print("Invalid choice!")

    def buy_item(self, player, item):
        """Handles item purchases."""
        if player.spend_gold(item.price):
            player.pick_item(item)
            print(f"You bought {item.name} for {item.price} gold!")
        else:
            print("You don't have enough gold.")

    def buy_pet(self, player):
        """Handles pet adoption."""
        if not self.pet_for_sale:
            print("No pet is available right now.")
            return

        if player.spend_gold(100):
            player.adopt_pet(self.pet_for_sale)
            print(f"You adopted {self.pet_for_sale.name}!")
            self.pet_for_sale = None  # The pet is no longer for sale
        else:
            print("You don't have enough gold.")

    def sell_items(self, player):
        """Allows the player to sell items from their inventory for gold."""
        if not player.inventory:
            print("You have no items to sell.")
            return

        print("\n=== Sell Items ===")
        for i, item in enumerate(player.inventory, 1):
            sell_price = item.price // 2  # Sell for half the price
            print(f"[{i}] {item.name} ({item.get_item_description(item)}) - Sell for {sell_price} Gold")

        print("[0] Exit Selling")

        choice = input("\nChoose an item to sell (or 0 to leave): ").strip()

        if choice == "0":
            return

        try:
            item_index = int(choice) - 1
            item_to_sell = player.inventory[item_index]
            sell_price = item_to_sell.price // 2

            player.earn_gold(sell_price)
            print(f"You sold {item_to_sell.name} for {sell_price} gold!")
            player.inventory.pop(item_index)

        except (ValueError, IndexError):
            print("Invalid choice!")
