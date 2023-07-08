class Primitives:
    """
    Generic class containing primitives for the state machine.
    """

    @classmethod
    def __getattr__(cls, name):
        for class_ in cls.classes:
            if hasattr(class_, name):
                method = getattr(class_, name)
                return method
        raise AttributeError(f"{cls.__name__} has no attribute '{name}'")
