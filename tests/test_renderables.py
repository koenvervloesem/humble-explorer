"""Tests for renderables module."""
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


def test_time() -> None:
    """Test RichTime class."""
    time1 = RichTime(datetime.now())
    time2 = RichTime(datetime.now())
    # Make time1 and time2 times within the same second
    while time1.full_time.split(".")[0] != time2.full_time.split(".")[0]:
        time1 = RichTime(datetime.now())

    # Times within the same second should have the same color
    assert time1.style == time2.style


def test_device_address() -> None:
    """Test RichDeviceAddress class."""
    address_string = "D5:FE:15:49:AC:7D"
    device_address = RichDeviceAddress(address_string)
    device_address2 = RichDeviceAddress(address_string)
    assert str(device_address.__rich__()) == address_string
    assert device_address.height() == 1

    # Devices with the same address should have the same color
    assert device_address.style == device_address2.style

    # Address with known OUI should show company description
    address_string_qingping = "58:2D:34:54:2D:2C"
    full_address_string_qingping = (
        "58:2D:34:54:2D:2C\nQingping Electronics (Suzhou) Co., Ltd"
    )
    device_address_qingping = RichDeviceAddress(address_string_qingping)
    assert str(device_address_qingping.__rich__()) == full_address_string_qingping
    assert device_address_qingping.height() == 2


def test_rssi() -> None:
    """Test RichRSSI class."""
    rssi = RichRSSI(-70)

    # The number should be colored
    assert rssi.__rich__() == Text.assemble(("-70", "green bold"), " dBm")


def test_uuid() -> None:
    """Test RichUUID class."""
    # Unknown UUID should be rendered without color but with "Unknown" in red
    unknown_uuid = "22110000-554a-4546-5542-46534450464d"
    unknown_rich_uuid = RichUUID(unknown_uuid).__rich__()
    assert str(unknown_rich_uuid) == f"{unknown_uuid} (Unknown)"
    assert {Span(0, 36, ""), Span(38, 45, "red bold")} <= set(unknown_rich_uuid.spans)

    # 16-bit UUID part in a standardized 128-bit UUID should be colored,
    # as well as the service name
    environmental_sensing_uuid = "0000181a-0000-1000-8000-00805f9b34fb"
    environmental_sensing_rich_uuid = RichUUID(environmental_sensing_uuid).__rich__()
    assert (
        str(environmental_sensing_rich_uuid)
        == "0000181a-0000-1000-8000-00805f9b34fb (Environmental Sensing)"
    )
    assert {
        Span(0, 36, ""),
        Span(4, 8, "green bold"),
        Span(38, 59, "green bold"),
    } <= set(environmental_sensing_rich_uuid.spans)


def test_company_id() -> None:
    """Test RichCompanyID class."""
    # Unknown CID should have "Unknown" colored in red
    unknown_cid = 0xD1C2
    unknown_rich_cid = RichCompanyID(unknown_cid).__rich__()
    assert str(unknown_rich_cid) == "0xd1c2 (Unknown)"
    assert Span(8, 15, "red bold") in unknown_rich_cid.spans

    # Company name for a known CID should be colored in red
    ruuvi_cid = 0x0499
    ruuvi_rich_cid = RichCompanyID(ruuvi_cid).__rich__()
    assert str(ruuvi_rich_cid) == "0x0499 (Ruuvi Innovations Ltd.)"
    assert Span(8, 30, "green bold") in ruuvi_rich_cid.spans


def test_hex_data() -> None:
    """Test RichHexData class."""
    # Hex data should be colored and with space separator between bytes
    data = b"\x03\x4e\x11\x23\xca\x2e\xff\xaa\xff\xd1\x03\xe7\x0b\xb9"
    assert (
        str(RichHexData(data).__rich__()) == "03 4e 11 23 ca 2e ff aa ff d1 03 e7 0b b9"
    )
    assert RichHexData(data).__rich__().style == "cyan bold"


def test_hex_string() -> None:
    """Test RichHexString class."""
    # Hex string should show the correct characters with space separator between bytes
    data = b"\x03\x4e\x11\x23\xca\x2e\xff\xaa\xff\xd1\x03\xe7\x0b\xb9"
    assert (
        str(RichHexString(data).__rich__())
        == " .  N  .  #  .  .  .  .  .  .  .  .  .  ."
    )
