from .widget import Widget


class Button(Widget):
    def __init__(self, *args, text: str = "", **kwargs):
        super().__init__(*args, **kwargs)

        self.text = text
        self._rect_id = self.add_element("rect", rect=self.rect)

    def draw_config(self, canvas):
        self.config_element(self._rect_id, rect=self.rect)
