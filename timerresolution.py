"""
A Simple Tool for changing the value of NTSystemTimer
to achieve Less latency and optimized polling rate
"""

import tkinter as tk
from tkinter import ttk
from typing import Union

import wres

# Initialize a window
root: tk.Tk = tk.Tk()

# Save the current timer
maxres, minres, current = wres.query_resolution()
default_res: int = current


def format_ms(value: int) -> str:
    """
    Format any value to milliseconds because of the Windows API convention
    that reports in 100ns (nanoseconds):
    http://undocumented.ntinternals.net/index.html?page=UserMode2FUndocumented20Functions2FTime2FNtQueryTimerResolution.html
    """
    return f"{value/10000:.3f} ms"


def max_timer() -> int:
    """
    Sets the value NTSystemTimer to it's max using NtSetSystemTime
    """
    with wres.set_resolution(5000):
        _, _, current = wres.query_resolution()
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


def default_timer() -> int:
    """
    Sets NTSystemTimer value back to the default using NtSetSystemTime
    """
    with wres.set_resolution(162500):
        _, _, current = wres.query_resolution()
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


def on_exit() -> None:
    """
    Reset the NTSystemTimer on exit using NtSetSystemTime
    """
    with wres.set_resolution(default_res):
        pass
    root.destroy()


def exit_out() -> None:
    """
    Exit the app
    """
    root.destroy()


def custom_res_window() -> None:
    """
    Make a window for setting custom resolutions
    """
    custom_res: tk.Toplevel = tk.Toplevel(root)
    custom_res.title("Custom Resolution")
    center_window(custom_res, 200, 110)
    custom_res.resizable(width=False, height=False)
    custom_res.withdraw()  # Hide until warning is acknowledged

    # Create the warning window
    warning: tk.Toplevel = tk.Toplevel(root)
    warning.title("Warning")
    center_window(warning, 375, 125)
    warning.resizable(width=False, height=False)

    warning_lbl: tk.Label = tk.Label(
        warning,
        text="Please type your value in 100ns units, For example: 0.5ms is 5000ns.\nAlso, Changing resolution may affect system stability.\nProceed with caution!",
    )
    warning_lbl.pack(pady=10)

    # Function for opening custom
    def close_warning() -> None:
        warning.destroy()
        custom_res.deiconify()  # Show custom resolution after the window is closed
        custom_res.attributes("-topmost", True)
        custom_res.focus_force()
        custom_res.grab_set()

    confirm_btn: ttk.Button = ttk.Button(warning, text="Ok", command=close_warning)
    confirm_btn.pack(pady=10)

    # Block interaction with other windows until warning is closed
    warning.attributes("-topmost", True)
    warning.grab_set()
    root.wait_window(warning)

    # --- Custom Resolution UI ---
    custom_res_lbl: tk.Label = tk.Label(
        master=custom_res, text=f"Current Resolution: {format_ms(current)}"
    )
    custom_res_lbl.pack(pady=10)

    entry: ttk.Entry = ttk.Entry(master=custom_res, width=28)
    entry.pack()

    def clicked(event: object=None) -> None:
        res: str = str(entry.get())
        if not res:
            return
        try:
            with wres.set_resolution(int(res)):
                _, _, current = wres.query_resolution()
                custom_res_lbl.config(text=f"Current Resolution: {format_ms(current)}")
                lbl.config(text=f"Current Resolution: {format_ms(current)}")
        except ValueError:
            custom_res_lbl.config(text="Only numeric values are allowed.")
            raise

    custom_res_btn: ttk.Button = ttk.Button(custom_res, text="Apply", command=clicked)
    custom_res_btn.pack(pady=10)

    custom_res.bind("<Return>", clicked)


def center_window(window: Union[tk.Tk, tk.Toplevel], width: int, height: int) -> None:
    """
    Centers any window given using basic math
    """
    screen_width: int = window.winfo_screenwidth()
    screen_height: int = window.winfo_screenheight()
    x: int = (screen_width // 2) - (width // 2)
    y: int = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Configuration for the app
WINDOW_WIDTH: int = 400
WINDOW_HEIGHT: int = 110

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
btn.pack(side="left", padx=10)

btn2: ttk.Button = ttk.Button(btn_frame, text="Default", command=default_timer)
btn2.pack(side="left", padx=10)

btn3: ttk.Button = ttk.Button(btn_frame, text="Custom", command=custom_res_window)
btn3.pack(side="left", padx=10)

btn4: ttk.Button = ttk.Button(btn_frame, text="Exit", command=exit_out)
btn4.pack(side="left", padx=10)

# Trigger 'on_exit()' when window is closed
root.protocol("WM_DELETE_WINDOW", on_exit)

# Run the app
if __name__ == "__main__":
    root.mainloop()
