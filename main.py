import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import csv
from datetime import datetime

# shipment schedule - Days when shipments are received
shipments = ["Monday", "Tuesday", "Wednesday", "Saturday"]

# Replace with actual inventory items, divided into groups for each tab
tab_inventory_items = {
    "Janitorial": ["3M #105 Green Scouring Pad", "Degreser, Heavy Duty 4ct", "Delimer Solution", "Esteem Dry-All", "Esteem Sani NC", "Grill Bricks", "Kay Liquid Disinfectant Cleanser", "Kay Neutral Floor Cleaner", "KayQuat Sanitizer", "Multi-Fold Towels", "Pot and Pan Detergent"],
    "Janitorial Cont.": ["Power Pad Eraser", "Purell Surface Sanitizer Gallons", "Purell, Healthy Gentle Soap", "Purell, Sanitizer", "Machine Warewash Detergent", "Toilet Tissue", "Trash Liner", "Victory Wash"],
    "Paper": ["12# Paper Bag", "16oz Paper Cup", "22oz Paper Cup", "25# Paper Bag", "32oz Paper Cup", "4oz Portion Cup", "6# Paper Bag", "Burrito Bowl", "Foil Roll", "Food Container Lid", "Food Container", "Fork Black"],
    "Paper Cont.": ["Spoon Clear", "Straws", "Kids Meal Tray", "Kids Meal Insert", "Kids Meal Lids", "Knife Black", "Lid 16/22oz", "4oz Lid", "Napkins, Printed", "Rope Handle Bags"],
}

# Load existing data if the file exists, otherwise initialize empty data
data_file = "inventory_data.json"
if os.path.exists(data_file):
    with open(data_file, "r") as file:
        saved_data = json.load(file)
else:
    saved_data = {"inventory": {}, "usage_history": {}}

# Ensure "usage_history" key exists in saved_data
if "usage_history" not in saved_data:
    saved_data["usage_history"] = {}

# Ensure all items have initial values of 0 if not already in saved data
for group in tab_inventory_items.values():
    for item in group:
        saved_data["inventory"].setdefault(item, 0)
        saved_data["usage_history"].setdefault(item, [])

# Function to get the number of days until the next shipment
def days_until_next_shipment():
    today = datetime.now().strftime("%A")
    for shipment_day in shipments:
        if shipment_day == today:
            return 1 # If today is a shipment day, the next shipment is tomorrow
        elif shipment_day > today:
            return (datetime.strptime(shipment_day, "%A") - datetime.strptime(today, "%A")).days
    # If no more shipments this week, use the first shipment of the next week
    return (7 - datetime.now(). weekday() + shipments[0]. weekday()) % 7

# Initialize the main window
root = tk.Tk()
root.title("Inventory Order Calculator")
root.geometry("600x600")

# Create the Notebook (tab manager)
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Create a tab for each group of items
inventory_entries = {}

# Function to focus the next widget and highlight its value
def focus_and_highlight(event):
    next_widget = event.widget.tk_focusNext()
    next_widget.focus()
    next_widget.select_range(0, tk.END)
    return "break"

# Function to highlight the value when the field is clicked
def highlight_on_focus(event):
    event.widget.select_range(0, tk.END)
    return "break"

# Function to update entry background based on value
def update_entry_background(entry):
    try:
        value = float(entry.get())
        if value <= 1:
            entry.config(bg="red")
        else:
            entry.config(bg="white")
    except ValueError:
        entry.config(bg="red")  # Invalid value should also show an alert color

# Create tabs and add entries for inventory items
for group_name, items in tab_inventory_items.items():
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=group_name)

    # Add entry fields for each item in the group
    for row_num, item in enumerate(items):
        tk.Label(tab, text=f"{item} (Cases):").grid(row=row_num, column=0, padx=10, pady=5, sticky="w")
        entry = tk.Entry(tab)
        # Insert value from saved data (should be defaulted to 0 if not present)
        entry.insert(0, str(saved_data["inventory"][item]))
        entry.grid(row=row_num, column=1, padx=10, pady=5)
        entry.bind("<Return>", focus_and_highlight)  # Bind Enter key to move focus and highlight text
        entry.bind("<FocusIn>", highlight_on_focus)  # Bind mouse click to highlight text

        # Bind an event to check the inventory value whenever it is updated
        entry.bind("<KeyRelease>", lambda event, e=entry: update_entry_background(e))
        update_entry_background(entry)  # Initial update to set correct background color

        inventory_entries[item] = entry

