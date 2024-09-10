from ..template import PromptTemplate


__all__ = [
    "prompt_entities",
    "prompt_relations",
]


template_entities = """Given a text document that is potentially relevant to this activity and a list of entity types.
Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, capitalized
- entity_type: One of the following types: {entity_types}
- entity_description: Comprehensive description of the entity's attributes and activities
Format each entity as List[Tuple]
```python
[(<entity_name>, <entity_type>, <entity_description>)]
```

Entity Types: {entity_types}
Content: {content}
"""

prompt_entities = PromptTemplate(
    input_variables=["entity_types", "content"],
    template=template_entities,
)


template_relations = """Given your text, entity type, and extracted entities, 
you need to identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
    - source_entity_name: name of the source entity, as identified in step 1
    - target_entity_name: name of the target entity, as identified in step 1
    - relationship_description: explanation as to why you think the source entity and the target entity are related to each other
    - relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
Format each relationship as List[Tuple]:
```python
[(<source_entity_name>, <target_entity_name>, <relationship_description>, <relationship_strength>)]
```

Content: {content}
Entity Types: {entity_types}
Entities: {entities}
"""

prompt_relations = PromptTemplate(
    input_variables=["content", "entity_types", "entities"],
    template=template_relations,
)
