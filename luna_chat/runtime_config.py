from pydantic import BaseModel, ConfigDict

from luna_chat.config import LunaChatModel


class RuntimeConfig(BaseModel):
    model_config = ConfigDict(frozen=True)

    selected_model: LunaChatModel
    system_prompt: str
