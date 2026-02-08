import random
from collections import deque

class GenerateRandomBlocks:

    DIRS : list[tuple[int, int]] = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(
            self,
            width: int,
            height: int,
            count_blocks: int,
            occupied: set[tuple[int, int]]
    ):
        self.H = height
        self.W = width
        self.count_blocks = count_blocks
        self.occupied = set(occupied)
        self.blocks: set[tuple[int, int]] = set()

    def _in_bounds(self, x: int, y: int):
        return 0 <= x < self.W and 0 <= y < self.H
    
    def _neighbors(self, x: int, y: int):
        for dx, dy in self.DIRS:
            nx, ny = dx + x, dy + y
            if self._in_bounds(nx, ny):
                yield (nx, ny)

    def is_free(self, x: int, y: int):
        return (x, y) not in self.blocks and (x, y) not in self.occupied
    
    def _creates_isolated_cell(self, x: int, y: int) -> bool:
        """
        Проверяем: не создаёт ли установка блока
        вершину степени 0 в графе свободных клеток
        """
        for nx, ny in self._neighbors(x, y):
            if not self.is_free(nx, ny):
                continue

            free_neighbors = 0
            for nnx, nny in self._neighbors(nx, ny):
                if (nnx, nny) != (x, y) and self.is_free(nnx, nny):
                    free_neighbors += 1

            if free_neighbors == 0:
                return True

        return False
    
    def _is_connected(self) -> bool:
        """
        Проверка связности графа свободных клеток
        """
        free_cells = [
            (x, y)
            for x in range(self.W)
            for y in range(self.H)
            if self.is_free(x, y)
        ]

        if not free_cells:
            return True

        start = free_cells[0]
        visited = {start}
        q = deque([start])

        while q:
            x, y = q.popleft()
            for nx, ny in self._neighbors(x, y):
                if self.is_free(nx, ny) and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny))

        return len(visited) == len(free_cells)
    
    def _can_place_block(self, x: int, y: int) -> bool:
        if not self.is_free(x, y):
            return False

        # временно ставим блок
        self.blocks.add((x, y))

        bad = (
            self._creates_isolated_cell(x, y)
            or not self._is_connected()
        )

        # откат
        self.blocks.remove((x, y))

        return not bad

    def generate(self) -> set[tuple[int, int]]:
        attempts = 0
        max_attempts = self.count_blocks * 30

        while len(self.blocks) < self.count_blocks and attempts < max_attempts:
            x = random.randrange(1, self.W)
            y = random.randrange(1, self.H)

            if self._can_place_block(x, y):
                self.blocks.add((x, y))

            attempts += 1

        if len(self.blocks) < self.count_blocks:
            raise RuntimeError("Не удалось сгенерировать валидную конфигурацию блоков")

        return self.blocks