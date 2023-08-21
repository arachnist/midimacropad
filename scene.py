from layouts import Layout
from effects import Effect


class Scene:
    layouts: list[Layout] = []
    effects: list[Effect] = []

    def __init__(self, layouts: list[Layout], effects: list[Effect] = []) -> None:
        self.layouts = layouts
        self.effects = effects

    def tick(self) -> None:
        self.effects[:] = [x for x in self.effects if x.tick()]
        for layout in self.layouts:
            layout.draw_full_next()

    def add_effect(self, e: Effect) -> None:
        self.effects.append(e)
