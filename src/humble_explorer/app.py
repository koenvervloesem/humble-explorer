from argparse import Namespace
from datetime import datetime
from platform import system

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from rich.style import Style
from textual.app import App, ComposeResult
from textual.widgets import Checkbox, DataTable, Footer, Header, Input

if system() == "Linux":
    from bleak.assigned_numbers import AdvertisementDataType
    from bleak.backends.bluezdbus.advertisement_monitor import OrPattern
    from bleak.backends.bluezdbus.scanner import BlueZScannerArgs

from humble_explorer.renderables import DeviceAddress, RichAdvertisement, Time
from humble_explorer.widgets import FilterWidget, ShowDataWidget

from . import __version__

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

_PAUSE_STYLE = Style(color="red", bgcolor="grey50")


class BLEScannerApp(App[None]):
    """A Textual app to scan for Bluetooth Low Energy advertisements."""

    CSS_PATH = "app.css"
    TITLE = f"HumBLE Explorer {__version__}"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "toggle_filter", "Filter"),
        ("a", "toggle_data", "Data"),
        ("s", "toggle_scan", "Toggle scan"),
    ]

    def __init__(self, cli_args: Namespace):
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

        # Initialize empty address filter
        self.address_filter = ""

        # Initialize empty list of advertisements
        self.advertisements = []

        super().__init__()

    def action_toggle_data(self) -> None:
        """Enable or disable data widget."""
        data_widget = self.query_one(ShowDataWidget)
        data_widget.display = not data_widget.display

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

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ShowDataWidget(id="sidebar")
        yield FilterWidget(placeholder="address=")
        yield DataTable(zebra_stripes=True)

    def show_data_config(self):
        """Return dictionary with which advertisement data to show."""
        return {
            "local_name": self.query_one("#local_name").value,
            "rssi": self.query_one("#rssi").value,
            "tx_power": self.query_one("#tx_power").value,
            "manufacturer_data": self.query_one("#manufacturer_data").value,
            "service_data": self.query_one("#service_data").value,
            "service_uuids": self.query_one("#service_uuids").value,
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
            Time(now),
            DeviceAddress(device.address),
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
        self.recreate_table()

    def on_input_changed(self, message: Input.Changed) -> None:
        """Filter advertisements with user-supplied filter."""
        if message.value.startswith("address="):
            self.address_filter = message.value[8:].upper()
        else:
            self.address_filter = ""

        self.recreate_table()

    def recreate_table(self):
        """Recreate table with advertisements."""
        table = self.query_one(DataTable)
        table.clear()
        for advertisement in self.advertisements:
            self.add_advertisement_to_table(
                table,
                Time(advertisement[0]),
                DeviceAddress(advertisement[1]),
                RichAdvertisement(advertisement[2], self.show_data_config()),
            )

    def add_advertisement_to_table(
        self, table, now, device_address, rich_advertisement
    ):
        """Add new row to table with time, address and advertisement."""
        if device_address.address.startswith(self.address_filter):
            table.add_row(
                now,
                device_address,
                rich_advertisement,
                height=rich_advertisement.height(),
            )
            table.scroll_end(animate=False)

    async def start_scan(self) -> None:
        """Start BLE scan."""
        self.scanning = True
        await self.scanner.start()

    async def stop_scan(self) -> None:
        """Stop BLE scan."""
        self.scanning = False
        await self.scanner.stop()
        table = self.query_one(DataTable)
        table.add_row(Time(datetime.now(), style=_PAUSE_STYLE))
        table.scroll_end(animate=False)
