from typing import List, Optional
from pydantic import BaseModel, Field
from ...schema import Message


__all__ = [
    "ShowMessages",
    "steam_message",
    "StreamMessage",
]


class StreamMessage(BaseModel):
    not_find_content: Optional[str] = "**未在知识库中找到相关信息**...\n\n"
    not_find_table: Optional[str] = "**未在数据库中找到相关表，请您提供更为准确的表名，我再为您解答**...\n\n"
    thinking: Optional[str] = "**正在思考**...\n\n"
    write_script: Optional[str] = "**正在编写相关程序**...\n\n"
    run_script: Optional[str] = "**执行程序**...\n\n"
    script_result: Optional[str] = "**执行结果**:\n\n"
    observation_answer: Optional[str] = "**总结回答**:\n\n"


class ShowMessages(BaseModel):
    """"""
    messages: List[Message] = Field(default=[], description="")
    drop_system: Optional[bool] = Field(default=True, description="")
    content_length: Optional[int] = Field(default=None, description="")
    few_shot: Optional[bool] = Field(default=True, description="")
    logger_name: Optional[str] = Field(default="Logger", description="")


steam_message = StreamMessage()
