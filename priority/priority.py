from abc import ABC, abstractmethod
import gymnasium as gym

class Priority(ABC):
    """
    Базовый класс для всех энергетических обёрток.
    Требует определения статического атрибута `priority`.
    """
    
    # Абстрактное свойство на уровне класса — гарантирует наличие priority
    @property
    @abstractmethod
    def priority(self) -> int:
        """Приоритет обёртки: чем меньше число — тем ближе к ядру среды."""
        pass

    def __init_subclass__(cls, **kwargs):
        """
        Автоматически проверяет при создании подкласса,
        что он определил атрибут `priority` как целое число.
        """
        super().__init_subclass__(**kwargs)
        
        # Проверяем, что priority определён в самом классе (не унаследован)
        if not hasattr(cls, 'priority'):
            raise TypeError(f"Класс {cls.__name__} должен определить атрибут 'priority' (целое число).")
        
        priority = cls.priority
        if not isinstance(priority, int):
            raise TypeError(f"Атрибут 'priority' в {cls.__name__} должен быть целым числом, получено: {type(priority)}")