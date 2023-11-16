import tkinter as tk
from tkinter import messagebox
import mysql.connector as c
import serial

DB_HOST = "10.5.239.97"
DB_USER = "root69"
DB_PASSWORD = "SRM@123"
DB_DATABASE = "food"

serial_port = serial.Serial('COM9', 9600, timeout=1)
con = c.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, database=DB_DATABASE)
cur = con.cursor()

class StoreApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TapFood Store")
        self.geometry("600x400")

        self.item_prices = {
            'Veg Roll': 50,
            'Egg Roll': 60,
            'Chicken Roll': 70
        }

        self.cart = {}  # Dictionary to store item names and prices separately

        self.create_widgets()

    def create_widgets(self):
        # Item selection listbox
        self.item_listbox = tk.Listbox(self)
        for item in self.item_prices.keys():
            self.item_listbox.insert(tk.END, item)
        self.item_listbox.pack(side=tk.LEFT, padx=10, pady=10)

        # Cart listbox
        self.cart_listbox = tk.Listbox(self)
        self.cart_listbox.pack(side=tk.RIGHT, padx=10, pady=10)

        # Add to Cart button
        add_to_cart_button = tk.Button(self, text="Add to Cart", command=self.add_to_cart)
        add_to_cart_button.pack(pady=5)

        # Remove from Cart button
        remove_from_cart_button = tk.Button(self, text="Remove from Cart", command=self.remove_from_cart)
        remove_from_cart_button.pack(pady=5)

        # Checkout button
        checkout_button = tk.Button(self, text="Checkout", command=self.checkout)
        checkout_button.pack(pady=5)

        # Total amount label
        self.total_amount_label = tk.Label(self, text="Total Amount: ₹0")
        self.total_amount_label.pack(pady=5)

    def add_to_cart(self):
        selected_item_index = self.item_listbox.curselection()

        if selected_item_index:
            # Get the selected item
            item = self.item_listbox.get(selected_item_index)
            
            # Store item name in cart dictionary with a unique key to allow multiple instances of the same item
            key = f"{item} - {len([i for i in self.cart.keys() if item in i]) + 1}"
            self.cart[key] = self.item_prices[item]
            self.update_cart_listbox()

    def remove_from_cart(self):
        selected_items = [self.cart_listbox.get(idx) for idx in self.cart_listbox.curselection()]
        for item in selected_items:
            # Extract item name from the string
            item_name = item.split(' - ')[0]
            # Remove item from cart dictionary
            for key in list(self.cart.keys()):
                if item_name in key:
                    del self.cart[key]
        self.update_cart_listbox()

    def update_cart_listbox(self):
        self.cart_listbox.delete(0, tk.END)
        total_amount = sum(self.cart.values())
        for item, price in self.cart.items():
            # Display item name along with price
            self.cart_listbox.insert(tk.END, f"{item} - ₹{price}")
        self.total_amount_label.config(text=f"Total Amount: ₹{total_amount}")

    def checkout(self):
        rfid_uid = self.read_rfid()
        total_amount = sum(self.cart.values())

        try:
            self.deduct_amount(rfid_uid, total_amount)
            messagebox.showinfo("Checkout Successful", f"Total Amount: ₹{total_amount} deducted from user's balance.")
            self.cart = {}  # Clear the cart after successful checkout
            self.update_cart_listbox()
        except Exception as e:
            messagebox.showerror("Error", f"Error during checkout: {e}")

    def read_rfid(self):
        try:
            while True:
                data = serial_port.readline().decode().strip()
                if data:
                    return data
        except serial.SerialException as se:
            messagebox.showerror("Serial Port Error", f"Error accessing serial port: {se}")

    def deduct_amount(self, rfid_uid, amount):
        try:
            get_balance_cmd = "SELECT money FROM user WHERE rfid_uid = %s"
            cur.execute(get_balance_cmd, (rfid_uid,))
            current_balance = cur.fetchone()[0]

            if current_balance >= amount:
                new_balance = current_balance - amount
                update_balance_cmd = "UPDATE user SET money = %s WHERE rfid_uid = %s"
                cur.execute(update_balance_cmd, (new_balance, rfid_uid))
                con.commit()
            else:
                raise Exception("Insufficient balance")

        except c.Error as e:
            raise Exception(f"Error accessing database: {e}")


if __name__ == "__main__":
    app = StoreApp()
    app.mainloop()
