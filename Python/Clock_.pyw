import tkinter as tk
import time

digits = {
    "0": [" _ ",
          "| |",
          "|_|"],
    "1": ["   ",
          "  |",
          "  |"],
    "2": [" _ ",
          " _|",
          "|_ "],
    "3": [" _ ",
          " _|",
          " _|"],
    "4": ["   ",
          "|_|",
          "  |"],
    "5": [" _ ",
          "|_ ",
          " _|"],
    "6": [" _ ",
          "|_ ",
          "|_|"],
    "7": [" _ ",
          "  |",
          "  |"],
    "8": [" _ ",
          "|_|",
          "|_|"],
    "9": [" _ ",
          "|_|",
          " _|"],
    ":": ["   ",
          " . ",
          " . "]
}

def update_clock():
    hour = time.strftime("%I").lstrip("0") or "12"
    minute = time.strftime("%M")
    second = time.strftime("%S")
    ampm = time.strftime("%p").lower()

    day = time.strftime("%A")
    date = time.strftime("%d %B %Y")

    full_time = hour + ":" + minute + ":" + second

    lines = ["", "", ""]
    for ch in full_time:
        for i in range(3):
            lines[i] += digits[ch][i] + " "

    text = (
        "\n".join(lines) +
        f"\n\n   {ampm}\n\n     {day}\n     {date}"
    )

    label.config(text=text)
    root.after(1000, update_clock)

# Window
root = tk.Tk()
root.title("Clock")
root.configure(bg="white")
root.resizable(False, False)

# Small locked canvas
root.geometry("340x200")

label = tk.Label(
    root,
    font=("Courier New", 14),
    bg="white",
    fg="black",
    justify="left"
)
label.pack(padx=10, pady=10)

update_clock()
root.mainloop()
