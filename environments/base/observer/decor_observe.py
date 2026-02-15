class ObservableProperty(property):
    """Расширенный property с поддержкой метаданных для наблюдателя."""
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super().__init__(fget, fset, fdel, doc)
        self.__is_observable__ = True


def observe(func):
    """Декоратор для пометки свойства как наблюдаемого."""
    return ObservableProperty(func)