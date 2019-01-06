"""
ggame package defines names that may be imported directly from ggame (legacy)
"""
from .__version__ import VERSION
from .asset import ImageAsset, TextAsset, CircleAsset, RectangleAsset
from .asset import PolygonAsset, LineAsset, EllipseAsset
from .asset import Frame, Color, LineStyle, BLACK, WHITE, BLACKLINE, WHITELINE
from .sound import SoundAsset, Sound
from .sprite import Sprite
from .app import App
from .event import KeyEvent, MouseEvent
