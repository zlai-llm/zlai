from ..schema.messages import SystemMessage


__all__ = [
    "sql_system_message",
]


sql_system_message = SystemMessage(
    content="你是一个SQL专家，用户会提问你关于数据报表的问题，你需要分析用户提问的问题，并以List[str]的格式输出用户所需要报表的字段名称。")

