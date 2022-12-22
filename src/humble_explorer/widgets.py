"""This module contains Textual widgets for HumBLE Explorer's user interface."""
from typing import Optional

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Checkbox, Input, Static

__author__ = "Koen Vervloesem"
__copyright__ = "Koen Vervloesem"
__license__ = "MIT"


class FilterWidget(Input):
    """A Textual widget to filter Bluetooth Low Energy advertisements."""

    def __init__(self, placeholder: str = "") -> None:
        super().__init__(placeholder=placeholder)
        self.display = False

    def on_blur(self) -> None:
        """ "Automatically hide widget on losing focus."""
        self.display = False


class SettingsWidget(Static):
    """A Textual widget to let the user choose settings."""

    def __init__(self, id: Optional[str] = None) -> None:
        super().__init__(id=id)
        self.display = False

    def compose(self) -> ComposeResult:
        """Show checkboxes."""
        yield Static("[b]Show data types[/b]\n")
        yield Horizontal(
            Static("Local name       ", classes="label"),
            Checkbox(value=True, id="local_name", classes="view"),
            classes="container",
        )
        yield Horizontal(
            Static("RSSI             ", classes="label"),
            Checkbox(value=True, id="rssi", classes="view"),
            classes="container",
        )
        yield Horizontal(
            Static("TX power         ", classes="label"),
            Checkbox(value=True, id="tx_power", classes="view"),
            classes="container",
        )
        yield Horizontal(
            Static("Manufacturer data", classes="label"),
            Checkbox(value=True, id="manufacturer_data", classes="view"),
            classes="container",
        )
        yield Horizontal(
            Static("Service data     ", classes="label"),
            Checkbox(value=True, id="service_data", classes="view"),
            classes="container",
        )
        yield Horizontal(
            Static("Service UUIDs    ", classes="label"),
            Checkbox(value=True, id="service_uuids", classes="view"),
            classes="container",
        )
        yield Static("\n[b]Other settings[/b]\n")
        yield Horizontal(
            Static("Auto-scroll      ", classes="label"),
            Checkbox(value=True, id="autoscroll", classes="view"),
            classes="container",
        )

    def on_blur(self) -> None:
        """Automatically hide widget on losing focus."""
        self.display = False
