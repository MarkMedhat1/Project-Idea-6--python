import tkinter as tk
import sqlite3
import os
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Initialize the SQLite database
conn = sqlite3.connect('supermarket_inventory.db')
yyyy = conn.cursor()

# Create the inventory table if it doesn't exist
yyyy.execute('''CREATE TABLE IF NOT EXISTS inventory (
                product TEXT PRIMARY KEY,
                quantity INTEGER)''')
conn.commit()

# Initialize the inventory data (you can load from the database)
inventory = {}
yyyy.execute('SELECT product, quantity FROM inventory')
for row in yyyy.fetchall():
    product, quantity = row
    inventory[product] = quantity

# Create the main window
root = tk.Tk()
root.title('Supermarket Inventory Management')
root.geometry('400x400')

# Add a label to make it colorful
title_label = tk.Label(root, text='Supermarket Inventory Management', bg='purple', fg='white', font=('Helvetica', 16))
title_label.pack(fill='x')

# Product selection
product_label = tk.Label(root, text='Select Product:', bg='lightblue')
product_var = tk.StringVar()
product_dropdown = tk.OptionMenu(root, product_var, *inventory.keys())
product_label.pack()
product_dropdown.pack()

# Quantity entry
quantity_label = tk.Label(root, text='Quantity to Add:', bg='lightblue')
quantity_entry = tk.Entry(root)
quantity_label.pack()
quantity_entry.pack()

# Add product button
def add_product():
    product_name = product_var.get()
    quantity = int(quantity_entry.get())
    if product_name in inventory:
        inventory[product_name] += quantity
    else:
        inventory[product_name] = quantity
    update_inventory_display()
    product_var.set('')
    quantity_entry.delete(0, tk.END)

add_button = tk.Button(root, text='Add Product', command=add_product, bg='green', fg='white')
add_button.pack()

# Rename product button
def rename_product():
    selected_product = product_var.get()
    new_name = quantity_entry.get()
    if selected_product in inventory:
        inventory[new_name] = inventory.pop(selected_product)
    update_inventory_display()
    product_var.set('')
    quantity_entry.delete(0, tk.END)

rename_button = tk.Button(root, text='Rename Product', command=rename_product, bg='blue', fg='white')
rename_button.pack()

# Remove product button
def remove_product():
    product_name = product_var.get()
    if product_name in inventory:
        del inventory[product_name]
        product_var.set('')
        quantity_entry.delete(0, tk.END)
    update_inventory_display()

remove_button = tk.Button(root, text='Remove Product', command=remove_product, bg='red', fg='white')
remove_button.pack()

# View inventory button
def update_inventory_display():
    inventory_text.config(state=tk.NORMAL)
    inventory_text.delete(1.0, tk.END)

    for product, quantity in inventory.items():
        inventory_text.insert(tk.END, f'{product}: {quantity}\n')

    inventory_text.config(state=tk.DISABLED)

view_button = tk.Button(root, text='View Inventory', command=update_inventory_display, bg='purple', fg='white')
view_button.pack()

# Add quantity button
def add_quantity():
    selected_product = product_var.get()
    quantity_to_add = int(quantity_entry.get())
    if selected_product in inventory:
        inventory[selected_product] += quantity_to_add
        update_inventory_display()
        product_var.set('')
        quantity_entry.delete(0, tk.END)

add_quantity_button = tk.Button(root, text='Add Quantity', command=add_quantity, bg='green', fg='white')
add_quantity_button.pack()

# Remove quantity button
def remove_quantity():
    selected_product = product_var.get()
    quantity_to_remove = int(quantity_entry.get())
    if selected_product in inventory and inventory[selected_product] >= quantity_to_remove:
        inventory[selected_product] -= quantity_to_remove
        update_inventory_display()
        product_var.set('')
        quantity_entry.delete(0, tk.END)
    else:
        messagebox.showerror('Error', 'Insufficient quantity to remove.')

remove_quantity_button = tk.Button(root, text='Remove Quantity', command=remove_quantity, bg='red', fg='white')
remove_quantity_button.pack()

# Save to PDF button
def save_to_pdf():
    desktop_path = os.path.expanduser("~") + "/Desktop/"
    pdf_file_path = desktop_path + "inventory.pdf"

    # Generate the PDF file
    c = canvas.Canvas(pdf_file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Inventory Data")
    c.drawString(100, 730, "Product Name        Quantity")

    y = 710
    for product, quantity in inventory.items():
        c.drawString(100, y, f"{product:<20}{quantity}")
        y -= 15

    c.showPage()
    c.save()

    messagebox.showinfo('Success', f'Inventory data saved to {pdf_file_path}')

save_pdf_button = tk.Button(root, text='Save to PDF', command=save_to_pdf, bg='orange', fg='white')
save_pdf_button.pack()

# Small calculator
calculator_label = tk.Label(root, text='Calculator:', bg='lightblue')
calculator_label.pack()

calculation_var = tk.StringVar()
calculation_entry = tk.Entry(root, textvariable=calculation_var)
calculation_entry.pack()

def calculate():
    try:
        result = eval(calculation_var.get())
        messagebox.showinfo('Result', f'Result: {result}')
    except Exception as e:
        messagebox.showerror('Error', f'Invalid expression: {str(e)}')

calculate_button = tk.Button(root, text='Calculate', command=calculate, bg='blue', fg='white')
calculate_button.pack()

# Display inventory
inventory_text = tk.Text(root, height=10, width=40)
inventory_text.pack()
inventory_text.config(state=tk.DISABLED)

# Initialize the inventory display
update_inventory_display()

# Start the Tkinter main loop
root.mainloop()
