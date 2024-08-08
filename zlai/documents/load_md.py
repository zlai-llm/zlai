import pandas as pd
from typing import Any, List, Tuple, Optional, Literal, Union
from zlai.types.documents.markdown import MarkdownLine


__all__ = [
    "ParseMarkdown",
    "get_node_source",
]


class ParseMarkdown:
    """"""
    max_level: int
    lines: List[MarkdownLine]

    def __init__(
            self,
            text: str,
            indentation: Optional[int] = 4,
            **kwargs: Any
    ):
        """"""
        self.text = text
        self.max_level = 0
        self.indentation = indentation
        self.lines = []
        self.kwargs = kwargs

    def _find_last_line(self, _type: str, level: Optional[int] = None) -> Optional[MarkdownLine]:
        """"""
        for line in self.lines[::-1]:
            if level:
                if line.level == level and line.type == _type:
                    return line
            else:
                if line.type == _type:
                    return line

    def _add_li_level(self, markdown_line: MarkdownLine):
        """"""
        last_title = self._find_last_line(_type="title")
        indentation, _ = markdown_line.origin.split("-", 1)
        indent_level = (len(indentation) // self.indentation)
        level = last_title.level + indent_level + 1
        markdown_line.level = level

        if indent_level > 0:
            last_li = self._find_last_line(_type="li", level=level - 1)
            markdown_line.src = last_li.content
        else:
            markdown_line.src = last_title.content
        if markdown_line.level > self.max_level:
            self.max_level = markdown_line.level

    def _detect_base(self, line: str, markdown_line: MarkdownLine, _type: str):
        """"""
        mark, content = line.split(sep=" ", maxsplit=1)
        markdown_line.type = _type
        markdown_line.content = content
        if _type == "li":
            self._add_li_level(markdown_line)

    def _detect_title(self, line: str, markdown_line: MarkdownLine,):
        """"""
        mark, content = line.split(sep=" ", maxsplit=1)
        level = len(mark)
        markdown_line.level = level
        markdown_line.content = content
        markdown_line.type = "title"
        if level > self.max_level:
            self.max_level = level

    def _find_src_line(self, level: int) -> Optional[MarkdownLine]:
        """ find last level line """
        for line in self.lines[::-1]:
            if line.level == level:
                return line

    def _detect_source(self, cur_line: MarkdownLine, src_line: MarkdownLine):
        """"""
        new_src_line = src_line.model_copy(deep=True)

        if not src_line.level <= cur_line.level and src_line.src != "root":
            src_line = self._find_last_line(level=cur_line.level - 1, _type="title")

        if src_line.src == "root" and cur_line.level == 1:
            cur_line.src = src_line.src
            new_src_line = cur_line
        elif src_line.type == "title" and cur_line.type == "title":
            if cur_line.level == src_line.level + 1:
                cur_line.src = src_line.content
            if cur_line.level == src_line.level:
                src_line = self._find_src_line(level=src_line.level - 1)
                cur_line.src = src_line.content
            new_src_line = cur_line
        return new_src_line

    def _detect_line(
            self,
            line: str,
            src_line: Optional[MarkdownLine] = None
    ) -> Tuple[MarkdownLine, MarkdownLine]:
        """"""
        markdown_line = MarkdownLine(origin=line)
        content = line.strip()
        if line.strip().startswith("#"):
            self._detect_title(content, markdown_line, )
        elif line.strip().startswith("-"):
            self._detect_base(content, markdown_line, _type="li")
        else:
            markdown_line.content = content
        src_line = self._detect_source(markdown_line, src_line)
        return markdown_line, src_line

    def split_text(self, text: Optional[str] = None):
        """"""
        if text is None:
            text = self.text
        line_content = [line for line in text.split("\n") if len(line.strip()) != 0]

        src_line = MarkdownLine(level=0, src="root")
        for i, line in enumerate(line_content):
            current_line, src_line = self._detect_line(line, src_line)
            self.lines.append(current_line)

    def to_table(self, drop_root: bool = True, fix_level: bool = True) -> pd.DataFrame:
        if len(self.lines) == 0:
            self.split_text(self.text)

        df_table = pd.DataFrame([line.model_dump() for line in self.lines])
        df_table = df_table[["level", "src", "content"]]
        df_table.columns = ["level", "src", "dst"]
        if drop_root:
            df_table = df_table[df_table["src"] != "root"]
        if fix_level:
            df_table["level"] = df_table["level"] - int(df_table.level.min() - 1)
        return df_table


def get_node_source(
        df: pd.DataFrame,
        node_name: str,
) -> Union[str, dict]:
    """"""
    node_level = df[df["dst"] == node_name]["level"].values[0]
    pre_node = df[df["dst"] == node_name]["src"].values[0]
    curr_level_nodes = df.loc[df.src == pre_node, "dst"].tolist()
    content = f"{'#' * (node_level - 1)} {pre_node}"
    for node_name in curr_level_nodes:
        content += f"\n- {node_name}"
    return content
