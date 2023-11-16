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

class TransactionApp:
    def __init__(self, master):
        self.master = master
        master.title("Transaction System")

        self.label_receive_user = tk.Label(master, text="Tap card of Payee Store:")
        self.label_receive_user.grid(row=0, column=0, sticky=tk.E)

        self.rfid_receive_user_var = tk.StringVar()
        self.entry_receive_user = tk.Entry(master, textvariable=self.rfid_receive_user_var, state=tk.DISABLED)
        self.entry_receive_user.grid(row=0, column=1)

        self.button_read_receive_user = tk.Button(master, text="Read RFID", command=self.read_receive_user_rfid)
        self.button_read_receive_user.grid(row=0, column=2)

        self.label_amount = tk.Label(master, text="Enter Amount:")
        self.label_amount.grid(row=1, column=0, sticky=tk.E)

        self.amount_var = tk.DoubleVar()
        self.entry_amount = tk.Entry(master, textvariable=self.amount_var)
        self.entry_amount.grid(row=1, column=1)

        self.label_pay_user = tk.Label(master, text="Tap card of Payor:")
        self.label_pay_user.grid(row=2, column=0, sticky=tk.E)

        self.rfid_pay_user_var = tk.StringVar()
        self.entry_pay_user = tk.Entry(master, textvariable=self.rfid_pay_user_var, state=tk.DISABLED)
        self.entry_pay_user.grid(row=2, column=1)

        self.button_read_pay_user = tk.Button(master, text="Read RFID", command=self.read_pay_user_rfid)
        self.button_read_pay_user.grid(row=2, column=2)

        self.button_make_transaction = tk.Button(master, text="Make Transaction", command=self.make_transaction)
        self.button_make_transaction.grid(row=3, column=1)

    def read_receive_user_rfid(self):
        try:
            while True:
                data = serial_port.readline().decode().strip()
                if data:
                    self.rfid_receive_user_var.set(data)
                    break
        except serial.SerialException as se:
            messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")

    def read_pay_user_rfid(self):
        try:
            while True:
                data = serial_port.readline().decode().strip()
                if data:
                    self.rfid_pay_user_var.set(data)
                    break
        except serial.SerialException as se:
            messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")

    def make_transaction(self):
        receive_user_rfid = self.rfid_receive_user_var.get()
        pay_user_rfid = self.rfid_pay_user_var.get()
        amount = self.amount_var.get()

        try:
            # Check if both users exist
            check_receive_user_cmd = "SELECT * FROM user WHERE rfid_uid = %s"
            check_pay_user_cmd = "SELECT * FROM user WHERE rfid_uid = %s"
            cur.execute(check_receive_user_cmd, (receive_user_rfid,))
            receive_user_data = cur.fetchone()
            cur.execute(check_pay_user_cmd, (pay_user_rfid,))
            pay_user_data = cur.fetchone()

            if receive_user_data and pay_user_data:
                # Deduct the amount from the payer's money
                payer_money = pay_user_data[3]
                if payer_money >= amount:
                    new_payer_money = payer_money - amount
                    update_payer_money_cmd = "UPDATE user SET money = %s WHERE rfid_uid = %s"
                    cur.execute(update_payer_money_cmd, (new_payer_money, pay_user_rfid))

                    # Add the amount to the receiver's money
                    receiver_money = receive_user_data[3]
                    new_receiver_money = receiver_money + amount
                    update_receiver_money_cmd = "UPDATE user SET money = %s WHERE rfid_uid = %s"
                    cur.execute(update_receiver_money_cmd, (new_receiver_money, receive_user_rfid))

                    con.commit()
                    messagebox.showinfo("Success", "Transaction successful.")
                    self.clear_entries()
                else:
                    messagebox.showerror("Insufficient money", "Not enough money to make the transaction.")
            else:
                messagebox.showerror("User Not Found", "One or both users not found.")
        except c.Error as e:
            messagebox.showerror("Error", f"Error accessing database: {e}")

    def clear_entries(self):
        self.amount_var.set(0.0)
        self.rfid_pay_user_var.set("")

# GUI setup
root = tk.Tk()
app = TransactionApp(root)
root.mainloop()

# Close the connection
con.close()
