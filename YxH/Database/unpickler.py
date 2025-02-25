import pickle

import pickle

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Replace BarracksManager with a dummy class to avoid errors
        if name == 'BarracksManager':
            class DummyBarracksManager:
                pass
            return DummyBarracksManager
        return super().find_class(module, name)

def safe_pickle_loads(data):
    import io
    return SafeUnpickler(io.BytesIO(data)).load()