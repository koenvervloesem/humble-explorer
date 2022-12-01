from argparse import Namespace
from platform import system

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from rich.style import Style
from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Header

if system() == "Linux":
    from bleak.assigned_numbers import AdvertisementDataType
    from bleak.backends.bluezdbus.advertisement_monitor import OrPattern
    from bleak.backends.bluezdbus.scanner import BlueZScannerArgs

from humble_explorer.renderables import Now, RichAdvertisement

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"

_PAUSE_STYLE = Style(color="red", bgcolor="grey50")


class BLEScannerApp(App[None]):
    """A Textual app to scan for Bluetooth Low Energy advertisements."""

    TITLE = "HumBLE Explorer"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "toggle_scan", "Toggle scan"),
    ]

    def __init__(self, cli_args: Namespace):
        """Initialize BLE scanner."""

        # Configure scanning mode
        self.scanner_kwargs = {"scanning_mode": cli_args.scanning_mode}

        # Passive scanning with BlueZ needs at least one or_pattern.
        # The following matches all devices.
        if system() == "Linux" and cli_args.scanning_mode == "passive":
            self.scanner_kwargs["bluez"] = BlueZScannerArgs(
                or_patterns=[
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x06"),
                    OrPattern(0, AdvertisementDataType.FLAGS, b"\x1a"),
                ]
            )

        # Configure Bluetooth adapter
        self.scanner_kwargs["adapter"] = cli_args.adapter

        # Configure detection callback
        self.scanner_kwargs["detection_callback"] = self.on_advertisement
        self.scanning = False

        super().__init__()

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
        yield DataTable(zebra_stripes=True)

    async def on_advertisement(
        self, device: BLEDevice, advertisement_data: AdvertisementData
    ) -> None:
        """Show advertisement data on detection of a BLE advertisement."""
        self.log(advertisement_data.local_name, device.address, advertisement_data)
        rich_advertisement = RichAdvertisement(advertisement_data)
        table = self.query_one(DataTable)
        table.add_row(
            Now(),
            device.address,
            rich_advertisement,
            height=rich_advertisement.height(),
        )
        table.scroll_end(animate=False)

    async def on_mount(self) -> None:
        """Initialize interface and start BLE scan."""
        table = self.query_one(DataTable)
        table.add_columns("Time", "Address", "Advertisement")
        self.scanner = BleakScanner(**self.scanner_kwargs)
        await self.start_scan()

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
