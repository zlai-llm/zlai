from ...schema.messages import SystemMessage
from ..schema.base import AgentPrompt


__all__ = [
    "prompt_chat",
]


system_message = SystemMessage(content="""You are a helpful assistant.""")


prompt_chat = AgentPrompt(system_message=system_message)
