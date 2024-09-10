from zlai.prompt.graph import prompt_entities, prompt_relations
from zlai.prompt import AgentPrompt


__all__ = [
    "agent_prompt_entities",
    "agent_prompt_relations",
]


agent_prompt_entities = AgentPrompt(prompt_template=prompt_entities)
agent_prompt_relations = AgentPrompt(prompt_template=prompt_relations)
