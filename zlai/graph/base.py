from pandas import DataFrame
import pandas as pd


__all__ = [
    "graph_long_to_wide"
]


def graph_long_to_wide(df_long: DataFrame) -> DataFrame:
    levels = sorted(df_long.level.unique().tolist())
    df_wide = None
    for level in levels:
        current_level = df_long.loc[df_long.level == level, ["src", "dst"]]
        current_level.columns = [f"level_{level}", f"level_{level + 1}"]
        if df_wide is None:
            df_wide = current_level
        else:
            df_wide = pd.merge(df_wide, current_level, on=[f"level_{level}"], how="outer")
    df_wide = df_wide.sort_values(by=["level_1", "level_2"])
    return df_wide
