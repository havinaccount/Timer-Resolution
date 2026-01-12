"""
Set/Get Timer Resolution with GUI and
using Tkinter
"""

# ` It is recommended to use the Better Comments extension
# ` while viewing this code in Visual Studio Code
# Any "``" symbol refers to bold format

import logging
import sys  # Use the sys module when needed
import tkinter as tk
from compileall import compile_dir
from tkinter import ttk  # For native widgets
from typing import Final, Literal, Union

import wres

__version__: Literal["1.1.0"] = "1.1.0"
__author__: Literal["havinaccount"] = "havinaccount"

logging.basicConfig(
    filename="runtime.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s - Line %(lineno)d - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Compile all .py files to .pyc bytecode for future faster execution
compile_dir(dir=".", optimize=2, quiet=1)
# ` This is basically covering linux even though NtSystemTimer is a Windows API
# // os.system('clear' if os.name == 'posix' else 'cls')

# Initialize a window
root: tk.Tk = tk.Tk()

# Save the current timer
maxres, minres, current = wres.query_resolution()
maxres: int
minres: int
current: int
DEFAULT_RES: Final[int] = 162500


def format_ms(value: int) -> str:
    """
    Format any value to milliseconds because of the Windows API convention
    that reports in 100ns (nanoseconds).

    Refer to documentation:
    http://undocumented.ntinternals.net/index.html?page=UserMode2FUndocumented20Functions2FTime2FNtQueryTimerResolution.html
    """
    return f"{value/10000:.3f} ms"


def max_timer(event: object = None) -> int:
    """
    Sets the value NTSystemTimer to it's max using NtSetSystemTime
    """
    with wres.set_resolution(5000):
        logging.info("Changed NTSystemTimer value to 0.5ms")
        _, _, current = wres.query_resolution()
        current: int
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


def default_timer(event: object = None) -> int:
    """
    Sets NTSystemTimer value back to the default using NtSetSystemTime
    """
    with wres.set_resolution(162500):
        logging.info("Changed NTSystemTimer value to 16.25ms")
        _, _, current = wres.query_resolution()
        current: int
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


def on_exit() -> None:
    """
    Reset the NTSystemTimer on exit using NtSetSystemTime
    Arguments:
    event: Used for keybindings functionality
    """
    with wres.set_resolution(DEFAULT_RES):
        logging.info("App killed")
    root.destroy()


def exit_out(event: object = None) -> None:
    """
    Exit the app
    Arguments:
    event: Used for keybindings functionality
    """
    root.destroy()


def custom_res_window(event: object = None) -> None:
    """
    Make a window for setting custom resolutions
    """
    custom_res: tk.Toplevel = tk.Toplevel(root)
    custom_res.title("Custom Resolution")
    center_window(custom_res, 200, 110)
    custom_res.resizable(width=False, height=False)
    custom_res.withdraw()  # Hide until warning is acknowledged
    custom_res.bind("<Escape>", exit_out)

    logging.info("Custom Resolution Window created")

    # Create the warning window
    warning: tk.Toplevel = tk.Toplevel(root)
    warning.title("Warning")
    center_window(warning, 375, 125)
    warning.resizable(width=False, height=False)
    warning.focus_force()

    warning_lbl: tk.Label = tk.Label(
        warning,
        text="""Please type your value in 100ns units, For example: 0.5ms is 5000ns.
        Also, Changing resolution may affect system stability.
        Proceed with caution!""",
    )
    warning_lbl.pack(pady=10)

    # Function for opening custom
    def close_warning() -> None:
        warning.destroy()
        custom_res.deiconify()  # Show custom resolution after the window is closed
        custom_res.attributes("-topmost", True)
        custom_res.focus_force()
        custom_res.grab_set()

    warning.protocol("WM_DELETE_WINDOW", close_warning)

    confirm_btn: ttk.Button = ttk.Button(warning, text="Ok", command=close_warning)
    confirm_btn.pack(pady=10)

    # Block interaction with other windows until warning is closed
    warning.attributes("-topmost", True)
    warning.grab_set()
    root.wait_window(warning)

    # --- Custom Resolution UI ---
    try:
        custom_res_lbl: tk.Label = tk.Label(
            master=custom_res, text=f"Current Resolution: {format_ms(current)}"
        )
    except tk.TclError as e:
        e: tk.TclError
        logging.error("Exited before window creation: %s", e)
        sys.exit(0)

    custom_res_lbl.pack(pady=10)

    entry: ttk.Entry = ttk.Entry(master=custom_res, width=28)
    entry.pack()

    def set_custom(event: object = None) -> None:
        try:
            res: int = int(entry.get())
        except ValueError as e:
            logging.error("Used an unknown data type, Probably a str: %s", e)
            custom_res_lbl.config(text="Only numeric values are allowed.")
            raise
        if not res:
            return
        with wres.set_resolution(res):
            logging.info("Changed NTSystemTimer value to %sms", format_ms(res))
            _, _, current = wres.query_resolution()
            current: int
            custom_res_lbl.config(text=f"Current Resolution: {format_ms(current)}")
            lbl.config(text=f"Current Resolution: {format_ms(current)}")

    custom_res_btn: ttk.Button = ttk.Button(
        custom_res, text="Apply", command=set_custom
    )
    custom_res_btn.pack(pady=10)

    custom_res.bind("<Return>", set_custom)


def center_window(  # type: ignore
    window: Union[tk.Tk, tk.Toplevel], width: int, height: int
) -> None:
    """
    Centers any window given using basic math
    Arguments:
    window: A window to center it's position to screen
    width: The width of the window
    height: The height of the window
    """
    screen_width: int = window.winfo_screenwidth()
    screen_height: int = window.winfo_screenheight()
    x: int = (screen_width // 2) - (width // 2)
    y: int = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Configuration for the app
WINDOW_WIDTH: Final[int] = 400
WINDOW_HEIGHT: Final[int] = 110

center_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
root.resizable(width=False, height=False)
root.title("Timer Resolution")

lbl: tk.Label = tk.Label(text=f"Current Resolution: {format_ms(current)}")
lbl.pack()

lbl2: tk.Label = tk.Label(text=f"Maximum Resolution: {format_ms(minres)}")
lbl2.pack()

lbl3: tk.Label = tk.Label(text=f"Maximum Resolution: {format_ms(maxres)}")
lbl3.pack()

btn_frame: tk.Frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn: ttk.Button = ttk.Button(btn_frame, text="Maximum", command=max_timer)
root.bind("<m>", max_timer)
btn.pack(side="left", padx=10)

btn2: ttk.Button = ttk.Button(btn_frame, text="Default", command=default_timer)
root.bind("<d>", default_timer)
btn2.pack(side="left", padx=10)

btn3: ttk.Button = ttk.Button(btn_frame, text="Custom", command=custom_res_window)
root.bind("<c>", custom_res_window)
btn3.pack(side="left", padx=10)

btn4: ttk.Button = ttk.Button(btn_frame, text="Exit", command=exit_out)
btn4.pack(side="left", padx=10)

# Trigger 'on_exit()' when window is closed
root.protocol("WM_DELETE_WINDOW", on_exit)

# Use a keybind for exiting the app
root.bind("<Escape>", exit_out)

# Run the app
if __name__ == "__main__":
    logging.info("Executed as an application")
    logging.info(
        "Any set_resolution log comes from wres module, You can ignore those messages"
    )
    root.mainloop()
