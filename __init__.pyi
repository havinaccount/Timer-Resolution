import tkinter as tk
from tkinter import ttk
from typing import Union

__version__: str
author: str

root: tk.Tk

maxres: int
minres: int
current: int
default_res: int

def format_ms(value: int) -> str:
    ...

def max_timer() -> int:
    ...

def default_timer() -> int:
    ...

def on_exit() -> None:
    ...

def exit_out() -> None:
    ...

def custom_res_window() -> None:
    def close_warning() -> None:
        ...
    
    def clicked(event=None) -> None:
        ...

def center_window(window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
    ...

WINDOW_WIDTH: int
WINDOW_HEIGHT: int

lbl: tk.Label
lbl2: tk.Label
lbl3: tk.Label

btn_frame: tk.Frame

btn: ttk.Button
btn2: ttk.Button
btn3: ttk.Button
btn4: ttk.Button