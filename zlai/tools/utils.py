from typing import List, Union, Literal, Optional
from pandas import DataFrame


__all__ = [
    "headers",
    "transform_tool_params",
    "trans_dataframe",
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}


def transform_tool_params(data):
    """Transform the data structure to the desired format."""
    if isinstance(data, dict) and "Items" in data:
        return data["Items"]
    elif isinstance(data, dict):
        return {k: transform_tool_params(v) for k, v in data.items()}
    else:
        return data


def trans_dataframe(
        df: Optional[DataFrame] = None,
        return_type: Optional[Literal["DataFrame", "List", "Markdown"]] = "Markdown",
) -> Union[DataFrame, List, str]:
    """
    Transform the dataframe to the desired format.

    :param df:
    :param return_type:
    :return:
    """
    if return_type == "DataFrame":
        return df
    elif return_type == "List":
        return df.to_dict(orient="records")
    elif return_type == "Markdown":
        return df.to_markdown()
    else:
        raise ValueError(f"Unsupported return type: {return_type}")
