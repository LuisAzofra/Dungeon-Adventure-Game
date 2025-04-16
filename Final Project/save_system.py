import json

class SaveSystem:
    """Handles saving and loading the game state to/from a JSON file."""

    SAVE_FILE = "savegame.json"

    @staticmethod
    def save_game(player, dungeon):
        """
        Saves the game state (player, dungeon, inventory, gold, and pet) into a JSON file.
        If the player's pet is dead, it will not be saved.
        """
        try:
            save_data = {
                "player": player.to_dict(),
                "dungeon": dungeon.to_dict()
            }

            if player.pet and player.pet.is_alive():
                save_data["player"]["pet"] = player.pet.to_dict()
            else:
                save_data["player"]["pet"] = None  

            with open(SaveSystem.SAVE_FILE, "w") as f:
                json.dump(save_data, f, indent=4)
            print("\nGame saved successfully!")
        except Exception as e:
            print(f"Error saving game: {e}")

    @staticmethod
    def load_game():
        """
        Loads the game state from the JSON file, if it exists.
        Returns a dictionary containing player and dungeon data.
        """
        try:
            with open(SaveSystem.SAVE_FILE, "r") as f:
                data = json.load(f)

            return data
        except FileNotFoundError:
            print("\nNo save file found. Starting a new game.")
            return None
        except json.JSONDecodeError:
            print("\nError loading save file. The data might be corrupted.")
            return None
