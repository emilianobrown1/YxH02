import pickle

class SafeUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        # Ignore BarracksManager references
        if name == 'BarracksManager':
            return None
        return super().find_class(module, name)

def safe_pickle_loads(data):
    import io
    return SafeUnpickler(io.BytesIO(data)).load()