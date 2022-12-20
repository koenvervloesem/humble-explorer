from datetime import datetime

from rich.text import Span, Text

from humble_explorer.renderables import (
    RichCompanyID,
    RichDeviceAddress,
    RichHexData,
    RichHexString,
    RichRSSI,
    RichTime,
    RichUUID,
)

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


def test_time():
    """Test RichTime class."""
    time1 = RichTime(datetime.now())
    time2 = RichTime(datetime.now())
    # Make time1 and time2 times within the same second
    while time1.full_time.split(".")[0] != time2.full_time.split(".")[0]:
        time1 = RichTime(datetime.now())

    # Times within the same second should have the same color
    assert time1.style == time2.style


def test_device_address():
    """Test RichDeviceAddress class."""
    address_string = "D5:FE:15:49:AC:7D"
    device_address = RichDeviceAddress(address_string)
    device_address2 = RichDeviceAddress(address_string)
    assert str(device_address.__rich__()) == address_string

    # Devices with the same address should have the same color
    assert device_address.style == device_address2.style


def test_rssi():
    """Test RichRSSI class."""
    rssi = RichRSSI(-70)

    # The number should be colored
    assert rssi.__rich__() == Text.assemble(("-70", "green bold"), " dBm")


def test_uuid():
    """Test RichUUID class."""
    # Unknown UUID should be rendered without color
    unknown_uuid = "22110000-554a-4546-5542-46534450464d"
    assert str(RichUUID(unknown_uuid).__rich__()) == f"{unknown_uuid} (Unknown)"

    # 16-bit UUID part in a standardized 128-bit UUID should be colored
    environmental_sensing_uuid = "0000181a-0000-1000-8000-00805f9b34fb"
    assert (
        str(RichUUID(environmental_sensing_uuid).__rich__())
        == "0000181a-0000-1000-8000-00805f9b34fb (Environmental Sensing)"
    )
    assert (
        Span(4, 8, "green bold")
        in RichUUID(environmental_sensing_uuid).__rich__().spans
    )


def test_company_id():
    """Test RichCompanyID class."""
    # Company name should be colored
    ruuvi_cid = 0x0499
    assert str(RichCompanyID(ruuvi_cid).__rich__()) == "0x0499 (Ruuvi Innovations Ltd.)"
    assert (
        Span(8, len(str(RichCompanyID(ruuvi_cid).__rich__())) - 1, "green bold")
        in RichCompanyID(ruuvi_cid).__rich__().spans
    )


def test_hex_data():
    """Test RichHexData class."""
    # Hex data should be colored and with space separator between bytes
    data = b"\x03\x4e\x11\x23\xca\x2e\xff\xaa\xff\xd1\x03\xe7\x0b\xb9"
    assert (
        str(RichHexData(data).__rich__()) == "03 4e 11 23 ca 2e ff aa ff d1 03 e7 0b b9"
    )
    assert RichHexData(data).__rich__().style == "cyan bold"


def test_hex_string():
    """Test RichHexString class."""
    # Hex string should show the correct characters with space separator between bytes
    data = b"\x03\x4e\x11\x23\xca\x2e\xff\xaa\xff\xd1\x03\xe7\x0b\xb9"
    assert (
        str(RichHexString(data).__rich__())
        == " .  N  .  #  .  .  .  .  .  .  .  .  .  ."
    )
