# This isn't used anywhere
# TODO: TD4 Determine if this file is required and remove it if not

class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class Singleton(metaclass=SingletonMeta):
    pass