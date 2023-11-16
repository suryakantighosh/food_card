import serial
import mysql.connector as c
from mysql.connector import pooling
import tkinter as tk
from tkinter import messagebox
from tkinter import *

# Connection pooling configuration
dbconfig = {
    "host": "10.5.239.97",
    "user": "root69",
    "passwd": "SRM@123",
    "database": "food",
    "pool_name": "mypool",
    "pool_size": 5,
}

# Create a connection pool
pool = pooling.MySQLConnectionPool(**dbconfig)

# Serial port configuration
serial_port = serial.Serial('COM9', 9600, timeout=1)


def read_from_database(card_uid):
    try:
        # Get a connection from the pool
        con = pool.get_connection()

        # Execute database query
        cmd = "SELECT * FROM user WHERE rfid_uid = %s"
        with con.cursor() as cur:
            cur.execute(cmd, (card_uid,))
            user_data = cur.fetchone()

        if user_data:
            # Display user data
            messagebox.showinfo("User Data", f"Name: {user_data[0]}\nRegistration Number: {user_data[1]}\nCard UID: {user_data[2]}\nBalance: {user_data[3]}")
        else:
            # Display message if card not registered
            messagebox.showwarning("Card Not Registered", "Card UID not found in the database.")

    except c.Error as e:
        messagebox.showerror("Error", f"Error accessing database: {e}")

    finally:
        # Close the connection (return it to the pool)
        if con.is_connected():
            con.close()


def rfid():
    try:
        while True:
            data = serial_port.readline().decode().strip()
            print(f"ID: {data}")  # Debug print
            if data:
                try:
                    read_from_database(data)
                    break
                except c.Error as e:
                    messagebox.showerror("Error", f"Error: {e}")
                    break  # Break the loop on error
    except serial.SerialException as se:
        messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")


window = Tk()
window.geometry("600x600")
b1 = tk.Button(window, text="TAP CARD", command=rfid)
b1.pack()

window.mainloop()
