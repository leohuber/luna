from typing import TYPE_CHECKING, cast
from importlib.metadata import version
from rich.markup import escape
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.signal import Signal
from textual.widget import Widget
from textual.widgets import Label

from rich.text import Text
from luna_chat.config import LunaChatModel
from luna_chat.models import get_model
from luna_chat.runtime_config import RuntimeConfig


if TYPE_CHECKING:
    from luna_chat.app import Luna


class AppHeader(Widget):
    COMPONENT_CLASSES = {"app-title", "app-subtitle"}

    def __init__(
        self,
        config_signal: Signal[RuntimeConfig],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.config_signal: Signal[RuntimeConfig] = config_signal
        self.luna = cast("Luna", self.app)

    def on_mount(self) -> None:
        def on_config_change(config: RuntimeConfig) -> None:
            self._update_selected_model(config.selected_model)

        self.config_signal.subscribe(self, on_config_change)

    def compose(self) -> ComposeResult:
        with Horizontal():
            with Vertical(id="cl-header-container"):
                yield Label(
                    Text("Luna") + Text(" v" + version("luna-chat"), style="dim"),
                    id="luna-title",
                )
            model_name_or_id = self.luna.runtime_config.selected_model.id or self.luna.runtime_config.selected_model.name
            model = get_model(model_name_or_id, self.luna.launch_config)
            yield Label(self._get_selected_model_link_text(model), id="model-label")

    def _get_selected_model_link_text(self, model: LunaChatModel) -> str:
        return f"[@click=screen.options]{escape(model.display_name or model.name)}[/]"

    def _update_selected_model(self, model: LunaChatModel) -> None:
        print(self.luna.runtime_config)
        model_label = self.query_one("#model-label", Label)
        model_label.update(self._get_selected_model_link_text(model))
