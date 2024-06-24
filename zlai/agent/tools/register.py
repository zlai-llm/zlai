import inspect
import traceback
from enum import EnumMeta
from typing import *
from types import GenericAlias

from .schema import *


__all__ = [
    "register_tool",
    "dispatch_tool",
]


def enum_metadata(typ: EnumMeta) -> Dict:
    """"""
    enum_typ_lst = list(typ)
    enum_properties = dict()
    info = dict()
    for item in enum_typ_lst:
        enum_item = eval(item.value)
        enum_typ, (enum_desc, enum_name) = enum_item.__origin__, enum_item.__metadata__
        enum_properties.update({"type": enum_typ.__name__,})
        info.update({"value": enum_name, "description": enum_desc})
    enum_properties.update({"enum": info})
    return enum_properties


def register_tool(tool_hooks: Dict, tool_descriptions: List):
    """"""
    def decorator_func(func):
        tool_name = func.__name__
        tool_description = inspect.getdoc(func).strip()
        python_params = inspect.signature(func).parameters
        tool_params = []
        required_lst = []
        properties = dict()
        for name, param in python_params.items():
            annotation = param.annotation
            if annotation is inspect.Parameter.empty:
                raise TypeError(f"Parameter `{name}` missing type annotation")
            if get_origin(annotation) != Annotated:
                raise TypeError(f"Annotation type for `{name}` must be typing.Annotated")

            typ, (description, required) = annotation.__origin__, annotation.__metadata__

            if isinstance(typ, EnumMeta):
                enum_properties = enum_metadata(typ)
            else:
                enum_properties = None

            typ: str = str(typ) if isinstance(typ, GenericAlias) else typ.__name__
            if not isinstance(description, str):
                raise TypeError(f"Description for `{name}` must be a string")
            if not isinstance(required, bool):
                raise TypeError(f"Required for `{name}` must be a bool")

            if required:
                required_lst.append(name)

            tool_params.append({
                "name": name,
                "description": description,
                "type": typ,
                "required": required
            })

            properties.update({name: dict()})
            properties.get(name).update({
                "description": description,
                "type": typ,
            })
            if enum_properties:
                properties.get(name).update({
                    "enum": enum_properties.get("enum"),
                    "type": enum_properties.get("type"),
                })

        tool_def = {
            "name": tool_name,
            "description": tool_description,
            "parameters": tool_params
        }
        tool_hooks[tool_name] = func

        tool_parameters = ToolParameters(
            properties=properties,
            required=required_lst,
        )
        tool_item = ToolItem(
            function=ToolFunction(
                name=tool_def.get("name"),
                description=tool_def.get("description"),
                parameters=tool_parameters
            )
        )
        tool_descriptions.append(tool_item.model_dump())

        def wrapper(*args, **kwargs):
            """"""
            return func
        return wrapper
    return decorator_func


def dispatch_tool(
        tool_name: str,
        tool_params: dict,
        hooks: Optional[Dict[str, Callable]],
        *args: Any,
        **kwargs: Any,
) -> str:
    if tool_name not in hooks:
        return f"Tool `{tool_name}` not found. Please use a provided tool."
    tool_call = hooks[tool_name]
    try:
        ret = tool_call(**tool_params)
    except:
        ret = traceback.format_exc()
    return str(ret)
