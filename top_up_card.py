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

# Database connection
con = c.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_DATABASE)
cur = con.cursor()

class TopUpCardApp:
    def __init__(self, master):
        self.master = master
        master.title("Top Up Card")

        self.label_rfid_uid = tk.Label(master, text="RFID UID:")
        self.label_rfid_uid.grid(row=0, column=0, sticky=tk.E)

        self.rfid_uid_var = tk.StringVar()
        self.entry_rfid_uid = tk.Entry(master, textvariable=self.rfid_uid_var, state=tk.DISABLED)
        self.entry_rfid_uid.grid(row=0, column=1)

        self.button_read_rfid = tk.Button(master, text="Read RFID", command=self.read_rfid)
        self.button_read_rfid.grid(row=0, column=2)

        self.label_top_up_amount = tk.Label(master, text="Top Up Amount:")
        self.label_top_up_amount.grid(row=1, column=0, sticky=tk.E)

        self.top_up_amount_var = tk.DoubleVar()
        self.entry_top_up_amount = tk.Entry(master, textvariable=self.top_up_amount_var)
        self.entry_top_up_amount.grid(row=1, column=1)

        self.label_balance = tk.Label(master, text="Current Balance:")
        self.label_balance.grid(row=2, column=0, sticky=tk.E)

        self.balance_var = tk.StringVar()
        self.label_display_balance = tk.Label(master, textvariable=self.balance_var)
        self.label_display_balance.grid(row=2, column=1)

        self.button_top_up = tk.Button(master, text="Top Up", command=self.top_up_card)
        self.button_top_up.grid(row=3, column=1)

    def read_rfid(self):
        try:
            while True:
                data = serial_port.readline().decode().strip()
                if data:
                    self.rfid_uid_var.set(data)
                    self.update_balance_display()
                    break
        except serial.SerialException as se:
            messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")

    def update_balance_display(self):
        rfid_uid = self.rfid_uid_var.get()
        try:
            get_balance_cmd = "SELECT money FROM user WHERE rfid_uid = %s"
            cur.execute(get_balance_cmd, (rfid_uid,))
            current_balance = cur.fetchone()[0]
            self.balance_var.set(current_balance)
        except c.Error as e:
            messagebox.showerror("Error", f"Error accessing database: {e}")

    def top_up_card(self):
        rfid_uid = self.rfid_uid_var.get()
        top_up_amount = self.top_up_amount_var.get()

        try:
            get_balance_cmd = "SELECT money FROM user WHERE rfid_uid = %s"
            cur.execute(get_balance_cmd, (rfid_uid,))
            current_balance = cur.fetchone()[0]

            new_balance = current_balance + top_up_amount
            update_balance_cmd = "UPDATE user SET money = %s WHERE rfid_uid = %s"
            cur.execute(update_balance_cmd, (new_balance, rfid_uid))
            con.commit()

            self.update_balance_display()

            messagebox.showinfo("Success", f"Card topped up successfully. New balance: {new_balance}")
        except c.Error as e:
            messagebox.showerror("Error", f"Error accessing database: {e}")

# GUI setup
root = tk.Tk()
app = TopUpCardApp(root)
root.mainloop()

# Close the connection
con.close()
