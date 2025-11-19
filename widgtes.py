from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from adaptive_font_size import *
from kivy.clock import Clock


class BaseStyled:

    def apply_base_style(self):
        self.halign = 'center'
        self.valign = 'center'
        self.border = (0, 0, 0, 0)
        self.size_hint_y = None
        self.height = sp(60)


class BaseButton(Button, BaseStyled):
    def __init__(self, bg_normal, text_color="white", **kwargs):
        super().__init__(**kwargs)
        self.color = text_color
        self.background_normal = bg_normal
        self.background_active = bg_normal
        self.font_size = adaptive_sp(14)
        self.bold = True
        self.allow_stretch = True
        self.keep_ratio = False
        self.apply_base_style()


class ClosingButton(BaseButton):
    def __init__(self, **kwargs):
        super().__init__(bg_normal="button09.png", **kwargs)
        self.text = "Bezár"


class NewLabel(BaseButton):
    def __init__(self, **kwargs):
        super().__init__(bg_normal="button03.png", **kwargs)
        self.bind(size=self.update_font_size)
        self.size_hint = 1, None


    def update_font_size(self, *args):
        self.font_size = min(self.width, self.height) * 0.3
        self.text_size = self.size


class NewTextInput(TextInput, BaseStyled):
    def __init__(self, font_size, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = "button10.png"
        self.background_active = "button10.png"
        self.border = (0, 0, 0, 0)
        self.font_size = adaptive_sp(font_size)
        self.halign = 'center'
        self.valign = 'middle'
        self.multiline = True
        self.foreground_color = "white"
        self.apply_base_style()

        Clock.schedule_once(self.update_padding, 0)

    def update_padding(self, *args):
        self.padding = (0, (self.height - self.font_size) / 2, 0, 0)


class InforPopup(Popup):
    def __init__(self, content, screen, dec_size, **kwargs):
        super().__init__(**kwargs)
        self.title = "Figyelem!"
        self.content = content
        self.size_hint = (None, None)
        self.padding = (40, 40)
        self.size = (screen.width / 1.2, screen.height / dec_size)
        self.auto_dismiss = False