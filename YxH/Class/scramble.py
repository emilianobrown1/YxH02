from ..Database.clan import db
import pickle

class Scramble: 
def __init__ reset_daily_state(self):
        if datetime.today().date() != self.last_played_date:
            self.scramble_progress = {
                'incorrect_attempts': 0,
                'stops': 0,
                'skips': 0,
                'count': 0,
                'completed': False,
                'blocked_until': None
            }
            self.daily_skips = 0
            self.last_played_date = datetime.today().date()