import tkinter as tk
from tkinter import messagebox, simpledialog
import mysql.connector
from datetime import datetime
from tkinter import scrolledtext


# Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",  
    database="shopping_mall"
)
cursor = conn.cursor()

# ----------------- PRODUCT FUNCTIONS -----------------
def add_product():
    product_id = simpledialog.askstring("Add Product", "Enter Product ID:")
    if not product_id:
        return

    product_name = simpledialog.askstring("Add Product", "Enter Product Name:")
    quantity = simpledialog.askinteger("Add Product", "Enter Product Quantity:")
    price = simpledialog.askfloat("Add Product", "Enter Product Price:")
    discount = simpledialog.askfloat("Add Product", "Enter Discount (%):")

    try:
        cursor.execute("INSERT INTO product_table (product_id, product_name, quantity, price, discount) VALUES (%s, %s, %s, %s, %s)",
                       (product_id, product_name, quantity, price, discount))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")

def modify_product():
    product_id = simpledialog.askstring("Modify Product", "Enter Product ID to Modify:")
    cursor.execute("SELECT * FROM product_table WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        messagebox.showerror("Error", "Product not found!")
        return

    new_name = simpledialog.askstring("Modify Product", "Enter New Product Name:", initialvalue=product[1])
    new_quantity = simpledialog.askinteger("Modify Product", "Enter New Quantity:", initialvalue=product[2])
    new_price = simpledialog.askfloat("Modify Product", "Enter New Price:", initialvalue=product[3])
    new_discount = simpledialog.askfloat("Modify Product", "Enter New Discount (%):", initialvalue=product[4])

    try:
        cursor.execute("UPDATE product_table SET product_name=%s, quantity=%s, price=%s, discount=%s WHERE product_id=%s",
                       (new_name, new_quantity, new_price, new_discount, product_id))
        conn.commit()
        messagebox.showinfo("Success", "Product modified successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")

def delete_product():
    product_id = simpledialog.askstring("Delete Product", "Enter Product ID to Delete:")
    cursor.execute("SELECT * FROM product_table WHERE product_id=%s", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        messagebox.showerror("Error", "Product not found!")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {product[1]}?")
    if confirm:
        try:
            cursor.execute("DELETE FROM product_table WHERE product_id=%s", (product_id,))
            conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

# ----------------- CUSTOMER FUNCTIONS -----------------
def add_customer():
    customer_id = simpledialog.askstring("Add Customer", "Enter Customer ID:")
    customer_name = simpledialog.askstring("Add Customer", "Enter Customer Name:")
    address = simpledialog.askstring("Add Customer", "Enter Addess:")
    phone = simpledialog.askstring("Add Customer", "Enter Phone Number:")
    
    
    try:
        cursor.execute("INSERT INTO customer_table (customer_id, customer_name,address, phone_no) VALUES (%s, %s, %s, %s)",
                       (customer_id, customer_name, address,phone))
        conn.commit()
        messagebox.showinfo("Success", "Customer added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")

def modify_customer():
    customer_id = simpledialog.askstring("Modify Customer", "Enter Customer ID to Modify:")
    cursor.execute("SELECT * FROM customer_table WHERE customer_id=%s", (customer_id,))
    customer = cursor.fetchone()
    
    if not customer:
        messagebox.showerror("Error", "Customer not found!")
        return

    new_name = simpledialog.askstring("Modify Customer", "Enter New Name:", initialvalue=customer[1])
    new_address = simpledialog.askstring("Modify Customer", "Enter New Address:", initialvalue=customer[2])
    new_phone = simpledialog.askstring("Modify Customer", "Enter New Phone No.:", initialvalue=customer[3])
    

    try:
        cursor.execute("UPDATE customer_table SET customer_name=%s, address=%s, phone_no=%s WHERE customer_id=%s",
                       (new_name, new_address, new_phone, customer_id))
        conn.commit()
        messagebox.showinfo("Success", "Customer modified successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database Error: {err}")

def delete_customer():
    customer_id = simpledialog.askstring("Delete Customer", "Enter Customer ID to Delete:")
    cursor.execute("SELECT * FROM customer_table WHERE customer_id=%s", (customer_id,))
    customer = cursor.fetchone()
    
    if not customer:
        messagebox.showerror("Error", "Customer not found!")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {customer[1]}?")
    if confirm:
        try:
            cursor.execute("DELETE FROM customer_table WHERE customer_id=%s", (customer_id,))
            conn.commit()
            messagebox.showinfo("Success", "Customer deleted successfully!")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

# ----------------- BILL FUNCTIONS -----------------

def generate_bill():
    customer_id = simpledialog.askstring("Create Bill", "Enter Customer ID:")
    cursor.execute("SELECT * FROM customer_table WHERE customer_id=%s", (customer_id,))
    customer = cursor.fetchone()
    
    if not customer:
        messagebox.showerror("Error", "Customer not found!")
        return
    
    items = []
    while True:
        product_id = simpledialog.askstring("Create Bill", "Enter Product ID:")
        cursor.execute("SELECT * FROM product_table WHERE product_id=%s", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            messagebox.showerror("Error", "Product not found!")
            continue
        
        quantity = simpledialog.askinteger("Create Bill", "Enter Quantity:")
        if quantity > product[2]:
            messagebox.showerror("Error", "Not enough stock!")
            continue
        
        discount = product[4]
        price = product[3] * quantity
        discount_amount = (price * discount) / 100
        total_price = price - discount_amount
        
        items.append((product_id, product[1], quantity, product[3], discount, total_price))
        
        cursor.execute("UPDATE product_table SET quantity = quantity - %s WHERE product_id = %s", (quantity, product_id))
        conn.commit()
        
        more = simpledialog.askstring("Create Bill", "Do you want to buy more product <y/n>?")
        if more.lower() != 'y':
            break
    
    bill_no = datetime.now().strftime("%H%M%S")
    bill_text = f"""
    ********************************************************************
                          THE GREAT INDIAN MALL
                          INDIRA NAGAR CHENNAI
    ********************************************************************
    Invoice No: {bill_no}          {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    ********************************************************************
    CUSTOMER_ID: {customer[0]}
    CUSTOMER_NAME: {customer[1]}
    ADDRESS: {customer[2]}
    PHONE_NO: {customer[3]}
    ********************************************************************
    PRODUCT ID   PRODUCT NAME   QUANTITY   PRICE   DISCOUNT(%)   TOTAL
    
    """
    grand_total = 0
    
    for item in items:
        bill_text += f"{item[0]:<12} {item[1]:<14} {item[2]:<9} {item[3]:<7} {item[4]:<10} {item[5]:<8.2f}\n"
        grand_total += item[5]
    
    bill_text += f"""
    ********************************************************************
    Grand Total: {grand_total:.2f}
    ********************************************************************
    THANK YOU!! SEE YOU SOON ☺
    """
    
    cursor.execute("INSERT INTO bill_table (bill_no, customer_id, total_amount) VALUES (%s, %s, %s)",
                   (bill_no, customer_id, grand_total))
    conn.commit()
    
    show_bill(bill_text)

def show_bill(bill_text):
    bill_window = tk.Toplevel(root)
    bill_window.title("Generated Bill")
    bill_window.geometry("500x500")
    
    bill_area = scrolledtext.ScrolledText(bill_window, width=80, height=35, wrap=tk.WORD)
    bill_area.insert(tk.INSERT, bill_text)
    bill_area.config(state=tk.DISABLED)
    bill_area.pack(padx=10, pady=10)

# ----------------- SHOW PRODUCT FUNCTIONS -----------------

def show_products():
    cursor.execute("SELECT * FROM product_table")
    products = cursor.fetchall()
    
    product_window = tk.Toplevel(root)
    product_window.title("Product List")
    product_window.geometry("500x400")
    
    product_text = "Product ID   Product Name   Quantity   Price   Discount\n"
    product_text += "=" * 60 + "\n"
    
    for product in products:
        product_text += f"{product[0]:<12} {product[1]:<14} {product[2]:<9} {product[3]:<7} {product[4]:<10}\n"
    
    text_area = scrolledtext.ScrolledText(product_window, width=60, height=20, wrap=tk.WORD)
    text_area.insert(tk.INSERT, product_text)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10)

    

# ----------------- MENU NAVIGATION -----------------
def open_product_menu():
    main_menu.pack_forget()
    product_menu.pack()

def open_customer_menu():
    main_menu.pack_forget()
    customer_menu.pack()
    
def open_bill_menu():
    generate_bill()

def back_to_main():
    product_menu.pack_forget()
    customer_menu.pack_forget()
    main_menu.pack()

def exit_app():
    conn.close()
    root.destroy()

# ----------------- UI DESIGN -----------------
root = tk.Tk()
root.title("Shopping Mall Management System")
root.geometry("400x300")

# Main Menu
main_menu = tk.Frame(root)
main_menu.pack()

tk.Label(main_menu, text="Main Menu", font=("Arial", 14)).pack(pady=10)
tk.Button(main_menu, text="Product Menu", width=20, command=open_product_menu).pack(pady=5)
tk.Button(main_menu, text="Customer Menu", width=20, command=open_customer_menu).pack(pady=5)
tk.Button(main_menu, text="Bill Menu", width=20,command=open_bill_menu).pack(pady=5)
tk.Button(main_menu, text="Show Products", width=20, command=show_products).pack(pady=5)

tk.Button(main_menu, text="Exit", width=20, command=exit_app).pack(pady=5)

# Product Menu
product_menu = tk.Frame(root)

tk.Label(product_menu, text="Product Menu", font=("Arial", 14)).pack(pady=10)
tk.Button(product_menu, text="Add Product", width=20, command=add_product).pack(pady=5)
tk.Button(product_menu, text="Modify Product", width=20, command=modify_product).pack(pady=5)
tk.Button(product_menu, text="Delete Product", width=20, command=delete_product).pack(pady=5)
tk.Button(product_menu, text="Back to Main Menu", width=20, command=back_to_main).pack(pady=5)

# Customer Menu
customer_menu = tk.Frame(root)

tk.Label(customer_menu, text="Customer Menu", font=("Arial", 14)).pack(pady=10)
tk.Button(customer_menu, text="Add Customer", width=20, command=add_customer).pack(pady=5)
tk.Button(customer_menu, text="Modify Customer", width=20, command=modify_customer).pack(pady=5)
tk.Button(customer_menu, text="Delete Customer", width=20, command=delete_customer).pack(pady=5)
tk.Button(customer_menu, text="Back to Main Menu", width=20, command=back_to_main).pack(pady=5)

# Run the application
root.mainloop()