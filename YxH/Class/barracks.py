from ..Database import db 
import pickle

def __setstate__(self, state):
    # Clean ALL potential barracks-related attributes
    barracks_attrs = [
        'barracks', 'barracks_manager', 'troops',
        'military_units', 'army', 'soldiers',
        'barracks_level', 'military', 'barracks_data'
    ]
    
    # Remove barracks-related keys
    for attr in barracks_attrs:
        state.pop(attr, None)
    
    # Update instance dictionary
    self.__dict__.update(state)
    
    # Initialize new attributes safely
    if not hasattr(self, 'swap'):
        self.swap = {"count": 0}
    if not hasattr(self, 'scramble'):
        self.scramble = []
