import tkinter as tk
from tkinter import ttk

root = tk.Tk()
tree = ttk.Treeview(root, columns=("Column 1", "Column 2", "Column 3"))
tree.heading("#0", text="Item")
tree.heading("Column 1", text="Column 1")
tree.heading("Column 2", text="Column 2")
tree.heading("Column 3", text="Column 3")
tree.column("#0", width=100, anchor="center")
tree.column("Column 1", width=100, anchor="center")
tree.column("Column 2", width=100, anchor="center")
tree.column("Column 3", width=100, anchor="center")

tree.insert("", "end", text="Row 1", values=("Data 1", "Data 2", "Data 3"))

tree.pack()
root.mainloop()