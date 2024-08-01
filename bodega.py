import tkinter as tk
from tkinter import messagebox
import pickle
import os

DATA_FILE = 'sales_data.pkl'

class SalesApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Ventas')
        self.root.geometry('600x400')  
        self.root.configure(bg='#006F7A')
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
       
        tk.Label(self.root, text='Producto:', bg='lightgray').grid(row=0, column=0, padx=20, pady=10, sticky='e')
        self.product_entry = tk.Entry(self.root, width=30)
        self.product_entry.grid(row=0, column=1, padx=20, pady=10)

        tk.Label(self.root, text='Kilos Comprados:', bg='lightgray').grid(row=1, column=0, padx=20, pady=10, sticky='e')
        self.quantity_purchased_entry = tk.Entry(self.root, width=30)
        self.quantity_purchased_entry.grid(row=1, column=1, padx=20, pady=10)

        tk.Label(self.root, text='Kilos Vendidos:', bg='lightgray').grid(row=2, column=0, padx=20, pady=10, sticky='e')
        self.quantity_sold_entry = tk.Entry(self.root, width=30)
        self.quantity_sold_entry.grid(row=2, column=1, padx=20, pady=10)

      
        tk.Button(self.root, text='🛒 Registrar Compra', command=self.add_purchase, bg='lightblue', width=20).grid(row=3, column=0, padx=20, pady=10)
        tk.Button(self.root, text='💰 Registrar Venta', command=self.add_sale, bg='lightgreen', width=20).grid(row=3, column=1, padx=20, pady=10)
        tk.Button(self.root, text='Actualizar Inventario', command=self.update_inventory, bg='lightyellow', width=20).grid(row=4, column=0, columnspan=2, padx=20, pady=10)

   
        self.inventory_text = tk.Text(self.root, height=10, width=70, wrap='word', bg='white')
        self.inventory_text.grid(row=5, column=0, columnspan=2, padx=20, pady=10)
        self.inventory_text.configure(state='disabled')

    def add_purchase(self):
        product = self.product_entry.get().strip()
        if not product:
            messagebox.showwarning('Advertencia', 'El nombre del producto no puede estar vacío')
            return
        try:
            quantity = float(self.quantity_purchased_entry.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'Cantidad debe ser un número positivo')
            return
        if product in self.inventory:
            self.inventory[product]['purchased'] += quantity
        else:
            self.inventory[product] = {'purchased': quantity, 'sold': 0}
        self.save_data()
        self.update_inventory()
        messagebox.showinfo('Éxito', f'Compra de {quantity} kilos del producto "{product}" registrada.')

    def add_sale(self):
        product = self.product_entry.get().strip()
        if not product:
            messagebox.showwarning('Advertencia', 'El nombre del producto no puede estar vacío')
            return
        try:
            quantity = float(self.quantity_sold_entry.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror('Error', 'Cantidad debe ser un número positivo')
            return
        if product in self.inventory:
            available_stock = self.inventory[product]['purchased'] - self.inventory[product]['sold']
            if available_stock >= quantity:
                self.inventory[product]['sold'] += quantity
                self.save_data()
                self.update_inventory()
                messagebox.showinfo('Éxito', f'Venta de {quantity} kilos del producto "{product}" registrada.')
            else:
                messagebox.showerror('Error', 'No hay suficiente inventario para la venta')
        else:
            messagebox.showerror('Error', 'El producto no existe en el inventario')

    def update_inventory(self):
    
        self.inventory_text.configure(state='normal')
        self.inventory_text.delete(1.0, tk.END)  
        if not self.inventory:
            self.inventory_text.insert(tk.END, 'No hay productos en el inventario')
        else:
            inventory_str = '\n'.join(
                [f'{product}: Comprados {info["purchased"]} kg, Vendidos {info["sold"]} kg, Restantes {info["purchased"] - info["sold"]} kg'
                 for product, info in self.inventory.items()]
            )
            self.inventory_text.insert(tk.END, inventory_str)
        self.inventory_text.configure(state='disabled')

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as f:
                try:
                    self.inventory = pickle.load(f)
                except (pickle.PickleError, EOFError):
                    self.inventory = {}
        else:
            self.inventory = {}

    def save_data(self):
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(self.inventory, f)

if __name__ == '__main__':
    root = tk.Tk()
    app = SalesApp(root)
    root.mainloop()
