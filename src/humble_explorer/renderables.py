"""Module with Rich renderables for HumBLE Explorer's user interface."""
from __future__ import annotations

from datetime import datetime
from string import printable, whitespace
from uuid import UUID

from bleak.backends.scanner import AdvertisementData
from bluetooth_numbers import company, oui, service
from bluetooth_numbers.exceptions import (
    UnknownCICError,
    UnknownOUIError,
    UnknownUUIDError,
    WrongOUIFormatError,
)
from rich._palettes import EIGHT_BIT_PALETTE
from rich.style import Style
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from humble_explorer.utils import hash8

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

PRINTABLE_CHARS = printable.replace(whitespace, " ")


class RichTime:
    """Rich renderable that shows a time.

    All times within the same second are rendered in the same color.
    """

    def __init__(self, time: datetime) -> None:
        """Create a RichTime object.

        Args:
            time (datetime): The time to show.
        """
        self.full_time = time.strftime("%H:%M:%S.%f")
        self.style = Style(
            color=EIGHT_BIT_PALETTE[hash8(time.strftime("%H:%M:%S"))].hex
        )

    def __rich__(self) -> Text:
        """Render the RichTime object.

        Returns:
            Text: The rendering of the RichTime object.
        """
        return Text(self.full_time, style=self.style)


class RichDeviceAddress:
    """Rich renderable that shows a Bluetooth device address aand OUI description.

    Every address is rendered in its own color.
    """

    def __init__(self, address: str) -> None:
        """Create a RichDeviceAddress object.

        Args:
            address (str): The address to show.
        """
        self.address = address
        self.style = Style(color=EIGHT_BIT_PALETTE[hash8(self.address)].hex)
        try:
            self.oui = oui[self.address[:8]]
        except (UnknownOUIError, WrongOUIFormatError):
            # This could be macOS that returns a UUID instead of Bluetooth address
            self.oui = ""

    def height(self) -> int:
        """Return the number of lines this Rich renderable uses."""
        height = 1
        if self.oui:
            height += 1
        return height  # noqa: R504

    def __rich__(self) -> Text:
        """Render the RichDeviceAddress object.

        Returns:
            Text: The rendering of the RichDeviceAddress object.
        """
        if self.oui:
            return Text.assemble(Text(self.address, style=self.style), f"\n{self.oui}")

        return Text(self.address, style=self.style)


class RichRSSI:
    """Rich renderable that shows RSSI of a device."""

    def __init__(self, rssi: int) -> None:
        """Create a RichRSSI object.

        Args:
            rssi (int): The RSSI to show.
        """
        self.rssi = rssi

    def __rich__(self) -> Text:
        """Render the RichRSSI object.

        Returns:
            Text: The rendering of the RichRSSI object.
        """
        return Text.assemble((str(self.rssi), "green bold"), " dBm")


class RichUUID:
    """Rich renderable that shows a UUID with description and colors."""

    def __init__(self, uuid128: str) -> None:
        """Create a RichUUID object.

        Args:
            uuid128 (str): The UUID to show.
        """
        self.uuid128 = uuid128

    def __rich__(self) -> Text:
        """Render the RichUUID object.

        Returns:
            Text: The rendering of the RichUUID object.
        """
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
            service_name = (service[UUID(self.uuid128)], "green bold")
        except UnknownUUIDError:
            service_name = ("Unknown", "red bold")

        return Text.assemble(colored_uuid, " (", service_name, ")")


class RichCompanyID:
    """Rich renderable that shows company ID and name."""

    def __init__(self, cic: int) -> None:
        """Create a RichCompanyID object.

        Args:
            cic (int): The company ID to show.
        """
        self.cic = cic

    def __rich__(self) -> Text:
        """Render the RichCompanyID object.

        Returns:
            Text: The rendering of the RichCompanyID object.
        """
        try:
            manufacturer_name = (company[self.cic], "green bold")
        except UnknownCICError:
            manufacturer_name = ("Unknown", "red bold")

        return Text.assemble(f"0x{self.cic:04x} (", manufacturer_name, ")")


class RichHexData:
    """Rich renderable that shows hex data."""

    def __init__(self, data: bytes) -> None:
        """Create a RichHexData object.

        Args:
            data (bytes): The hex data to show.
        """
        self.data = data

    def __rich__(self) -> Text:
        """Render the RichHexData object.

        Returns:
            Text: The rendering of the RichHexData object.
        """
        # Python 3.7 doesn't have sep parameter for bytes.hex()
        hex_data_str = self.data.hex()
        hex_data = " ".join(
            a + b for a, b in zip(hex_data_str[::2], hex_data_str[1::2])
        )
        return Text(hex_data, style="cyan bold")


class RichHexString:
    """Rich renderable that shows hex data as a string.

    Non-printable characters are replaced by a dot.
    """

    def __init__(self, data: bytes) -> None:
        """Create a RichHexString object.

        Args:
            data (bytes): The hex data to show.
        """
        self.data = data

    def __rich__(self) -> str:
        """Render the RichHexString object.

        Returns:
            Text: The rendering of the RichHexString object.
        """
        result = []
        for byte in self.data:
            char = chr(byte)
            if char in PRINTABLE_CHARS:
                result.append(f" {char}")
            else:
                result.append(" .")

        return " ".join(result)


class RichAdvertisement:
    """Rich renderable that shows advertisement data."""

    def __init__(self, data: AdvertisementData, show_data: dict[str, bool]) -> None:
        """Create a RichAdvertisement object.

        Args:
            data (AdvertisementData): The advertisement data to show.
            show_data (dict[str, bool]): Which data to show.
        """
        self.data = data
        self.show_data = show_data

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
        return height  # noqa: R504

    def __rich__(self) -> Table:
        """Render the RichAdvertisement object.

        Returns:
            Table: The rendering of the RichAdvertisement object.
        """
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
                company_structure = Tree(
                    Text.assemble(
                        RichCompanyID(cic).__rich__(), f" → {len(value)} bytes"
                    )
                )
                company_structure.add(
                    Text.assemble("hex  → ", RichHexData(value).__rich__())
                )
                company_structure.add(
                    Text.assemble("text → ", RichHexString(value).__rich__())
                )
                tree.add(company_structure)
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
