from typing import Sequence, Tuple, Union

from pygame.color import Color

# C'est pour les couleurs qu'utilise pygame
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]