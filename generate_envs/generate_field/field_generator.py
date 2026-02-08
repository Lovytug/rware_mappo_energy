from generate_envs.generate_field.generate_blocks import GenerateRandomBlocks
from abc import ABC, abstractmethod
from typing import Any
import random

class FieldGenerator(ABC):
    phase: int

    @abstractmethod
    def can_handle(self, field_cfg: dict) -> bool:
        pass

    @abstractmethod
    def generate(self, name: str, cfg: dict, ctx) -> Any:
        pass
    

class ScalerGenerator(FieldGenerator):
    phase = 0
    SCALER_TYPE = ("int", "float", "double", "string")

    def can_handle(self, field_cfg):
        return field_cfg.get('type') in self.SCALER_TYPE
    
    def generate(self, name, cfg, ctx):
        if cfg['type'] == 'int':
            value = self._generate_int(name, cfg)
        elif cfg['type'] == "float":
            value = self._generate_float(name, cfg)
        elif cfg['type'] == "string":
            value = self._generate_string(name, cfg)
        
        ctx.set(name, value)

        return value

    def _generate_int(self, name: str, cfg: dict):
        if 'value' in cfg:
            return cfg['value']
        elif 'range' in cfg:
            return random.randint(*cfg['range'])
        else:
            raise ValueError(f'Неуказана или некорректно написан тип операции над числом для {name}. Пришлом {cfg}')
        
    def _generate_float(self, name: str, cfg: dict):
        if 'value' in cfg:
            return cfg['value']
        elif 'range' in cfg:
            return random.uniform(*cfg['range'])
        else:
            raise ValueError(f'Неуказана или некорректно написан тип операции над числом для {name}. Пришлом {cfg}')
        

    def _generate_string(self, name: str, cfg: dict):
        if 'value' in cfg:
            return cfg['value']
        else:
            raise ValueError(f'Неуказана или некорректно написан тип операции над числом для {name}. Пришлом {cfg}')
        

class CoordListGenerator(FieldGenerator):
    phase = 1

    def can_handle(self, field_cfg):
        return field_cfg.get('type') == "list" and field_cfg['item']['type'] == "coord"
    
    def generate(self, name: str, cfg: dict, ctx):
        count = self._generate_count(name, cfg)

        generator = GenerateRandomBlocks(
            width=ctx.get('width'),
            height=ctx.get('height'),
            count_blocks=count,
            occupied=ctx.occupied
        )

        coords = generator.generate()
        ctx.occupied.update(coords)

        return [list(coord) for coord in coords]

    def _generate_count(self, name: str, cfg: dict) -> int:
        count_cfg = cfg['count']

        if count_cfg['type'] == 'int':
            count = self._generate_int(name, count_cfg)
        else:
            raise ValueError(f'count для {name} должен быть int. Пришлом {cfg}')
        
        return count
    
    def _generate_int(self, name: str, cfg: dict):
        if 'value' in cfg:
            return cfg['value']
        elif 'range' in cfg:
            return random.randint(*cfg['range'])
        else:
            raise ValueError(f'Неуказана или некорректно написан тип операции над числом для {name}. Пришлом {cfg}')