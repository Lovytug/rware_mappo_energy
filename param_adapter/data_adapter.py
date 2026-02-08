from abc import ABC, abstractmethod
from typing import Any

class DataAdapter(ABC):
    
    def __init__(self, config_data):
        self.cfg = config_data

    @abstractmethod
    def extract(self) -> Any:
        pass
        