# Function to validate inventory data and save all data to a JSON file
def save_data():
    # Validate inventory data
    inventory_data = {}
    for item, entry in inventory_entries.items():
        try:
            cases = float(entry.get())
            if cases < 0:
                messagebox.showerror("Input Error", f"Number of cases for {item} must be a non-negative number.")
                return
            inventory_data[item] = cases
            # Track usage history if the inventory level has changed
            if item in saved_data["inventory"] and saved_data["inventory"][item] != cases:
                usage = saved_data["inventory"][item] - cases
                if usage > 0:
                    saved_data["usage_history"][item].append(usage)
        except ValueError:
            messagebox.showerror("Input Error", f"Please enter a valid number of cases for {item}.")
            return

    # Save validated data to the JSON file
    saved_data["inventory"] = inventory_data
    with open(data_file, "w") as file:
        json.dump(saved_data, file)

    messagebox.showinfo("Save Successful", "Data saved successfully!")

# Button to save all data with validation
save_all_button = tk.Button(root, text="Save All Data", command=save_data)
save_all_button.pack(pady=10)

# Function to calculate restocking needs
def calculate_restock():
    restock_message = ""
    days_until_next = days_until_next_shipment()

    for item in inventory_entries:
        current_inventory = float(inventory_entries[item].get())

        # Calculate average usage from usage history
        usage_history = saved_data["usage_history"].get(item, [])
        if usage_history:
            average_usage = sum(usage_history) / len(usage_history)
        else:
            average_usage = 1 # Default average usage if no history is available

        # Calculate adaptive restocking threshold
        adaptive_threshold = average_usage * days_until_next

        # If inventory is below the adaptive threshold, recommend restocking
        if current_inventory < adaptive_threshold:
            restock_needed = adaptive_threshold - current_inventory
            restock_message += f"{item}: Restock needed - {restock_needed:.2f} units (Threshold: {adaptive_threshold:.2f})\n"

    if restock_message:
        messagebox.showinfo("Restocking Recommendations", restock_message)
    else:
        messagebox.showinfo("Restocking Recommendations", "All items are above the threshold.")

# Button to calculate restocking needs
calculate_restock_button = tk.Button(root, text="Calculate Restocking", command=calculate_restock)
calculate_restock_button.pack(pady=10)

# Function to import inventory data from a CSV file
def import_data():
    # Open a file dialog to select the CSV file
    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return # User canceled the file dialog
    
    try:
        with open(file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            if 'Item' not in reader.fieldnames or 'Cases' not in reader.fieldnames:
                messagebox.showerror("Import Error", "CSV file must contain 'Item' and 'Cases' columns.")
                return
            
            for row in reader:
                item = row['Item']
                try:
                    cases = float(row['Cases'])
                    if cases < 0:
                        raise ValueError("Cases must be a non-negative number.")
                
                # Update the inventory data if the item exists
                    if item in saved_data["inventory"]:
                        saved_data["inventory"][item] = cases
                        # Update the UI if the item exists in the entries
                        if item in inventory_entries:
                            inventory_entries[item].delete(0, tk.END)
                            inventory_entries[item].insert(0, str(cases))
                            update_entry_background(inventory_entries[item])

                except ValueError:
                    messagebox.showerror("Import Error", f"Invalid number of cases for item '{item}'.")
                    return
    
        save_data()

        messagebox.showinfo("Import Successful", "Inventory data imported successfully.")

    except Exception as e:
        messagebox.showerror("Import Error", f"An error occured while importing: {e}")

# Button to import data from a CSV file
import_button = tk.Button(root, text="Import Inventory Data", command=import_data)
import_button.pack(pady=10)

root.mainloop()
