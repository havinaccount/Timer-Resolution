import tkinter as tk
from tkinter import ttk

import wres

# Initialize a window
root: tk.Tk = tk.Tk()

# Save the current timer
maxres, minres, current = wres.query_resolution()
default_res: int = current


# Format it to milliseconds because of the Windows API convention
# that reports in ns (nanoseconds) http://undocumented.ntinternals.net/index.html?page=UserMode2FUndocumented20Functions2FTime2FNtQueryTimerResolution.html
def format_ms(value: int) -> str:
    return f"{value/10000:.3f} ms"


# Sets the value to it's max
def max_timer() -> int:
    with wres.set_resolution(5000):
        _, _, current = wres.query_resolution()
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


# Set it back to the default value
def default_timer() -> int:
    with wres.set_resolution(162500):
        _, _, current = wres.query_resolution()
        lbl.config(text=f"Current Resolution: {format_ms(current)}")
        return current


# Reset the timer on exit
def on_exit() -> None:
    with wres.set_resolution(default_res):
        pass
    root.destroy()


# Exit the app
def exit_out() -> None:
    root.destroy()


# Configuration for the app
root.geometry("300x110")
root.resizable(width=False, height=False)
root.title("Timer Resolution")

lbl: tk.Label = tk.Label(text=f"Current Resolution: {format_ms(current)}")
lbl.pack()

lbl2 = tk.Label(text=f"Maximum Resolution: {minres}")
lbl2.pack()

lbl3 = tk.Label(text=f"Maximum Resolution: {maxres}")
lbl3.pack()

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn: ttk.Button = ttk.Button(btn_frame, text="Maximum", command=max_timer)
btn.pack(side="left", padx=10)

btn2: ttk.Button = ttk.Button(btn_frame, text="Default", command=default_timer)
btn2.pack(side="left", padx=10)

btn3: ttk.Button = ttk.Button(btn_frame, text="Exit", command=exit_out)
btn3.pack(side="left", padx=10)

# Trigger 'on_exit()' when window is closed
root.protocol("WM_DELETE_WINDOW", on_exit)

# Run the app
if __name__ == "__main__":
    root.mainloop()
