import tkinter as tk
from tkinter import ttk
from typing import Final, Literal, Union

__version__: Literal["1.1.1"]
__author__: Literal["havinaccount"]

root: tk.Tk

maxres: int
minres: int
current: int
DEFAULT_RES: Final[int]

def format_ms(value: int) -> str: ...
def max_timer(event: object) -> int: ...
def default_timer(event: object) -> int: ...
def on_exit(event: object) -> None: ...
def exit_out(event: object) -> None: ...
def custom_res_window(event: object) -> None:
    def close_warning(event: object) -> None: ...
    def clicked(event: object = None) -> None: ...

def center_window(
    window: Union[tk.Tk, tk.Toplevel], width: int, height: int
) -> None: ...

WINDOW_WIDTH: Final[int]
WINDOW_HEIGHT: Final[int]

lbl: tk.Label
lbl2: tk.Label
lbl3: tk.Label

btn_frame: tk.Frame

btn: ttk.Button
btn2: ttk.Button
btn3: ttk.Button
btn4: ttk.Button
