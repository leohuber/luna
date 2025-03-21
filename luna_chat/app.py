from __future__ import annotations

import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from textual.app import App
from textual.binding import Binding
from textual.signal import Signal

from luna_chat.chats_manager import ChatsManager
from luna_chat.config import LaunchConfig, LunaChatModel
from luna_chat.models import ChatData, ChatMessage
from luna_chat.runtime_config import RuntimeConfig
from luna_chat.screens.chat_screen import ChatScreen
from luna_chat.screens.help_screen import HelpScreen
from luna_chat.screens.home_screen import HomeScreen

if TYPE_CHECKING:
    from litellm.types.completion import (
        ChatCompletionSystemMessageParam,
        ChatCompletionUserMessageParam,
    )


class Luna(App[None]):
    ENABLE_COMMAND_PALETTE = False
    CSS_PATH = Path(__file__).parent / "luna.scss"
    BINDINGS = [
        Binding("q", "app.quit", "Quit", show=False),
        Binding("f1,?", "help", "Help"),
    ]

    def __init__(self, config: LaunchConfig):
        self.launch_config = config

        self._runtime_config = RuntimeConfig(
            selected_model=config.default_model_object,
            system_prompt=config.system_prompt,
        )
        self.runtime_config_signal = Signal[RuntimeConfig](self, "runtime-config-updated")
        """Widgets can subscribe to this signal to be notified of
        when the user has changed configuration at runtime (e.g. using the UI)."""

        super().__init__()

    @property
    def runtime_config(self) -> RuntimeConfig:
        return self._runtime_config

    @runtime_config.setter
    def runtime_config(self, new_runtime_config: RuntimeConfig) -> None:
        self._runtime_config = new_runtime_config
        self.runtime_config_signal.publish(self.runtime_config)

    async def on_mount(self) -> None:
        await self.push_screen(HomeScreen(self.runtime_config_signal))
        self.theme = "textual-dark"

    async def launch_chat(self, prompt: str, model: LunaChatModel) -> None:
        current_time = datetime.datetime.now(datetime.UTC)
        system_message: ChatCompletionSystemMessageParam = {
            "content": self.runtime_config.system_prompt,
            "role": "system",
        }
        user_message: ChatCompletionUserMessageParam = {
            "content": prompt,
            "role": "user",
        }
        chat = ChatData(
            id=None,
            title=None,
            create_timestamp=None,
            model=model,
            messages=[
                ChatMessage(
                    message=system_message,
                    timestamp=current_time,
                    model=model,
                ),
                ChatMessage(
                    message=user_message,
                    timestamp=current_time,
                    model=model,
                ),
            ],
        )
        chat.id = await ChatsManager.create_chat(chat_data=chat)
        await self.push_screen(ChatScreen(chat))

    async def action_help(self) -> None:
        if isinstance(self.screen, HelpScreen):
            self.pop_screen()
        else:
            await self.push_screen(HelpScreen())


if __name__ == "__main__":
    app = Luna(LaunchConfig())
    app.run()
