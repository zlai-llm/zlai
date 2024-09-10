from zlai.prompt import PromptTemplate, AgentPrompt


__all__ = [
    "prompt_long_write_plan",
    "prompt_long_write",
]


long_write_plan_template = """
I need you to help me break down the following long-form writing instruction into multiple subtasks.
Each subtask will guide the writing of one paragraph in the essay, and should include the main points
and word count requirements for that paragraph.

The writing instruction is as follows:

{instruction}

Please break it down in the following format, with each subtask taking up one line:

Paragraph 1 - Main Point: [Describe the main point of the paragraph, in detail] - Word Count: [Word count requirement, e.g., 400 words]

Paragraph 2 - Main Point: [Describe the main point of the paragraph, in detail] - Word Count: [word count requirement, e.g. 1000 words].

...

Make sure that each subtask is clear and specific, and that all subtasks cover the entire content of the writing instruction.
Do not split the subtasks too finely; each subtask's paragraph should be no less than 200 words and no more than 1000 words.
Do not output any other content. As this is an ongoing work, omit open-ended conclusions or other rhetorical hooks.
Finally, [Main Point] use Chinese.
"""

long_write_template = """
You are an excellent writing assistant. I will give you an original writing instruction and my planned writing steps. 
I will also provide you with the text I have already written. Please help me continue writing the next paragraph 
based on the writing instruction, writing steps, and the already written text.

Writing instruction:

{instruction}

Writing steps:

{step}

Already written text:

{content}

Please integrate the original writing instruction, writing steps, and the already written text, 
and now continue writing {step}. If needed, you can add a small subtitle at the beginning. 
Remember to only output the paragraph you write, without repeating the already written text.
"""

prompt_long_write_plan = AgentPrompt(
    prompt_template=PromptTemplate(
        template=long_write_plan_template,
        input_variables=["instruction"]
    )
)
prompt_long_write = AgentPrompt(
    prompt_template=PromptTemplate(
        template=long_write_template,
        input_variables=["instruction", "step", "content"]
    )
)
