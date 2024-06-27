
__all__ = ["transform_tool_params"]


def transform_tool_params(data):
    """Transform the data structure to the desired format."""
    if isinstance(data, dict) and "Items" in data:
        return data["Items"]
    elif isinstance(data, dict):
        return {k: transform_tool_params(v) for k, v in data.items()}
    else:
        return data
