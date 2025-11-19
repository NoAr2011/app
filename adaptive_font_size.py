from kivy.utils import platform
from kivy.metrics import sp


def adaptive_sp(value):
    if platform == "android":
        return sp(value * 0.8)
    elif platform == "ios":
        return sp(value * 0.9)
    else:
        return sp(value)