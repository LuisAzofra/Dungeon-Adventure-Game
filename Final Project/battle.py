import random
from player import Player
from enemy import Enemy

class Battle:
    """Handles turn-based combat between the player (and possibly their pet) against multiple enemies."""

    def __init__(self, player, enemies):
        """
        Initializes a battle instance between the player (and pet) and multiple enemies.
        """
        self.player = player
        self.enemies = enemies  

    def player_turn(self):
        """
        Handles the player's turn where they can attack, use an item, counterattack, or flee.
        """
        print("\nYour turn!")
        print("[1] Attack")
        print("[2] Use Item")
        print("[3] Counterattack (High risk, high reward)")
        print("[4] Try to Flee")

        choice = input("Choose an action: ").strip()

        if choice == "1":
            self.choose_enemy_action("attack")
        elif choice == "2":
            self.player.show_inventory()
            item_choice = input("Choose an item to use: ").strip()
            self.player.use_item(item_choice)
        elif choice == "3":
            self.choose_enemy_action("counterattack")
        elif choice == "4":
            if self.flee():
                return True  # Successfully escaped battle
        else:
            print("Invalid choice! You lose your turn.")

        return False  # Combat continues

    def choose_enemy_action(self, action_type):
        """
        Allows the player to choose which enemy they want to target.
        """
        if len(self.enemies) == 1:
            target_enemy = self.enemies[0]  
        else:
            print("\nChoose an enemy to target:")
            for i, enemy in enumerate(self.enemies, 1):
                print(f"[{i}] {enemy.name} (Health: {enemy.health})")

            try:
                enemy_index = int(input("Select an enemy: ").strip()) - 1
                target_enemy = self.enemies[enemy_index]
            except (ValueError, IndexError):
                print("Invalid choice! You lose your turn.")
                return

        if action_type == "attack":
            self.attack_enemy(target_enemy)
        elif action_type == "counterattack":
            self.counterattack_enemy(target_enemy)

    def attack_enemy(self, enemy):
        """
        Player attacks an enemy. Damage considers temporary buffs.
        """
        damage = self.player.attack + (5 if self.player.temporary_buffs.get("attack", 0) > 0 else 0)
        print(f"You attack {enemy.name} for {damage} damage! (Enemy health: {max(0, enemy.health - damage)})")
        enemy.health -= damage

        if enemy.health <= 0:
            print(f"{enemy.name} has been defeated!")
            self.enemies.remove(enemy)
            gold_reward = random.randint(10, 50)
            self.player.earn_gold(gold_reward)

    def counterattack_enemy(self, enemy):
        """
        Counterattack: 50% success = double damage, 50% fail = no damage.
        """
        print(f"You attempt a counterattack on {enemy.name}...")
        if random.random() < 0.5:
            damage = (self.player.attack * 2)
            print(f"Counterattack successful! You deal {damage} damage! (Enemy health: {max(0, enemy.health - damage)})")
            enemy.health -= damage
        else:
            print("Counterattack failed! You missed your chance to attack.")

    def enemy_turn(self):
        """
        Each enemy takes a turn to attack the player or pet.
        """
        for enemy in self.enemies:
            if not enemy.is_alive():
                continue  

            target = self.choose_target()  
            enemy.attack_player(target)

            # Show updated health for player or pet
            if target == self.player:
                print(f"(Your health: {max(0, self.player.health)})")
            elif target == self.player.pet:
                print(f"({self.player.pet.name}'s health: {max(0, self.player.pet.health)})")

            if not target.is_alive():
                if target == self.player:
                    print("You have been defeated... Game over.")
                    return True
                elif target == self.player.pet:
                    print(f"{self.player.pet.name} has fallen in battle!")

        return False  

    def choose_target(self):
        """
        Determines if the enemy attacks the player or their pet.
        """
        if self.player.pet and random.random() < 0.5:  
            return self.player.pet
        return self.player

    def flee(self):
        """
        Player attempts to flee from battle. Chance is lower with more enemies.
        """
        escape_chance = max(10, 40 - (len(self.enemies) * 10))  
        print(f"Escape chance: {escape_chance}% (More enemies = lower chance)")

        if random.randint(1, 100) <= escape_chance:
            print("You successfully escaped the battle!")
            return True
        else:
            print("Failed to escape!")
            return False

    def apply_status_effects(self):
        """
        Applies ongoing status effects to the player (Poison, Burn).
        """
        if self.player.temporary_buffs.get("poison", 0) > 0:
            print("Poison effect! You take 3 extra damage.")
            self.player.health -= 3
            self.player.temporary_buffs["poison"] -= 1  

        if self.player.temporary_buffs.get("burn", 0) > 0:
            print("Burning effect! You take 5 extra damage.")
            self.player.health -= 5
            self.player.temporary_buffs["burn"] -= 1  

    def pet_turn(self):
        """
        If the player has a pet, the pet attacks a random enemy.
        """
        if not self.player.pet or not self.enemies:
            return

        target = random.choice(self.enemies)
        print(f"{self.player.pet.name} attacks {target.name} for {self.player.pet.attack} damage!")
        target.health -= self.player.pet.attack

        if target.health <= 0:
            print(f"{target.name} has been defeated!")
            self.enemies.remove(target)

    def start(self):
        """
        Starts the battle loop where the player, pet, and enemies take turns.
        """
        print(f"\nA battle begins! You are facing {len(self.enemies)} enemy(s)!")
        while self.player.is_alive() and self.enemies:
            self.apply_status_effects()  

            escaped = self.player_turn()
            if escaped:
                return  

            self.pet_turn()  

            if self.enemy_turn():
                return  

            self.player.update_buffs()  

        if self.player.is_alive():
            print("You won the battle!")
        else:
            print("You were defeated...")
