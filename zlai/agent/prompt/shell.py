from dataclasses import dataclass
from ...schema.messages import SystemMessage
from ..schema import AgentPrompt


__all__ = [
    "prompt_shell",
]


system_message = SystemMessage(content="You are a helpful SHELL assistant.")
prompt_shell = AgentPrompt(system_message=system_message)
