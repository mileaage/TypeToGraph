from typing import Final

SCREEN_X: Final[int] = 1280
SCREEN_Y: Final[int] = 720

TOP_PAD: Final[float] = 0.1
BOTTOM_PAD: Final[float] = 0.1
AVAILABLE_SPACE: Final[float] = SCREEN_Y * (1 - TOP_PAD - BOTTOM_PAD)
START_Y: Final[float] = TOP_PAD * SCREEN_Y
