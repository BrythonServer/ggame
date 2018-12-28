"""
Example of using the PolygonAsset class.
"""

from ggame import PolygonAsset, LineStyle, Color, BLACK

POLY = PolygonAsset(
    [(0, 0), (50, 50), (50, 100), (0, 0)], LineStyle(4, BLACK), Color(0x80FF00, 0.8)
)
