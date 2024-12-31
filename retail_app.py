import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date

# Database connection setups
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Replace with your MySQL root password
        database="app_penjualan"
    )

# Create database and tables if not exists
def setup_database():
    db = connect_to_db()
    cursor = db.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        product_price DECIMAL(10, 2) NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        quantity INT NOT NULL,
        total_price DECIMAL(10, 2) NOT NULL,
        transaction_date DATE NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    )
    """)
    
    db.commit()
    db.close()

setup_database()

# Application class
class RetailApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Retail Management App")
        self.db = connect_to_db()

        self.setup_gui()

    def setup_gui(self):
        # Product Management Frame
        product_frame = ttk.LabelFrame(self.root, text="Manage Products")
        product_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(product_frame, text="Name:").grid(row=0, column=0)
        self.product_name = ttk.Entry(product_frame)
        self.product_name.grid(row=0, column=1)

        ttk.Label(product_frame, text="Price:").grid(row=1, column=0)
        self.product_price = ttk.Entry(product_frame)
        self.product_price.grid(row=1, column=1)

        self.add_product_btn = ttk.Button(product_frame, text="Add Product", command=self.add_product)
        self.add_product_btn.grid(row=2, column=0, pady=5)

        self.update_product_btn = ttk.Button(product_frame, text="Update Product", command=self.update_product)
        self.update_product_btn.grid(row=2, column=1, pady=5)

        self.delete_product_btn = ttk.Button(product_frame, text="Delete Product", command=self.delete_product)
        self.delete_product_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Product List Frame
        product_list_frame = ttk.LabelFrame(self.root, text="Product List")
        product_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        self.product_list = ttk.Treeview(product_list_frame, columns=("ID", "Name", "Price"), show="headings")
        self.product_list.heading("ID", text="ID")
        self.product_list.heading("Name", text="Name")
        self.product_list.heading("Price", text="Price")
        self.product_list.bind("<ButtonRelease-1>", self.select_product)
        self.product_list.pack(fill="both", expand=True)

        self.load_products()

        # Transaction Frame
        transaction_frame = ttk.LabelFrame(self.root, text="Manage Transactions")
        transaction_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        ttk.Label(transaction_frame, text="Product:").grid(row=0, column=0)
        self.product_dropdown = ttk.Combobox(transaction_frame, state="readonly")
        self.product_dropdown.grid(row=0, column=1)
        self.load_products_into_dropdown()

        ttk.Label(transaction_frame, text="Quantity:").grid(row=1, column=0)
        self.quantity = ttk.Entry(transaction_frame)
        self.quantity.grid(row=1, column=1)

        self.add_transaction_btn = ttk.Button(transaction_frame, text="Add Transaction", command=self.add_transaction)
        self.add_transaction_btn.grid(row=2, column=0, columnspan=2, pady=5)

        # Transaction List Frame
        transaction_list_frame = ttk.LabelFrame(self.root, text="Transaction List")
        transaction_list_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        self.transaction_list = ttk.Treeview(transaction_list_frame, columns=("Name", "Quantity", "Total", "Date"), show="headings")
        self.transaction_list.heading("Name", text="Product Name")
        self.transaction_list.heading("Quantity", text="Quantity")
        self.transaction_list.heading("Total", text="Total Price")
        self.transaction_list.heading("Date", text="Transaction Date")
        self.transaction_list.pack(fill="both", expand=True)

        self.load_transactions()

    def load_products(self):
        for row in self.product_list.get_children():
            self.product_list.delete(row)

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM products")
        for pid, name, price in cursor.fetchall():
            self.product_list.insert("", "end", values=(pid, name, price))

    def load_products_into_dropdown(self):
        cursor = self.db.cursor()
        cursor.execute("SELECT product_id, product_name FROM products")
        self.products = {name: pid for pid, name in cursor.fetchall()}
        self.product_dropdown["values"] = list(self.products.keys())

    def load_transactions(self):
        for row in self.transaction_list.get_children():
            self.transaction_list.delete(row)

        cursor = self.db.cursor()
        query = """
        SELECT products.product_name, transactions.quantity, transactions.total_price, transactions.transaction_date
        FROM transactions
        JOIN products ON transactions.product_id = products.product_id
        """
        cursor.execute(query)
        for name, quantity, total, date in cursor.fetchall():
            self.transaction_list.insert("", "end", values=(name, quantity, total, date))

    def select_product(self, event):
        selected = self.product_list.focus()
        if not selected:
            return

        values = self.product_list.item(selected, "values")
        self.selected_product_id = values[0]
        self.product_name.delete(0, tk.END)
        self.product_name.insert(0, values[1])
        self.product_price.delete(0, tk.END)
        self.product_price.insert(0, values[2])

    def add_product(self):
        name = self.product_name.get()
        try:
            price = float(self.product_price.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
            return

        cursor = self.db.cursor()
        cursor.execute("INSERT INTO products (product_name, product_price) VALUES (%s, %s)", (name, price))
        self.db.commit()

        messagebox.showinfo("Success", "Product added successfully")
        self.load_products()
        self.load_products_into_dropdown()
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)

    def update_product(self):
        if not hasattr(self, 'selected_product_id'):
            messagebox.showerror("Error", "Select a product to update")
            return

        name = self.product_name.get()
        try:
            price = float(self.product_price.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid price format")
            return

        cursor = self.db.cursor()
        cursor.execute("UPDATE products SET product_name = %s, product_price = %s WHERE product_id = %s",
                       (name, price, self.selected_product_id))
        self.db.commit()

        messagebox.showinfo("Success", "Product updated successfully")
        self.load_products()
        self.load_products_into_dropdown()
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)

    def delete_product(self):
        if not hasattr(self, 'selected_product_id'):
            messagebox.showerror("Error", "Select a product to delete")
            return

        cursor = self.db.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = %s", (self.selected_product_id,))
        self.db.commit()

        messagebox.showinfo("Success", "Product deleted successfully")
        self.load_products()
        self.load_products_into_dropdown()
        self.product_name.delete(0, tk.END)
        self.product_price.delete(0, tk.END)

    def add_transaction(self):
        product_name = self.product_dropdown.get()
        if not product_name:
            messagebox.showerror("Error", "Select a product")
            return

        try:
            quantity = int(self.quantity.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity format")
            return

        product_id = self.products[product_name]
        cursor = self.db.cursor()
        cursor.execute("SELECT product_price FROM products WHERE product_id = %s", (product_id,))
        product_price = cursor.fetchone()[0]

        total_price = quantity * product_price
        cursor.execute(
            "INSERT INTO transactions (product_id, quantity, total_price, transaction_date) VALUES (%s, %s, %s, %s)",
            (product_id, quantity, total_price, date.today())
        )
        self.db.commit()

        messagebox.showinfo("Success", "Transaction added successfully")
        self.load_transactions()
        self.quantity.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = RetailApp(root)
    root.mainloop()
