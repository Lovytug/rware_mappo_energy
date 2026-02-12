import os
import json
from typing import Optional
from read_write_file.writer.base.writer_run_file import WriterFileForRun


class WriterConfigJSON(WriterFileForRun):

    def save(self, data, name_save: str, overwrite=False):
        """
        Сохраняет данные в JSON файл.
        
        Args:
            data: Данные для сохранения
            name_save: Имя файла для сохранения
            overwrite: Перезаписывать ли существующий файл (default: False)
        """

        file_path = os.path.join(self.path, name_save)
        
        if not file_path.endswith('.json'):
            file_path += '.json'
        
        if not overwrite and os.path.exists(file_path):
            raise FileExistsError(f"Файл {file_path} уже существует. Используйте overwrite=True для перезаписи.")
        
        try:
            self.save_pretty_json(data, file_path)
        except (IOError, OSError) as e:
            raise IOError(f"Ошибка при сохранении файла {file_path}: {e}")
        except TypeError as e:
            raise TypeError(f"Данные не могут быть сериализованы в JSON: {e}")


    def save_pretty_json(self, data, path: Optional[str], indent=2):
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