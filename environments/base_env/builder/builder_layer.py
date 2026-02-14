from base_env.extracter_data.layer import LayersParamsExtracter


class BuilderLayer:
    """
        Генерирует слои для base env среды
    """

    def __init__(self, data):

        params = LayersParamsExtracter().extract(data)

        self.width: int = params.width
        self.height: int = params.height

        self.gates: list[tuple[int, int]] = [self._validate_pair(p) for p in params.gates]
        self.shelves: list[tuple[int, int]] = [self._validate_pair(p) for p in params.shelves]

        self._validate_no_overlapping_coords()


    def _validate_pair(self, pair) -> tuple[int, int]:
        x, y = pair
        if x is None or y is None:
            raise ValueError(f'Коордианаты содержат пустое значение {x}, {y}')
        if x < 1 or y < 1:
            raise ValueError(f'Коориданты задаются от 1 до width/height {x}, {y}')
        return (x - 1, y - 1)


    def _validate_no_overlapping_coords(self):
        all_list = self.gates + self.shelves
        unique = set(all_list)

        if len(all_list) != len(unique):
            seen = set()
            duplicated = set()
            for elem in all_list:
                if elem not in seen:
                    seen.add(elem)
                else:
                    duplicated.add(elem)
            raise ValueError(f'Имеются дубликаты: {duplicated}')


    def build(self) -> str:
        """
        Генерирует текстовое представление слоя среды.
        Координаты: (1,1) — левый нижний угол.
        Визуализация идёт сверху вниз (по убыванию y).
        """
        lines = []
        for y in reversed(range(self.height)):
            lines.append(self.create_row_layer(y))
        return "\n".join(lines)


    def create_row_layer(self, y: int) -> str:
        row = ""
        for x in range(self.width):
            if (x, y) in self.gates:
                row += 'G'
            elif (x, y) in self.shelves:
                row += 'X'
            else:
                row += '.'
        
        return row