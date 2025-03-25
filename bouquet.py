import sqlite3
from tkinter import *
from tkinter import messagebox
import pandas as pd

# Database functions
def create_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect("bouquet_shop.db")
    return conn

def create_table(conn):
    """Create the bouquets table if it doesn't exist."""
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS bouquets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            flower_type TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        );
        """)

def add_bouquet(conn, name, flower_type, quantity, price):
    """Add a new bouquet to the bouquets table."""
    with conn:
        conn.execute("INSERT INTO bouquets (name, flower_type, quantity, price) VALUES (?, ?, ?, ?)", (name, flower_type, quantity, price))

def get_bouquets(conn):
    """Retrieve all bouquets from the bouquets table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bouquets")
    return cursor.fetchall()

def update_bouquet(conn, bouquet_id, name, flower_type, quantity, price):
    """Update an existing bouquet in the bouquets table."""
    with conn:
        conn.execute("UPDATE bouquets SET name = ?, flower_type = ?, quantity = ?, price = ? WHERE id = ?", (name, flower_type, quantity, price, bouquet_id))

def delete_bouquet(conn, bouquet_id):
    """Delete a bouquet from the bouquets table."""
    with conn:
        conn.execute("DELETE FROM bouquets WHERE id = ?", (bouquet_id,))

def search_bouquet(conn, name):
    """Search for a bouquet by name."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bouquets WHERE name LIKE ?", ('%' + name + '%',))
    return cursor.fetchall()

# GUI functions
def add_bouquet_gui():
    name = name_entry.get()
    flower_type = flower_type_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    
    with create_connection() as conn:
        add_bouquet(conn, name, flower_type, quantity, price)
        messagebox.showinfo("Success", "Bouquet added successfully.")
        clear_entries()

def view_bouquets_gui():
    with create_connection() as conn:
        bouquets = get_bouquets(conn)
        df = pd.DataFrame(bouquets, columns=['ID', 'Name', 'Flower Type', 'Quantity', 'Price'])
        messagebox.showinfo("Bouquets", df.to_string(index=False))

def update_bouquet_gui():
    bouquet_id = int(bouquet_id_entry.get())
    name = name_entry.get()
    flower_type = flower_type_entry.get()
    quantity = int(quantity_entry.get())
    price = float(price_entry.get())
    
    with create_connection() as conn:
        update_bouquet(conn, bouquet_id, name, flower_type, quantity, price)
        messagebox.showinfo("Success", "Bouquet updated successfully.")
        clear_entries()

def delete_bouquet_gui():
    bouquet_id = int(bouquet_id_entry.get())
    
    with create_connection() as conn:
        delete_bouquet(conn, bouquet_id)
        messagebox.showinfo("Success", "Bouquet deleted successfully.")
        clear_entries()

def search_bouquet_gui():
    name = name_entry.get()
    
    with create_connection() as conn:
        bouquets = search_bouquet(conn, name)
        if bouquets:
            df = pd.DataFrame(bouquets, columns=['ID', 'Name', 'Flower Type', 'Quantity', 'Price'])
            messagebox.showinfo("Search Results", df.to_string(index=False))
        else:
            messagebox.showinfo("Search Results", "No bouquets found.")

def clear_entries():
    name_entry.delete(0, END)
    flower_type_entry.delete(0, END)
    quantity_entry.delete(0, END)
    price_entry.delete(0, END)
    bouquet_id_entry.delete(0, END)

# GUI setup
root = Tk()
root.title("Bouquet Shop Application")

# Input fields
Label(root, text="Bouquet ID (for update/delete):").grid(row=0, column=0)
bouquet_id_entry = Entry(root)
bouquet_id_entry.grid(row=0, column=1)

Label(root, text="Bouquet Name:").grid(row=1, column=0)
name_entry = Entry(root)
name_entry.grid(row=1, column=1)

Label(root, text="Flower Type:").grid(row=2, column=0)
flower_type_entry = Entry(root)
flower_type_entry.grid(row=2, column=1)

Label(root, text="Quantity:").grid(row=3, column=0)
quantity_entry = Entry(root)
quantity_entry.grid(row=3, column=1)

Label(root, text="Price:").grid(row=4, column=0)
price_entry = Entry(root)
price_entry.grid(row=4, column=1)

# Buttons
Button(root, text="Add Bouquet", command=add_bouquet_gui).grid(row=5, column=0)
Button(root, text="View Bouquets", command=view_bouquets_gui).grid(row=5, column=1)
Button(root, text="Update Bouquet", command=update_bouquet_gui).grid(row=6, column=0)
Button(root, text="Delete Bouquet", command=delete_bouquet_gui).grid(row=6, column=1)
Button(root, text="Search Bouquet", command=search_bouquet_gui).grid(row=7, column=0)

# Initialize database
with create_connection() as conn:
    create_table(conn)

# Start the GUI event loop
root.mainloop()