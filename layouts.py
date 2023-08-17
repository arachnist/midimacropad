import mido
from typing import Optional


class Button:
    id: int
    type: str = "not_implemented"

    def __init__(self, id: int) -> None:
        self.id = id

    def message(self, id: str, color: int):
        raise NotImplementedError("implement this")

    def __eq__(self, other) -> bool:
        return self.type == other.type and self.id == other.id


class ControlChange(Button):
    type: str = "control_change"

    def message(self, color: int):
        return mido.Message("control_change", control=self.id, value=color)


class NoteOn(Button):
    type: str = "note_on"

    def message(self, color: int):
        return mido.Message("note_on", note=self.id, velocity=color)


class Missing(Button):
    type: str = "empty"

    def message(self, id: str, color: int):
        return None


class Layout:
    button_layout: list[list[tuple[str, int]]] = [[]]
    state: list[list[int]] = [[]]
    ioport: mido.ports.IOPort

    def __init__(self, button_layout: list[list[tuple[str, int]]], ioport: mido.ports.IOPort) -> None:
        self.button_layout = button_layout
        self.state = [[0 for e in r] for r in self.button_layout]
        self.ioport = ioport

    def get_coords(
        self, button: Optional[tuple[str, int]]
    ) -> Optional[tuple[int, int]]:
        for idy, row in enumerate(self.button_layout):
            for idx, element in enumerate(row):
                if element == button:
                    return (idx, idy)

        return None

    def get_button(
        self, coords: Optional[tuple[int, int]]
    ) -> Optional[tuple[int, int]]:
        try:
            return self.button_layout[coords[0]][coords[1]]
        except (IndexError, TypeError):
            return None

    def color_change(self, coords: tuple[int, int], value) -> None:
        self.state[coords[0]][coords[1]] = value
        ioport.send(self.get_button(coords).message(value))


class GridLayout(Layout):
    def get_coord_neighbors(self, coords: tuple[int, int]) -> list[tuple[str, int]]:
        return list(
            filter(
                lambda i: self.get_button(i) is not None,
                [
                    c
                    for c in [
                        # top row
                        (coords[0] - 1, coords[1] - 1),
                        (coords[0], coords[1] - 1),
                        (coords[0] + 1, coords[1] - 1),
                        # middle row
                        (coords[0] - 1, coords[1]),
                        (coords[0] + 1, coords[1]),
                        # bottom row
                        (coords[0] - 1, coords[1] + 1),
                        (coords[0], coords[1] + 1),
                        (coords[0] + 1, coords[1] + 1),
                    ]
                ],
            )
        )

    def get_button_neighbors(self, button: tuple[str, int]) -> list[tuple[str, int]]:
        coords = self.get_coords(button)
        if coords == None:
            return []
        else:
            return self.get_coord_neighbors(coords)


class LaunchpadMiniMk1(GridLayout):
    ioport: mido.ports.IOPort

    def __init__(self, ioport: mido.ports.IOPort) -> None:
        GridLayout.__init__(
            self,
            [[ControlChange(n) for n in range(104, 111 + 1)] + [Missing(0)]]
            + [[NoteOn(n) for n in range(x * 16, x * 16 + 8 + 1)] for x in range(8)],
            ioport
        )
