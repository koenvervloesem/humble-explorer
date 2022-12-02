from rich.text import Text

from humble_explorer.renderables import RSSI, Now

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


def test_now():
    """Test Now class."""
    now1 = Now()
    now2 = Now()
    # make now1 and now2 times within the same second
    while now1.time.split(".")[0] != now2.time.split(".")[0]:
        now1 = Now()

    assert now1.style == now2.style


def test_rssi():
    """Test RSSI class."""
    rssi = RSSI(-70)
    assert rssi.__rich__() == Text.assemble(("-70", "green bold"), " dBm")
