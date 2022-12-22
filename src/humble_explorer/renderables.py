"""This module contains Rich renderables that are part of HumBLE Explorer's user
interface.
"""
from datetime import datetime
from string import printable, whitespace
from typing import Dict, Optional
from uuid import UUID

from bleak.backends.scanner import AdvertisementData
from bluetooth_numbers import company, service
from bluetooth_numbers.exceptions import UnknownCICError, UnknownUUIDError
from rich._palettes import EIGHT_BIT_PALETTE
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from humble_explorer.utils import hash8

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

printable_chars = printable.replace(whitespace, " ")


class RichTime:
    """Rich renderable that shows a time. All times within the same second
    are rendered in the same color."""

    def __init__(self, time: datetime, style: Optional[Style] = None) -> None:
        self.full_time = time.strftime("%H:%M:%S.%f")
        if style:
            self.style = style
        else:
            self.style = Style(
                color=EIGHT_BIT_PALETTE[hash8(time.strftime("%H:%M:%S"))].hex
            )

    def __rich__(self) -> Text:
        return Text(self.full_time, style=self.style)


class RichDeviceAddress:
    """Rich renderable that shows a Bluetooth device address. Every address is rendered
    in its own color."""

    def __init__(self, address: str) -> None:
        self.address = address
        self.style = Style(color=EIGHT_BIT_PALETTE[hash8(self.address)].hex)

    def __rich__(self) -> Text:
        return Text(self.address, style=self.style)


class RichRSSI:
    """Rich renderable that shows RSSI of a device."""

    def __init__(self, rssi: int) -> None:
        self.rssi = rssi

    def __rich__(self) -> Text:
        return Text.assemble((str(self.rssi), "green bold"), " dBm")


class RichUUID:
    """Rich renderable that shows a UUID with description and colors."""

    def __init__(self, uuid128: str) -> None:
        self.uuid128 = uuid128

    def __rich__(self) -> Text:
        # Colorize the 16-bit UUID part in a standardized 128-bit UUID.
        if self.uuid128.startswith("0000") and self.uuid128.endswith(
            "-0000-1000-8000-00805f9b34fb"
        ):
            colored_uuid = Text.assemble(
                "0000",
                (self.uuid128[4:8], "green bold"),
                "-0000-1000-8000-00805f9b34fb",
            )
        else:
            colored_uuid = Text(self.uuid128)

        try:
            return Text.assemble(colored_uuid, f" ({service[UUID(self.uuid128)]})")
        except UnknownUUIDError:
            return Text.assemble(colored_uuid, " (Unknown)")


class RichCompanyID:
    """Rich renderable that shows company ID and name."""

    def __init__(self, cic: int) -> None:
        self.cic = cic

    def __rich__(self) -> Text:
        try:
            manufacturer_name = company[self.cic]
        except UnknownCICError:
            manufacturer_name = "Unknown"

        return Text.assemble(
            f"0x{self.cic:04x} (", (manufacturer_name, "green bold"), ")"
        )


class RichHexData:
    """Rich renderable that shows hex data."""

    def __init__(self, data: bytes) -> None:
        self.data = data

    def __rich__(self) -> Text:
        return Text(f"{self.data.hex(sep= ' ')}", style="cyan bold")


class RichHexString:
    """Rich renderable that shows hex data as a string with non-printable characters
    replaced by a dot."""

    def __init__(self, data: bytes) -> None:
        self.data = data

    def __rich__(self) -> str:
        result = []
        for byte in self.data:
            char = chr(byte)
            if char in printable_chars:
                result.append(f" {char}")
            else:
                result.append(" .")

        return " ".join(result)


class RichAdvertisement:
    """Rich renderable that shows advertisement data."""

    def __init__(self, data: AdvertisementData, show_data: Dict[str, bool]) -> None:
        self.data = data
        self.show_data = show_data

    def __rich__(self) -> Table:
        table = Table(show_header=False, show_edge=False, padding=0)

        # Show local name
        if self.data.local_name and self.show_data["local_name"]:
            table.add_row(
                Text.assemble("local name: ", (self.data.local_name, "green bold"))
            )

        # Show RSSI
        if self.data.rssi and self.show_data["rssi"]:
            table.add_row(Text.assemble("RSSI: ", RichRSSI(self.data.rssi).__rich__()))

        # Show TX Power
        if self.data.tx_power and self.show_data["tx_power"]:
            table.add_row(
                Text.assemble("TX power: ", RichRSSI(self.data.tx_power).__rich__())
            )

        # Show manufacturer data
        if self.data.manufacturer_data and self.show_data["manufacturer_data"]:
            tree = Tree("manufacturer data:")
            for cic, value in self.data.manufacturer_data.items():
                company = Tree(
                    Text.assemble(
                        RichCompanyID(cic).__rich__(), f" → {len(value)} bytes"
                    )
                )
                company.add(Text.assemble("hex  → ", RichHexData(value).__rich__()))
                company.add(Text.assemble("text → ", RichHexString(value).__rich__()))
                tree.add(company)
            table.add_row(tree)

        # Show service data
        if self.data.service_data and self.show_data["service_data"]:
            tree = Tree("service data:")
            for uuid, value in self.data.service_data.items():
                svc_uuid = Tree(
                    Text.assemble(RichUUID(uuid).__rich__(), f" → {len(value)} bytes")
                )
                svc_uuid.add(Text.assemble("hex  → ", RichHexData(value).__rich__()))
                svc_uuid.add(Text.assemble("text → ", RichHexString(value).__rich__()))
                tree.add(svc_uuid)
            table.add_row(tree)

        # Show service UUIDs with their description
        if self.data.service_uuids and self.show_data["service_uuids"]:
            tree = Tree("service UUIDs:")
            for uuid in sorted(self.data.service_uuids):
                tree.add(RichUUID(uuid))
            table.add_row(tree)

        return table

    def height(self) -> int:
        """Return the number of lines this Rich renderable uses."""
        height = 0
        if self.data.local_name and self.show_data["local_name"]:
            height += 1
        if self.data.rssi and self.show_data["rssi"]:
            height += 1
        if self.data.tx_power and self.show_data["tx_power"]:
            height += 1
        if self.data.manufacturer_data and self.show_data["manufacturer_data"]:
            height = height + 1 + 3 * len(self.data.manufacturer_data)
        if self.data.service_data and self.show_data["service_data"]:
            height = height + 1 + 3 * len(self.data.service_data)
        if self.data.service_uuids and self.show_data["service_uuids"]:
            height = height + 1 + len(self.data.service_uuids)
        return height
