import csv
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

INVENTORY_FILE = 'inventory.json'
MAX_INVENTORY_FILE = 'max_inventory.json'

def load_inventory(file_path):
    inventory = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            inventory.append({
                'name': row[2],
                'current_inventory': float(row[3])
            })
    save_inventory(inventory)
    return inventory

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as file:
        json.dump(inventory, file)

def load_saved_inventory():
    try:
        with open(INVENTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_max_inventory_values(max_inventory_values, day):
    try:
        with open(MAX_INVENTORY_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    data[day] = max_inventory_values
    with open(MAX_INVENTORY_FILE, 'w') as file:
        json.dump(data, file)

def load_max_inventory_values(day):
    try:
        with open(MAX_INVENTORY_FILE, 'r') as file:
            data = json.load(file)
            return data.get(day, {})
    except FileNotFoundError:
        return {}

def initialize_max_inventory(day):
    inventory = load_saved_inventory()
    max_inventory_values = load_max_inventory_values(day)
    if not max_inventory_values:
        max_inventory_values = {item['name']: 0 for item in inventory}
        save_max_inventory_values(max_inventory_values, day)
    return max_inventory_values

def calculate_order_quantity(current_inventory, max_inventory, case_size):
    order_quantity = max_inventory - current_inventory
    if order_quantity <= 0:
        return 0
    else:
        return ((order_quantity + case_size - 1) // case_size) * case_size

def load_inventory_and_display():
    inventory_file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not inventory_file:
        return
    
    inventory = load_inventory(inventory_file)
    display_inventory(inventory)

def display_inventory(inventory):
    for item in tree_inventory.get_children():
        tree_inventory.delete(item)
    for item in inventory:
        tree_inventory.insert("", "end", values=(item['name'], item['current_inventory']))

def calculate_and_display_order():
    inventory = load_saved_inventory()
    selected_day = day_combobox.get()
    max_inventory_values = load_max_inventory_values(selected_day)
    
    for item in tree_order.get_children():
        tree_order.delete(item)
    for item in inventory:
        max_inventory = max_inventory_values.get(item['name'], 0)
        order_quantity = calculate_order_quantity(item['current_inventory'], max_inventory, case_size=1)
        if order_quantity > 0:
            tree_order.insert("", "end", values=(item['name'], item['current_inventory'], order_quantity))

def create_max_inventory_tab(tab):
    days = ["Saturday", "Sunday", "Monday", "Thursday"]
    selected_day = tk.StringVar()
    selected_day.set(days[0])
    
    max_inventory_values = initialize_max_inventory(days[0])
    
    canvas = tk.Canvas(tab)
    scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    labels = []
    entries = []
    for i, (name, max_value) in enumerate(max_inventory_values.items()):
        label = tk.Label(scrollable_frame, text=name)
        label.grid(row=i, column=0)
        labels.append(label)
        
        entry = tk.Entry(scrollable_frame)
        entry.insert(0, str(max_value))
        entry.grid(row=i, column=1)
        entries.append(entry)
    
    def on_submit():
        new_max_inventory_values = {}
        for label, entry in zip(labels, entries):
            try:
                new_max_inventory_values[label.cget("text")] = float(entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers for max inventory values.")
                return
        save_max_inventory_values(new_max_inventory_values, day_combobox.get())
        messagebox.showinfo("Success", "Max inventory values updated successfully.")
    
    submit_button = tk.Button(scrollable_frame, text="Submit", command=on_submit)
    submit_button.grid(row=len(max_inventory_values), columnspan=2)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

root = tk.Tk()
root.title("Inventory Management")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

inventory_tab = ttk.Frame(notebook)
notebook.add(inventory_tab, text="Inventory")

max_inventory_tab = ttk.Frame(notebook)
notebook.add(max_inventory_tab, text="Set Max Inventory")

tree_inventory = ttk.Treeview(inventory_tab, columns=("Name", "Current Inventory"), show="headings")
tree_inventory.heading("Name", text="Name")
tree_inventory.heading("Current Inventory", text="Current Inventory")
tree_inventory.pack(expand=True, fill='both')

tree_order = ttk.Treeview(inventory_tab, columns=("Name", "Current Inventory", "Order Quantity"), show="headings")
tree_order.heading("Name", text="Name")
tree_order.heading("Current Inventory", text="Current Inventory")
tree_order.heading("Order Quantity", text="Order Quantity")
tree_order.pack(expand=True, fill='both')

days = ["Saturday", "Sunday", "Monday", "Thursday"]
selected_day = tk.StringVar()
selected_day.set(days[0])

day_label = tk.Label(inventory_tab, text="Select Day:")
day_label.pack()

day_combobox = ttk.Combobox(inventory_tab, values=days, textvariable=selected_day)
day_combobox.pack()

load_button = tk.Button(inventory_tab, text="Load Inventory CSV", command=load_inventory_and_display)
load_button.pack()

calculate_button = tk.Button(inventory_tab, text="Calculate Order", command=calculate_and_display_order)
calculate_button.pack()

create_max_inventory_tab(max_inventory_tab)

# Load the current inventory count on run
current_inventory = load_saved_inventory()
display_inventory(current_inventory)

root.mainloop()