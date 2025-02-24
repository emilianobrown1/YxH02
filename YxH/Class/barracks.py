def __setstate__(self, state):
        # Remove barracks-related attributes from the state before updating
        state.pop('barracks_manager', None)
        state.pop('troops', None)
        state.pop('barracks', None)
        # Update the instance's __dict__ with the cleaned state
        self.__dict__.update(state)