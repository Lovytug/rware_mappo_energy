from types import SimpleNamespace

class EnvObserver:
    def __init__(self):
        self._getters = {}

    def register(self, obj):
        """
        Регистрирует все @observer-property у объектов
        """
        for attr_name in dir(type(obj)):
            attr = getattr(type(obj), attr_name, None)

            if getattr(attr, "__is_observable__", False):
                self._getters[attr_name] = lambda o=obj, a=attr_name: getattr(o, a)

    def snapshot(self):
        """
        возращает snapshot состояния среды
        """
        return SimpleNamespace(**{
            name: getter() for name, getter in self._getters.items()
        })
    
    def merge(self, other: 'EnvObserver') -> 'EnvObserver':
        """
        Создаёт новый EnvObserver, объединяющий наблюдаемые свойства из self и other.
        В случае конфликта имён — побеждает other (можно изменить по желанию).
        """
        merged = EnvObserver()
        merged._getters = {**self._getters, **other._getters}
        return merged

    def __add__(self, other: 'EnvObserver') -> 'EnvObserver':
        """Позволяет писать obs1 + obs2"""
        if not isinstance(other, EnvObserver):
            return NotImplemented
        return self.merge(other)

    def __iadd__(self, other: 'EnvObserver') -> 'EnvObserver':
        """Позволяет писать obs1 += obs2 (модифицирует текущий объект)"""
        if not isinstance(other, EnvObserver):
            return NotImplemented
        self._getters.update(other._getters)
        return self