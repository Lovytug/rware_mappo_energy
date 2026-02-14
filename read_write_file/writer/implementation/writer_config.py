import os
import json
from typing import Optional
from read_write_file.writer.base.writer_run_file import WriterConcreteFileNameForRunEpisode


class WriterConfigJSON(WriterConcreteFileNameForRunEpisode):
    """
    Класс для сохранения данных в JSON с красивым форматированием.
    Поддерживает перезапись и дозапись данных.
    """

    def save(self, data, overwrite=False, append=False):
        """
        Сохраняет данные в JSON файл.

        Args:
            data: Данные для сохранения (dict или list)
            overwrite: Перезаписывать ли существующий файл
            append: Дозаписывать данные к существующему файлу
        """
        file_path = self.path
        if not file_path.endswith('.json'):
            file_path += '.json'

        if os.path.exists(file_path):
            if overwrite:
                pass  # просто перезаписываем
            elif append:
                data = self._merge_with_existing(data, file_path)
            else:
                raise FileExistsError(
                    f"Файл {file_path} уже существует. Используйте overwrite=True или append=True."
                )

        self._save_pretty_json(data, file_path)

    def _merge_with_existing(self, new_data, path: str):
        """
        Загружает существующие данные и объединяет их с новыми.
        Поддерживает списки и словари.
        """
        try:
            with open(path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл пустой или невалидный, возвращаем новые данные
            return new_data

        # Если оба объекта — списки, объединяем элементы
        if isinstance(existing_data, list) and isinstance(new_data, list):
            return existing_data + new_data
        # Если оба объекта — словари, обновляем ключи
        elif isinstance(existing_data, dict) and isinstance(new_data, dict):
            merged = existing_data.copy()
            merged.update(new_data)
            return merged
        # Невозможно объединить разные типы
        else:
            raise TypeError(
                "Невозможно дозаписать: существующие данные и новые данные несовместимы"
            )

    def _save_pretty_json(self, data, path: str, indent: int = 2):
        """
        Сохраняет данные в JSON с красивым форматированием.
        Компактно форматирует координаты вида [[x, y], [x, y]].
        """

        def serialize(obj, level=0):
            indent_str = ' ' * (level * indent)

            if isinstance(obj, dict):
                if not obj:
                    return '{}'
                items = []
                for i, (key, value) in enumerate(obj.items()):
                    serialized = serialize(value, level + 1)
                    items.append(f'{indent_str}{" " * indent}"{key}": {serialized}'
                                 + (',' if i < len(obj) - 1 else ''))
                return '{\n' + '\n'.join(items) + f'\n{indent_str}}}'

            elif isinstance(obj, list):
                if not obj:
                    return '[]'
                # Компактно для координат [[x, y], ...]
                if all(isinstance(item, list) and len(item) == 2 and
                       all(isinstance(x, (int, float)) for x in item)
                       for item in obj):
                    coords = ', '.join([f'[{x}, {y}]' for x, y in obj])
                    return f'[{coords}]'
                # Обычный список с отступами
                items = []
                for i, item in enumerate(obj):
                    serialized = serialize(item, level + 1)
                    items.append(f'{indent_str}{" " * indent}{serialized}'
                                 + (',' if i < len(obj) - 1 else ''))
                return '[\n' + '\n'.join(items) + f'\n{indent_str}]'

            else:
                return json.dumps(obj, ensure_ascii=False)

        result = serialize(data, level=0)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(result + '\n')
