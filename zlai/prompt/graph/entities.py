from zlai.prompt.agent import AgentPrompt
from zlai.prompt.template import PromptTemplate


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
----
Example:

Entity Types: ["人物"]
Content: 
却说太宗与魏征在便殿对弈，一递一着，摆开阵势。正合《烂柯经》云：博弈之道，贵乎严谨。高者在腹，下者在边，中者在角，此棋家之常法。
法曰：宁输一子，不失一先。击左则视右，攻后则瞻前。有先而后，有后而先。两生勿断，皆活勿连。阔不可太疏，密不可太促。
与其恋子以求生，不若弃之而取胜；与其无事而独行，不若固之而自补。彼众我寡，先谋其生；我众彼寡，务张其势。
善胜者不争，善阵者不战；善战者不败，善败者不乱。夫棋始以正合，终以奇胜。凡敌无事而自补者，有侵绝之意；弃小而不救者，有图大之心。
随手而下者，无谋之人；不思而应者，取败之道。《诗》云：“惴惴小心，如临于谷。”此之谓也。

Output:
```python
[("太宗", "人物", "唐太宗李世民，唐朝第二位皇帝，政治家、军事家、诗人。"), 
 ("魏征", "人物", "魏征（580年－643年），字玄成，唐朝政治家、军事家、文学家。")]
```
----
Entity Types: {entity_types}
Content: {content}
Output:
"""


prompt_entities = AgentPrompt(
    prompt_template=PromptTemplate(
        input_variables=["entity_types", "content"],
        template=template_entities,
    )
)


template_relations = """Given your text, entity type, and extracted entities, 
you need to identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
    - source_entity_name: name of the source entity
    - target_entity_name: name of the target entity
    - relationship_name: name of the relationship between the source entity and target entity
    - relationship_description: explanation as to why you think the source entity and the target entity are related to each other
    - relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
Format each relationship as List[Tuple]:
```python
[(<source_entity_name>, <target_entity_name>, <relationship_name>, <relationship_description>, <relationship_strength>)]
```

----
Example:

Content: 
却说太宗与魏征在便殿对弈，一递一着，摆开阵势。正合《烂柯经》云：博弈之道，贵乎严谨。高者在腹，下者在边，中者在角，此棋家之常法。
法曰：宁输一子，不失一先。击左则视右，攻后则瞻前。有先而后，有后而先。两生勿断，皆活勿连。阔不可太疏，密不可太促。
与其恋子以求生，不若弃之而取胜；与其无事而独行，不若固之而自补。彼众我寡，先谋其生；我众彼寡，务张其势。
善胜者不争，善阵者不战；善战者不败，善败者不乱。夫棋始以正合，终以奇胜。凡敌无事而自补者，有侵绝之意；弃小而不救者，有图大之心。
随手而下者，无谋之人；不思而应者，取败之道。《诗》云：“惴惴小心，如临于谷。”此之谓也。
Entity Types: ["人物"]
Entities:
[(太宗, 人物, "唐太宗李世民，唐朝第二位皇帝，政治家、军事家、诗人。"), 
 (魏征, 人物, "魏征（580年－643年），字玄成，唐朝政治家、军事家、文学家。")]
 
Output:
```python
[("太宗", "魏征", "君臣关系", "太宗与魏征在便殿对弈，体现了君臣关系，且太宗对魏征的评价非常高，因此认为他们之间存在紧密的君臣关系。", 8.5)]
```
----

Content: {content}
Entity Types: {entity_types}
Entities: {entities}
Output:
"""

prompt_relations = AgentPrompt(
    prompt_template=PromptTemplate(
        input_variables=["content", "entity_types", "entities"],
        template=template_relations,
    )
)
