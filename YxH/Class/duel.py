from ..Database import db
from ..class.user import User  # Ensure this import path is correct
import pickle
import random

# Anime characters with stats
CHARACTERS = {
    "Naruto": {"hp": 100, "attack": 25, "defense": 15, "speed": 20, "special": 35},
    "Kakashi": {"hp": 90, "attack": 22, "defense": 20, "speed": 25, "special": 30},
    "Hinata": {"hp": 85, "attack": 20, "defense": 18, "speed": 28, "special": 32},
    "Sasuke": {"hp": 95, "attack": 28, "defense": 16, "speed": 22, "special": 33},
    "Sakura": {"hp": 90, "attack": 23, "defense": 22, "speed": 18, "special": 30},
    "Luffy": {"hp": 110, "attack": 30, "defense": 17, "speed": 19, "special": 29},
    "Nami": {"hp": 80, "attack": 18, "defense": 15, "speed": 30, "special": 25},
    "Zoro": {"hp": 105, "attack": 32, "defense": 19, "speed": 15, "special": 28},
    "Light": {"hp": 85, "attack": 24, "defense": 17, "speed": 25, "special": 35},
    "Sung Jin-Woo": {"hp": 95, "attack": 28, "defense": 20, "speed": 20, "special": 40},
    "Boa Hancock": {"hp": 90, "attack": 26, "defense": 18, "speed": 22, "special": 33},
    "Rengoku": {"hp": 100, "attack": 29, "defense": 21, "speed": 17, "special": 31},
    "Zenitsu": {"hp": 80, "attack": 20, "defense": 15, "speed": 35, "special": 27},
    "Levi": {"hp": 85, "attack": 27, "defense": 20, "speed": 30, "special": 28},
    "Sanji": {"hp": 95, "attack": 28, "defense": 18, "speed": 25, "special": 29},
    "Mitsuri": {"hp": 90, "attack": 22, "defense": 17, "speed": 28, "special": 31},
    "Nezuko": {"hp": 100, "attack": 26, "defense": 19, "speed": 20, "special": 30},
    "Tanjiro": {"hp": 95, "attack": 27, "defense": 20, "speed": 22, "special": 32},
    "Gojo": {"hp": 100, "attack": 30, "defense": 22, "speed": 23, "special": 40},
}

class Duel:
    def __init__(self, user1_id, user2_id):
        self.user1 = User(user1_id)
        self.user2 = User(user2_id)

        self.players = {
            user1_id: self.random_character(),
            user2_id: self.random_character()
        }

        self.health = {
            user1_id: self.players[user1_id]['hp'],
            user2_id: self.players[user2_id]['hp']
        }

        self.turn = user1_id
        self.log = []

    def random_character(self):
        name = random.choice(list(CHARACTERS.keys()))
        stats = CHARACTERS[name].copy()
        stats['name'] = name
        return stats

    def opponent(self, user_id):
        return self.user2.id if user_id == self.user1.id else self.user1.id

    def is_finished(self):
        return any(hp <= 0 for hp in self.health.values())

    def attack(self, user_id):
        attacker = self.players[user_id]
        defender_id = self.opponent(user_id)
        defender = self.players[defender_id]

        base_damage = attacker["attack"] - (defender["defense"] * 0.5)
        damage = max(5, int(base_damage + random.randint(-3, 3)))
        self.health[defender_id] -= damage

        self.log.append(f"{attacker['name']} attacked {defender['name']} for {damage} damage!")
        self.turn = defender_id
        return damage

    def special(self, user_id):
        attacker = self.players[user_id]
        defender_id = self.opponent(user_id)
        defender = self.players[defender_id]

        base_damage = attacker["special"] - (defender["defense"] * 0.3)
        damage = max(8, int(base_damage + random.randint(-5, 5)))
        self.health[defender_id] -= damage

        self.log.append(f"{attacker['name']} used SPECIAL on {defender['name']} for {damage} damage!")
        self.turn = defender_id
        return damage

    def heal(self, user_id):
        player = self.players[user_id]
        heal_amount = int(player["hp"] * 0.2)
        self.health[user_id] = min(self.health[user_id] + heal_amount, player["hp"])

        self.log.append(f"{player['name']} healed for {heal_amount} HP!")
        self.turn = self.opponent(user_id)
        return heal_amount

    def get_status(self, user_id):
        player = self.players[user_id]
        hp = self.health[user_id]
        return f"{player['name']} HP: {hp}/{player['hp']}"

    def get_health_bar(self, user_id, length=20):
        hp = self.health[user_id]
        max_hp = self.players[user_id]['hp']
        filled_len = int(length * hp / max_hp)
        bar = "█" * filled_len + "░" * (length - filled_len)
        return f"[{bar}] {hp}/{max_hp}"

    def get_log(self):
        return "\n".join(self.log[-5:])  # last 5 entries

    def reward_winner(self, winner_id):
        loser_id = self.opponent(winner_id)
        winner = self.user1 if winner_id == self.user1.id else self.user2
        loser = self.user1 if winner_id != self.user1.id else self.user2

        if not loser.characters:
            self.log.append("Loser had no characters to steal.")
            return None

        stolen_char = random.choice(loser.characters)
        loser.characters.remove(stolen_char)
        winner.characters.append(stolen_char)

        self.log.append(f"{winner.name} won the duel and stole character ID {stolen_char} from {loser.name}.")

        # Save changes to DB
        winner.update()
        loser.update()

        return stolen_char