from layouts import Layout
from font import Font


class Effect:
    layout: Layout
    coords: tuple[int, int]
    iteration: int = 0
    start: int

    def __init__(
        self, layout, start: int = 0, coords: tuple[int, int] = (0, 0)
    ) -> None:
        self.layout = layout
        self.coords = coords
        self.iteration = 0
        self.start = start

    def tick(self) -> bool:
        raise NotImplementedError("this is just a base class")


class FullFlash(Effect):
    colors = [15, 60, 62, 63]

    def tick(self) -> bool:
        for y, row in enumerate(self.layout.next_state):
            for x, col in enumerate(row):
                self.layout.next_state[y][x] = self.colors[
                    (self.start + self.iteration) % len(self.colors)
                ]

        self.iteration += 1

        return True


class PointBloom(Effect):
    colors = [15, 60, 62, 63]

    def tick(self) -> bool:
        if self.iteration < len(self.colors):
            self.layout.next_state[self.coords[1]][self.coords[0]] = self.colors[
                self.iteration
            ]

        if self.iteration > 0 and self.iteration < len(self.colors) + 1:
            for c in self.layout.get_coord_neighbors(self.coords):
                self.layout.next_state[c[1]][c[0]] = self.colors[self.iteration - 1]

        self.iteration += 1

        if self.iteration > len(self.colors):
            return False
        else:
            return True


class TextScroll(Effect):
    text = ""
    bitmap = []

    def __init__(
        self, layout, start: int = 0, coords: tuple[int, int] = (0, 0), text: str = ""
    ) -> None:
        self.layout = layout
        self.coords = coords
        self.iteration = 0
        self.start = start
        self.text = text
        self.bitmap = []

        for c in list(text):
            for nr, line in enumerate(Font[ord(c)][1:]):
                if nr >= len(self.bitmap):
                    self.bitmap.append([0, 0, 0, 0, 0, 0, 0, 0, 0])
                self.bitmap[nr] += line

        for nr, line in enumerate(self.bitmap):
            self.bitmap[nr] += [0, 0, 0, 0, 0, 0, 0, 0, 0]

    def tick(self) -> bool:
        for y, row in enumerate(self.layout.next_state):
            for x, col in enumerate(row):
                self.layout.next_state[y][x] = self.bitmap[y][x + self.iteration]

        self.iteration += 1

        if self.iteration + len(self.layout.next_state[0]) >= len(self.bitmap[0]):
            return False

        return True
