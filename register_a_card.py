import serial
import mysql.connector as c
import tkinter as tk
from tkinter import messagebox

# Replace with your database connection details
DB_HOST = "10.5.239.97"
DB_USER = "root69"
DB_PASSWORD = "SRM@123"
DB_DATABASE = "food"

# Serial port configuration
serial_port = serial.Serial('COM9', 9600, timeout=1)
serial_port.flush()
# Database connection
con = c.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_DATABASE)
cur = con.cursor()

def read_rfid():
    try:
        while True:
            data = serial_port.readline().decode().strip()
            if data:
                return data
    except serial.SerialException as se:
        messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")

def register_card(name_entry, student_id_entry):
    # Read RFID UID
    rfid_uid = read_rfid()

    # Get user details from Tkinter entries
    name = name_entry.get()
    student_id = student_id_entry.get()

    # Insert data into the database
    try:
        cmd = "INSERT INTO user (name, student_id, rfid_uid, money) VALUES (%s, %s, %s, %s)"
        values = (name, student_id, rfid_uid, 0)  # Default money value is set to 0
        cur.execute(cmd, values)
        con.commit()
        messagebox.showinfo("Success", "Card registered successfully.")
    except c.Error as e:
        messagebox.showerror("Error", f"Error accessing database: {e}")

# GUI setup
window = tk.Tk()
window.title("Card Registration")

# Full screen settings
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
window.geometry(f"{width}x{height}")

# Tkinter entries for name and student ID
name_label = tk.Label(window, text="Enter Name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

student_id_label = tk.Label(window, text="Enter Registration Number:")
student_id_label.pack()
student_id_entry = tk.Entry(window)
student_id_entry.pack()

# Button to trigger card registration
register_button = tk.Button(window, text="Register Card", command=lambda: register_card(name_entry, student_id_entry))
register_button.pack()

window.mainloop()
