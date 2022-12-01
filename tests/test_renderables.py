from rich.text import Text

from humble_explorer.renderables import RSSI

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


def test_rssi():
    """Test RSSI class."""
    rssi = RSSI(-70)
    assert rssi.__rich__() == Text.assemble(("-70", "green bold"), " dBm")
