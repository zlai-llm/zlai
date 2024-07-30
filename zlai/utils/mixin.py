try:
    from colorama import Fore, Style
except ModuleNotFoundError:
    raise ModuleNotFoundError("pip install colorama")
from typing import Dict, Union, Optional, Callable, Literal
from logging import Logger


__all__ = ["LoggerMixin"]


print_color_mapping = {
    "BLACK".lower(): Fore.BLACK,
    "RED".lower(): Fore.RED,
    "GREEN".lower(): Fore.GREEN,
    "YELLOW".lower(): Fore.YELLOW,
    "BLUE".lower(): Fore.BLUE,
    "CYAN".lower(): Fore.CYAN,
    "MAGENTA".lower(): Fore.MAGENTA,
    "WHITE".lower(): Fore.WHITE,
    "RESET".lower(): Fore.RESET,
}


TypePrintColor = Literal['black', 'red', 'green', 'yellow', 'blue', 'cyan', 'magenta', 'white', 'reset']


class LoggerMixin:
    """"""
    logger: Optional[Union[Logger, Callable]]
    verbose: Optional[bool]

    def _logger(
            self,
            msg: str,
            color: Optional[TypePrintColor] = None
    ) -> None:
        """"""
        if self.logger: self.logger.info(msg)
        if self.verbose:
            if color:
                print(print_color_mapping.get(color) + msg + Style.RESET_ALL, flush=True)
            else:
                print(msg, flush=True)

    def _logger_base(self, msg: str, color: Optional[TypePrintColor] = None):
        """"""
        if self.logger: self.logger.info(msg)
        if self.verbose: print(print_color_mapping.get(color) + msg + Style.RESET_ALL, flush=True)

    def _logger_agent_start(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] Start ...\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_end(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] End ...\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_question(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "green"
    ):
        """"""
        if msg is None: msg = f"[{name}] User Question: {content}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages_start(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "red"
    ):
        """"""
        if msg is None: msg = f"{20 * '='} [{name}] Messages Start {20 * '='}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages_end(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            color: Optional[TypePrintColor] = "red"
    ):
        """"""
        if msg is None: msg = f"{20 * '='} [{name}] Messages End    {20 * '='}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_messages(
            self,
            msg: Optional[str] = None,
            role: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "blue"
    ):
        """"""
        if msg is None: msg = f"{role}: [{content}]\n"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_script(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            script: Optional[str] = None,
            color: Optional[TypePrintColor] = "magenta"
    ):
        """"""
        if msg is None: msg = f"[{name}] Script: ```\n{script}\n```"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_search(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "magenta"
    ):
        """"""
        if msg is None: msg = f"[{name}] Script: ```\n{content}\n```"
        self._logger_base(msg=msg, color=color)

    def _logger_agent_warning(self, msg: str, color: Optional[TypePrintColor] = "red"):
        """"""
        self._logger_base(msg=msg, color=color)

    def _logger_agent_final_answer(
            self,
            msg: Optional[str] = None,
            name: Optional[str] = None,
            content: Optional[str] = None,
            color: Optional[TypePrintColor] = "yellow"
    ):
        """"""
        if msg is None: msg = f"[{name}] Final Answer: {content}\n"
        self._logger_base(msg=msg, color=color)

    def _logger_dict(self, msg: Dict, color="green"):
        """"""
        for key, val in msg.items():
            if self.logger: self.logger.info(f"{key}: {val}")
            if self.verbose: print(print_color_mapping.get(color) + f"{key}: {val}" + Style.RESET_ALL, flush=True)

    def _logger_color(self, msg: str) -> None:
        """"""
        last_line = msg.split('\n')[-1]

        if self.logger: self.logger.info(msg)
        if self.verbose:
            if last_line.startswith("Answer"):
                print(Fore.YELLOW + msg + Style.RESET_ALL)
            elif last_line.startswith("Action"):
                print(Fore.GREEN + msg + Style.RESET_ALL)
            elif last_line.startswith("No Action"):
                print(Fore.RED + msg + Style.RESET_ALL)
            elif last_line.startswith("Observation"):
                print(Fore.BLUE + msg + Style.RESET_ALL)
            elif last_line.startswith("Running"):
                print(Fore.CYAN + msg + Style.RESET_ALL)
            else:
                print(msg)
            print()
