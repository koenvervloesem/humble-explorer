from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Checkbox, Input, Static

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


class FilterWidget(Input):
    """A Textual widget to filter Bluetooth Low Energy advertisements."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = False

    def on_blur(self, message: Input.on_blur) -> None:
        """ "Automatically hide widget on losing focus."""
        self.display = False


class ShowDataWidget(Static):
    """A Textual widget to let the user choose what advertisement data to show."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display = False

    def compose(self) -> ComposeResult:
        """Show checkboxes."""
        yield Static("[b]Show data\n")
        yield Horizontal(
            Static("Local name       ", classes="label"),
            Checkbox(value=True, id="local_name"),
            classes="container",
        )
        yield Horizontal(
            Static("RSSI             ", classes="label"),
            Checkbox(value=True, id="rssi"),
            classes="container",
        )
        yield Horizontal(
            Static("TX power         ", classes="label"),
            Checkbox(value=True, id="tx_power"),
            classes="container",
        )
        yield Horizontal(
            Static("Manufacturer data", classes="label"),
            Checkbox(value=True, id="manufacturer_data"),
            classes="container",
        )
        yield Horizontal(
            Static("Service data     ", classes="label"),
            Checkbox(value=True, id="service_data"),
            classes="container",
        )
        yield Horizontal(
            Static("Service UUIDs    ", classes="label"),
            Checkbox(value=True, id="service_uuids"),
            classes="container",
        )

    def on_blur(self, message: Input.on_blur) -> None:
        """Automatically hide widget on losing focus."""
        self.display = False
