 from datetime import datetime

class UserWordle:
    def __init__(self):
        self.games = []
        self.daily_limit = 20
        self.daily_games = {}

    def add_game(self, word: str, attempts: List[str], success: bool):
        game = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'word': word,
            'attempts': attempts,
            'success': success
        }
        self.games.append(game)
        self.increment_daily_game()

    def increment_daily_game(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.daily_games[today] = self.daily_games.get(today, 0) + 1

    def get_today_games(self) -> List[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        return [game for game in self.games if game['date'] == today]

    def get_today_game_count(self) -> int:
        today = datetime.now().strftime("%Y-%m-%d")
        return self.daily_games.get(today, 0)

    def can_play_today(self) -> bool:
        return self.get_today_game_count() < self.daily_limit

    def get_stats(self) -> Dict:
        total_games = len(self.games)
        wins = sum(1 for game in self.games if game['success'])
        average_attempts = sum(len(game['attempts']) for game in self.games) / total_games if total_games > 0 else 0

        return {
            'total_games': total_games,
            'wins': wins,
            'win_rate': (wins / total_games) * 100 if total_games > 0 else 0,
            'average_attempts': average_attempts
        }

    def get_average_attempts(self) -> List[int]:
        return [len(game['attempts']) for game in self.games if game['success']]

    def to_dict(self) -> Dict:
        return {
            'games': self.games,
            'daily_limit': self.daily_limit,
            'daily_games': self.daily_games
        }

    @classmethod
    def from_dict(cls, data: Dict):
        wordle = cls()
        wordle.games = data.get('games', [])
        wordle.daily_limit = data.get('daily_limit', 20)
        wordle.daily_games = data.get('daily_games', {})
        return wordle
