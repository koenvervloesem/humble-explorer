"""This module contains the Textual app that scans for Bluetooth Low Energy
advertisements.
"""
from argparse import Namespace
from datetime import datetime
from platform import system
from typing import Dict

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from rich.style import Style
from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Checkbox, DataTable, Footer, Header, Input

if system() == "Linux":
    from bleak.assigned_numbers import AdvertisementDataType
    from bleak.backends.bluezdbus.advertisement_monitor import OrPattern
    from bleak.backends.bluezdbus.scanner import BlueZScannerArgs

from humble_explorer.renderables import RichAdvertisement, RichDeviceAddress, RichTime
from humble_explorer.widgets import FilterWidget, SettingsWidget

from . import __version__

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

_PAUSE_STYLE = Style(color="red", bgcolor="grey50")


class BLEScannerApp(App[None]):
    """A Textual app to scan for Bluetooth Low Energy advertisements."""

    CSS_PATH = "app.css"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "toggle_filter", "Filter"),
        ("s", "toggle_settings", "Settings"),
        ("t", "toggle_scan", "Toggle scan"),
        ("c", "clear_advertisements", "Clear"),
    ]

    address_filter = reactive("")

    def __init__(self, cli_args: Namespace) -> None:
        """Initialize BLE scanner."""

        # Configure scanning mode
        scanner_kwargs = {"scanning_mode": cli_args.scanning_mode}

        # Passive scanning with BlueZ needs at least one or_pattern.
        # The following matches all devices.
        if system() == "Linux" and cli_args.scanning_mode == "passive":
            scanner_kwargs["bluez"] = BlueZScannerArgs(
                or_patterns=[
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x06"),
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x1a"),
                ]
            )

        # Configure Bluetooth adapter
        scanner_kwargs["adapter"] = cli_args.adapter

        # Set up BleakScanner object
        scanner_kwargs["detection_callback"] = self.on_advertisement
        self.scanner = BleakScanner(**scanner_kwargs)
        self.scanning = False

        # Initialize empty list of advertisements
        self.advertisements: list[tuple[datetime, str, AdvertisementData]] = []

        super().__init__()

    def set_title(self, scanning_description: str) -> None:
        """Set the title of the app with a description of the scanning status."""
        self.title = f"HumBLE Explorer {__version__} ({scanning_description})"

    def action_toggle_settings(self) -> None:
        """Enable or disable settings widget."""
        settings_widget = self.query_one(SettingsWidget)
        settings_widget.display = not settings_widget.display

    def action_toggle_filter(self) -> None:
        """Enable or disable filter input widget."""
        filter_widget = self.query_one(FilterWidget)
        filter_widget.display = not filter_widget.display
        if filter_widget.display:
            self.set_focus(filter_widget)

    async def action_toggle_scan(self) -> None:
        """Start or stop BLE scanning."""
        if self.scanning:
            await self.stop_scan()
        else:
            await self.start_scan()

    def action_clear_advertisements(self) -> None:
        """Clear the list of received advertisements."""
        self.advertisements = []
        self.query_one(DataTable).clear()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield SettingsWidget(id="sidebar")
        yield FilterWidget(placeholder="address=")
        yield DataTable(zebra_stripes=True)

    def show_data_config(self) -> Dict[str, bool]:
        """Return dictionary with which advertisement data to show."""
        return {
            "local_name": self.query_one("#local_name", Checkbox).value,
            "rssi": self.query_one("#rssi", Checkbox).value,
            "tx_power": self.query_one("#tx_power", Checkbox).value,
            "manufacturer_data": self.query_one("#manufacturer_data", Checkbox).value,
            "service_data": self.query_one("#service_data", Checkbox).value,
            "service_uuids": self.query_one("#service_uuids", Checkbox).value,
        }

    async def on_advertisement(
        self, device: BLEDevice, advertisement_data: AdvertisementData
    ) -> None:
        """Show advertisement data on detection of a BLE advertisement."""
        self.log(advertisement_data.local_name, device.address, advertisement_data)

        # Append advertisement to list of all advertisements
        now = datetime.now()
        self.advertisements.append((now, device.address, advertisement_data))

        # Create renderables for advertisement and add them to table
        table = self.query_one(DataTable)
        self.add_advertisement_to_table(
            table,
            RichTime(now),
            RichDeviceAddress(device.address),
            RichAdvertisement(advertisement_data, self.show_data_config()),
        )

    async def on_mount(self) -> None:
        """Initialize interface and start BLE scan."""
        table = self.query_one(DataTable)
        table.add_columns("Time", "Address", "Advertisement")
        # Set focus to table for immediate keyboard navigation
        table.focus()

        # Start BLE scan
        await self.start_scan()

    def on_checkbox_changed(self, message: Checkbox.Changed) -> None:
        """Show or hide advertisement data depending on the state of
        the checkboxes.
        """
        if "view" in message.input.classes:
            self.recreate_table()

    def on_input_changed(self, message: Input.Changed) -> None:
        """Filter advertisements with user-supplied filter."""
        if message.value.startswith("address="):
            self.address_filter = message.value[8:].upper()
        else:
            self.address_filter = ""

    def watch_address_filter(self, old_filter: str, new_filter: str) -> None:
        """Watch method called when the reactive attribute address_filter
        changes.
        """
        self.recreate_table()

    def recreate_table(self) -> None:
        """Recreate table with advertisements."""
        table = self.query_one(DataTable)
        table.clear()
        for advertisement in self.advertisements:
            self.add_advertisement_to_table(
                table,
                RichTime(advertisement[0]),
                RichDeviceAddress(advertisement[1]),
                RichAdvertisement(advertisement[2], self.show_data_config()),
            )

    def scroll_if_autoscroll(self) -> None:
        """Scroll to the end if autoscroll is enabled."""
        if self.query_one("#autoscroll", Checkbox).value:
            self.query_one(DataTable).scroll_end(animate=False)

    def add_advertisement_to_table(
        self,
        table: DataTable,
        now: RichTime,
        device_address: RichDeviceAddress,
        rich_advertisement: RichAdvertisement,
    ) -> None:
        """Add new row to table with time, address and advertisement."""
        if device_address.address.startswith(self.address_filter):
            table.add_row(
                now,
                device_address,
                rich_advertisement,
                height=rich_advertisement.height(),
            )
            self.scroll_if_autoscroll()

    async def start_scan(self) -> None:
        """Start BLE scan."""
        self.scanning = True
        self.set_title("Scanning")
        await self.scanner.start()

    async def stop_scan(self) -> None:
        """Stop BLE scan."""
        self.scanning = False
        self.set_title("Stopped")
        await self.scanner.stop()
        table = self.query_one(DataTable)
        table.add_row(RichTime(datetime.now(), style=_PAUSE_STYLE))
        self.scroll_if_autoscroll()
