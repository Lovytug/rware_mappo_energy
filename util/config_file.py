from pathlib import Path
from typing import Mapping, Optional
import json

class ReadConfigFileSystem:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self._conf_cache = {}

    def _get_conf_path(self, config_name: str) -> Path:
        return self.base_dir / config_name

    def get(self, config_name: str) -> dict:
        if config_name not in self._conf_cache:
            path = self._get_conf_path(config_name)
            with open(path, "r", encoding="utf-8") as f:
                self._conf_cache[config_name] = json.load(f)

        return self._conf_cache[config_name]


class WriteConfigFileSystem:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _resolve_path(self, config_name: str, custom_dir: Optional[Path] = None) -> Path:
        return (custom_dir or self.base_dir) / config_name
    
    def save(
        self,
        data: Mapping,
        config_name: str,
        directory: Optional[Path] = None,
        overwrite: bool = False
    ) -> Path:
        """
        Сохраняет конфиг в JSON.

        :param data: словарь с параметрами
        :param config_name: имя файла
        :param directory: кастомная директория
        :param overwrite: перезаписывать ли файл
        """
        path = self._resolve_path(config_name, directory)

        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists() and not overwrite:
            raise FileExistsError(f"{path} already exists")
        
        save_pretty_json(data, path, indent=4)

        return path
    

def save_pretty_json(data, path: Optional[Path], indent=2):
    """Сохраняет JSON с компактными координатами вида [[x, y], [x, y]]"""
    
    def custom_serialize(obj, level=0):
        indent_str = ' ' * (level * indent)
        
        if isinstance(obj, dict):
            if not obj:
                return '{}'
            items = []
            for i, (key, value) in enumerate(obj.items()):
                serialized = custom_serialize(value, level + 1)
                items.append(f'{indent_str}{" " * indent}"{key}": {serialized}' + (',' if i < len(obj) - 1 else ''))
            return '{\n' + '\n'.join(items) + f'\n{indent_str}}}'
        
        elif isinstance(obj, list):
            if not obj:
                return '[]'
            
            # 🔍 Распознаём список координат: [[x, y], [x, y], ...]
            if all(
                isinstance(item, list) and len(item) == 2 and
                all(isinstance(x, (int, float)) for x in item)
                for item in obj
            ):
                # Компактный формат: [[x, y], [x, y]]
                coords = ', '.join([f'[{x}, {y}]' for x, y in obj])
                return f'[{coords}]'
            
            # Обычный список — форматируем с отступами
            items = []
            for i, item in enumerate(obj):
                serialized = custom_serialize(item, level + 1)
                items.append(f'{indent_str}{" " * indent}{serialized}' + (',' if i < len(obj) - 1 else ''))
            return '[\n' + '\n'.join(items) + f'\n{indent_str}]'
        
        else:
            return json.dumps(obj, ensure_ascii=False)
    
    result = custom_serialize(data, level=0)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(result + '\n')  # добавляем завершающий перенос для чистоты