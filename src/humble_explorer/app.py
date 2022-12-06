from argparse import Namespace
from platform import system

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from rich.style import Style
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header, Input

if system() == "Linux":
    from bleak.assigned_numbers import AdvertisementDataType
    from bleak.backends.bluezdbus.advertisement_monitor import OrPattern
    from bleak.backends.bluezdbus.scanner import BlueZScannerArgs

from humble_explorer.renderables import DeviceAddress, Now, RichAdvertisement

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

_PAUSE_STYLE = Style(color="red", bgcolor="grey50")


class FilterWidget(Input):
    """A Textual widget to filter Bluetooth Low Energy advertisements."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = False

    def on_blur(self, message: Input.on_blur) -> None:
        """ "Automatically hide widget on losing focus."""
        self.display = False


class BLEScannerApp(App[None]):
    """A Textual app to scan for Bluetooth Low Energy advertisements."""

    TITLE = "HumBLE Explorer"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("f", "toggle_filter", "Filter"),
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
        yield FilterWidget(placeholder="address=")
        yield DataTable(zebra_stripes=True)

    async def on_advertisement(
        self, device: BLEDevice, advertisement_data: AdvertisementData
    ) -> None:
        """Show advertisement data on detection of a BLE advertisement."""
        self.log(advertisement_data.local_name, device.address, advertisement_data)

        # Create renderables for advertisement and add them to list of advertisements.
        now = Now()
        device_address = DeviceAddress(device.address)
        rich_advertisement = RichAdvertisement(advertisement_data)
        self.advertisements.append((now, device_address, rich_advertisement))

        # Only add advertisement to table if it matches current address filter.
        if device.address.startswith(self.address_filter):
            table = self.query_one(DataTable)
            table.add_row(
                now,
                device_address,
                rich_advertisement,
                height=rich_advertisement.height(),
            )
            table.scroll_end(animate=False)

    async def on_mount(self) -> None:
        """Initialize interface and start BLE scan."""
        table = self.query_one(DataTable)
        table.add_columns("Time", "Address", "Advertisement")
        await self.start_scan()

    def on_input_changed(self, message: Input.Changed) -> None:
        """Filter advertisements with user-supplied filter."""
        if message.value.startswith("address="):
            self.address_filter = message.value[8:].upper()
        else:
            self.address_filter = ""

        # Recreate table content with changed filter.
        table = self.query_one(DataTable)
        table.clear()
        for advertisement in self.advertisements:
            if advertisement[1].address.startswith(self.address_filter):
                table.add_row(
                    advertisement[0],
                    advertisement[1],
                    advertisement[2],
                    height=advertisement[2].height(),
                )

    async def start_scan(self) -> None:
        """Start BLE scan."""
        self.scanning = True
        await self.scanner.start()

    async def stop_scan(self) -> None:
        """Stop BLE scan."""
        self.scanning = False
        await self.scanner.stop()
        table = self.query_one(DataTable)
        table.add_row(Now(style=_PAUSE_STYLE))
        table.scroll_end(animate=False)
