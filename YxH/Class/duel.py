from ..Database import db
from ..Class.user import User
from ..Database.users import get_user
from ..Database.characters import get_anime_character
import pickle
import random

CHARACTERS = {
    "Boa Hancock": {
        "name": "Boa Hancock",
        "hp": 90,
        "abilities": ["Love Beam", "Slave Arrow", "Pistol Kiss", "Charm Strike"],
        "defense": 18,
        "speed": 22,
        "power": 24,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Gojo": {
        "name": "Gojo",
        "hp": 100,
        "abilities": ["Limitless", "Hollow Purple", "Reversal Red", "Infinity Hold"],
        "defense": 22,
        "speed": 23,
        "power": 28,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Hinata": {
        "name": "Hinata",
        "hp": 85,
        "abilities": ["Gentle Fist", "Twin Lion Fists", "Byakugan Strike", "Palm Rotation"],
        "defense": 17,
        "speed": 21,
        "power": 20,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Kakashi": {
        "name": "Kakashi",
        "hp": 90,
        "abilities": ["Chidori", "Lightning Blade", "Sharingan Strike", "Kunai Barrage"],
        "defense": 20,
        "speed": 25,
        "power": 26,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Levi": {
        "name": "Levi",
        "hp": 95,
        "abilities": ["Spin Slash", "Thunder Spears", "3D Maneuver", "Precision Cut"],
        "defense": 20,
        "speed": 27,
        "power": 25,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.3]
    },
    "Light": {
        "name": "Light",
        "hp": 80,
        "abilities": ["Death Note", "Judgment", "Mind Trap", "Deceit"],
        "defense": 12,
        "speed": 18,
        "power": 30,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.5]
    },
    "Luffy": {
        "name": "Luffy",
        "hp": 100,
        "abilities": ["Gum-Gum Pistol", "Gear Second", "Red Hawk", "Jet Gatling"],
        "defense": 19,
        "speed": 23,
        "power": 30,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Mitsuri": {
        "name": "Mitsuri",
        "hp": 90,
        "abilities": ["Whip Slash", "Love Spiral", "Serpent Strike", "Agile Dance"],
        "defense": 16,
        "speed": 24,
        "power": 22,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Nami": {
        "name": "Nami",
        "hp": 85,
        "abilities": ["Thunder Tempo", "Cyclone Burst", "Weather Trap", "Cloud Shock"],
        "defense": 14,
        "speed": 20,
        "power": 18,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Naruto": {
        "name": "Naruto",
        "hp": 100,
        "abilities": ["Rasengan", "Shadow Clones", "Wind Slash", "Chakra Punch"],
        "defense": 15,
        "speed": 20,
        "power": 28,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Nezuko": {
        "name": "Nezuko",
        "hp": 90,
        "abilities": ["Blood Burst", "Claw Swipe", "Flame Kick", "Resilient Rush"],
        "defense": 18,
        "speed": 22,
        "power": 23,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Rengoku": {
        "name": "Rengoku",
        "hp": 95,
        "abilities": ["Flame Breathing", "Blazing Slash", "Fire Tornado", "Burning Fury"],
        "defense": 20,
        "speed": 21,
        "power": 27,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Sakura": {
        "name": "Sakura",
        "hp": 95,
        "abilities": ["Chakra Smash", "Medical Palm", "Roaring Punch", "Healing Surge"],
        "defense": 19,
        "speed": 20,
        "power": 24,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Sanji": {
        "name": "Sanji",
        "hp": 95,
        "abilities": ["Diable Jambe", "Kick Barrage", "Sky Walk", "Fire Spin"],
        "defense": 18,
        "speed": 25,
        "power": 26,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Sasuke": {
        "name": "Sasuke",
        "hp": 95,
        "abilities": ["Chidori Spear", "Amaterasu", "Inferno Slash", "Rinnegan Pull"],
        "defense": 20,
        "speed": 24,
        "power": 28,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Sung Jin-Woo": {
        "name": "Sung Jin-Woo",
        "hp": 100,
        "abilities": ["Shadow Slash", "Monarch's Domain", "Stealth Step", "Summon Army"],
        "defense": 22,
        "speed": 24,
        "power": 30,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Tanjiro": {
        "name": "Tanjiro",
        "hp": 90,
        "abilities": ["Water Wheel", "Sun Breathing", "Constant Flux", "Smell Sense"],
        "defense": 17,
        "speed": 21,
        "power": 23,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Zenitsu": {
        "name": "Zenitsu",
        "hp": 85,
        "abilities": ["Thunderclap", "Sixfold Strike", "Lightning Dash", "Faint Counter"],
        "defense": 14,
        "speed": 28,
        "power": 25,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Zoro": {
        "name": "Zoro",
        "hp": 100,
        "abilities": ["Three Sword Style", "Oni Giri", "Dragon Twister", "Asura Strike"],
        "defense": 21,
        "speed": 22,
        "power": 30,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Goku": {
        "name": "Goku",
        "hp": 110,
        "abilities": ["Kamehameha", "Instant Transmission", "Spirit Bomb", "Ultra Instinct"],
        "defense": 23,
        "speed": 26,
        "power": 35,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    },
    "Vegeta": {
        "name": "Vegeta",
        "hp": 105,
        "abilities": ["Final Flash", "Galick Gun", "Big Bang Attack", "Saiyan Rage"],
        "defense": 22,
        "speed": 25,
        "power": 33,
        "ability_modifiers": [0.1, 0.2, 0.3, 0.4]
    }
}

