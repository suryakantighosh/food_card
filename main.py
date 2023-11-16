import tkinter as tk
import subprocess

def run_register_card():
    subprocess.run(['python', 'register_a_card.py'])

def run_view_card():
    subprocess.run(['python', 'read.py'])

def run_top_up_card():
    subprocess.run(['python', 'top_up_card.py'])

def exit_application():
    root.destroy()

# GUI setup
root = tk.Tk()
root.title("Kiosk Application")

# Full screen settings
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}")

# Buttons
button_a = tk.Button(root, text="Register a New Card", command=run_register_card)
button_a.pack(pady=10)

button_b = tk.Button(root, text="View Card Detail", command=run_view_card)
button_b.pack(pady=10)

button_c = tk.Button(root, text="Manually Top Up a Card", command=run_top_up_card)
button_c.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=exit_application)
exit_button.pack(pady=10)

root.mainloop()
