from dataclasses import dataclass

from object2dataclass import Object2Dataclass


@dataclass
class Color:
    red: int = None
    green: int = None
    blue: int = None


@dataclass
class Rectangle:
    width: int = None
    height: int = None
    color: Color = Color()


obj = {'width': 50, 'height': 42, 'color': {
    'red': 0, 'green': 128, 'blue': 255}}
can_be_converted = Object2Dataclass.can_be_convert_to_dataclass(obj, Rectangle)

print('Can be converted:', can_be_converted)

if can_be_converted:
    rectangle: Rectangle = Object2Dataclass.convert_object_to_dataclass(
        obj, Rectangle)
    if rectangle is not None:
        print(rectangle.height)
        print(rectangle.color.blue)