class Duel:
    def __init__(self, user1_id, user2_id, char1=None, char2=None):
        self.player_ids = [user1_id, user2_id]
        self.players = {
            user1_id: char1 if char1 else self.random_character(),
            user2_id: char2 if char2 else self.random_character()
        }
        self.health = {
            user1_id: self.players[user1_id]['hp'],
            user2_id: self.players[user2_id]['hp']
        }
        self.turn = user1_id
        self.log = []
        self.heal_cooldown = {user1_id: 0, user2_id: 0}
        self.ability_cooldowns = {
            user1_id: [0, 0, 0, 0],
            user2_id: [0, 0, 0, 0]
        }

    def random_character(self):
        from ..Class.duel import CHARACTERS
        name = random.choice(list(CHARACTERS.keys()))
        return {**CHARACTERS[name], 'name': name}

    def opponent(self, user_id):
        return self.player_ids[1] if user_id == self.player_ids[0] else self.player_ids[0]

    def is_finished(self):
        return any(hp <= 0 for hp in self.health.values())

    def calculate_damage(self, attacker, defender, ability_index):
        base_damage = (attacker['power'] * attacker['ability_modifiers'][ability_index] +
                      attacker['speed'] * 0.5) - (defender['defense'] * 0.3)

        variance = random.randint(-3, 3 + ability_index * 2)
        return max(5, int(base_damage + variance))

    def use_ability(self, user_id, ability_index):
        if self.ability_cooldowns[user_id][ability_index] > 0:
            return 0

        attacker = self.players[user_id]
        defender_id = self.opponent(user_id)
        defender = self.players[defender_id]

        damage = self.calculate_damage(attacker, defender, ability_index)
        self.health[defender_id] -= damage

        # Set cooldown based on ability strength
        self.ability_cooldowns[user_id][ability_index] = ability_index + 1

        # Special effects
        if ability_index == 3:  # Ultimate ability
            heal_amount = int(damage * 0.2)
            self.health[user_id] = min(attacker['hp'], self.health[user_id] + heal_amount)
            self.log.append(f"{attacker['name']}'s {attacker['abilities'][ability_index]} dealt {damage} damage and healed {heal_amount} HP!")
        else:
            self.log.append(f"{attacker['name']} used {attacker['abilities'][ability_index]} for {damage} damage!")

        self.turn = defender_id
        return damage

    def heal(self, user_id):
        if self.heal_cooldown[user_id] > 0:
            return 0

        player = self.players[user_id]
        heal_amount = min(int(player['hp'] * 0.25), player['hp'] - self.health[user_id])
        self.health[user_id] += heal_amount
        self.heal_cooldown[user_id] = 3
        self.log.append(f"{player['name']} healed for {heal_amount} HP!")
        self.turn = self.opponent(user_id)
        return heal_amount

    def update_cooldowns(self):
        for player_id in self.player_ids:
            if self.heal_cooldown[player_id] > 0:
                self.heal_cooldown[player_id] -= 1
            for i in range(4):
                if self.ability_cooldowns[player_id][i] > 0:
                    self.ability_cooldowns[player_id][i] -= 1

    def get_status(self, user_id):
        player = self.players[user_id]
        hp = self.health[user_id]
        cooldown = self.heal_cooldown[user_id]
        ability_cooldowns = ", ".join(str(cd) for cd in self.ability_cooldowns[user_id])
        return (f"{player['name']} HP: {hp}/{player['hp']}\n"
                f"Heal CD: {cooldown} turns | Ability CDs: [{ability_cooldowns}]")

    def get_health_bar(self, user_id, length=20):
        hp = self.health[user_id]
        max_hp = self.players[user_id]['hp']
        filled_len = int(length * hp / max_hp)
        bar = "█" * filled_len + "░" * (length - filled_len)
        return f"[{bar}] {hp}/{max_hp}"

    def get_log(self):
        return "\n".join(self.log[-5:])

    async def reward_winner(self, winner_id):
        from ..Database.users import get_user
        from ..Database.characters import get_anime_character
        loser_id = self.opponent(winner_id)
        winner = await get_user(winner_id)
        loser = await get_user(loser_id)

        transfer_msg = ""
        if loser.collection:
            import random
            stolen_char_id = random.choice(list(loser.collection.keys()))
            loser.collection[stolen_char_id] -= 1
            if loser.collection[stolen_char_id] <= 0:
                del loser.collection[stolen_char_id]

            winner.collection[stolen_char_id] = winner.collection.get(stolen_char_id, 0) + 1

            await winner.update()
            await loser.update()

            char = await get_anime_character(stolen_char_id)
            transfer_msg = f"\n\n🏆 Won {char.name} (ID: {stolen_char_id}) from opponent!"

        return transfer_msg


class Arena:
    def __init__(self, user1_id, user2_id):
        self.player_ids = [user1_id, user2_id]
        self.players = {
            user1_id: [self.random_character(), self.random_character()],
            user2_id: [self.random_character(), self.random_character()]
        }
        self.scores = {user1_id: 0, user2_id: 0}
        self.rounds = []
        self.current_round = 0
        self.active_duel = None
        self.finished = False

    def random_character(self):
        name = random.choice(list(CHARACTERS.keys()))
        return {**CHARACTERS[name], 'name': name}

    def start_next_round(self):
        self.current_round += 1
        if self.current_round > 2 or self.finished:
            return False

        p1_char = self.players[self.player_ids[0]][self.current_round-1]
        p2_char = self.players[self.player_ids[1]][self.current_round-1]

        self.active_duel = Duel(
            self.player_ids[0],
            self.player_ids[1],
            char1=p1_char,
            char2=p2_char
        )
        return True

    def process_round_result(self):
        if not self.active_duel.is_finished():
            return False

        winner = max(self.active_duel.health, key=lambda x: self.active_duel.health[x])
        self.scores[winner] += 1
        self.rounds.append(winner)

        if self.scores[self.player_ids[0]] >= 2 or self.scores[self.player_ids[1]] >= 2:
            self.finished = True
        elif self.current_round == 2: # Check for draw after 2 rounds
            if self.scores[self.player_ids[0]] == self.scores[self.player_ids[1]]:
                self.finished = True
        return True

    def get_round_characters(self):
        round_index = min(self.current_round - 1, 1)  # Ensure index is within 0 or 1
        return (
            self.players[self.player_ids[0]][round_index]['name'],
            self.players[self.player_ids[1]][round_index]['name']
        )

    def get_arena_status(self):
        p1_score = self.scores[self.player_ids[0]]
        p2_score = self.scores[self.player_ids[1]]
        round_num = self.current_round
        status = f"🏟️ Arena Status (Round {round_num}/2)\n"
        status += f"{self.players[self.player_ids[0]][0]['name']} ({self.player_ids[0]}): {p1_score}\n"
        status += f"{self.players[self.player_ids[1]][0]['name']} ({self.player_ids[1]}): {p2_score}\n"
        if self.active_duel:
            status += f"\n--- Current Round Duel ---\n"
            status += f"{self.active_duel.players[self.player_ids[0]]['name']} HP: {self.active_duel.health[self.player_ids[0]]}/{self.active_duel.players[self.player_ids[0]]['hp']}\n"
            status += f"{self.active_duel.players[self.player_ids[1]]['name']} HP: {self.active_duel.health[self.player_ids[1]]}/{self.active_duel.players[self.player_ids[1]]['hp']}\n"
            status += f"Turn: {self.active_duel.players[self.active_duel.turn]['name']} ({self.active_duel.turn})\n"
            status += f"Log: {self.active_duel.get_log()}"
        return status

    async def reward_players(self):
        from ..Database.users import get_user
        player1_id = self.player_ids[0]
        player2_id = self.player_ids[1]

        winner_id = None
        if self.scores[player1_id] > self.scores[player2_id]:
            winner_id = player1_id
            loser_id = player2_id
        elif self.scores[player2_id] > self.scores[player1_id]:
            winner_id = player2_id
            loser_id = player1_id
        else:
            # Draw condition
            winner1 = await get_user(player1_id)
            winner2 = await get_user(player2_id)
            winner1.crystals += 1
            winner2.crystals += 1
            await winner1.update()
            await winner2.update()
            return None, None  # Indicate a draw

        winner = await get_user(winner_id)
        loser = await get_user(loser_id)

        winner.crystals += 3
        loser.crystals += 1
        await winner.update()
        await loser.update()
        return winner_id, loser_id

    def get_final_results(self):
        p1_id = self.player_ids[0]
        p2_id = self.player_ids[1]
        p1_score = self.scores[p1_id]
        p2_score = self.scores[p2_id]

        if p1_score > p2_score:
            return p1_id, p2_id, "won"
        elif p2_score > p1_score:
            return p2_id, p1_id, "won"
        else:
            return p1_id, p2_id, "draw"
