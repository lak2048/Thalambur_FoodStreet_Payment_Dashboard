import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

DATA_FILE = "shops_data.csv"

class Shop:
    def __init__(self, shop_num, shop_name, owner="", address="", advance="", base_rent="",
                 rent_amt="0", rent_status="Pending", genset_amt="0", genset_status="Pending",
                 eb_amt="0", eb_status="Pending", room_rent_amt="0", room_rent_status="NA"):
        self.shop_num = shop_num
        self.shop_name = shop_name
        self.owner = owner
        self.address = address
        self.advance = advance
        self.base_rent = base_rent
        self.rent_amt = rent_amt
        self.rent_status = rent_status
        self.genset_amt = genset_amt
        self.genset_status = genset_status
        self.eb_amt = eb_amt
        self.eb_status = eb_status
        self.room_rent_amt = room_rent_amt
        self.room_rent_status = room_rent_status

class MultiShopManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Thalambur Food Street Manager (Data saved to CSV)")
        self.root.geometry("1100x700")
        
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("PaidRow.TLabel", background="lightgreen", foreground="black", padding=5)
        style.configure("PendingRow.TLabel", background="#FFC0CB", foreground="black", padding=5)
        style.configure("Header.TLabel", background="#333", foreground="white", font=("Arial", 10, "bold"), anchor="center", padding=5)
        
        self.shops = {} 
        self.load_data_from_csv()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        self.create_management_tab()
        self.create_dashboard_tab()

        self.populate_shop_list()
        self.populate_payment_dashboard()

    def get_csv_fieldnames(self):
        return [
            'shop_num', 'shop_name', 'owner', 'address', 'advance', 'base_rent',
            'rent_amt', 'rent_status', 'genset_amt', 'genset_status', 'eb_amt', 'eb_status',
            'room_rent_amt', 'room_rent_status'
        ]

    def load_data_from_csv(self):
        if not os.path.exists(DATA_FILE):
            self.add_sample_data()
            self.save_data_to_csv()
            return
        
        try:
            with open(DATA_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    shop_data = {
                        'shop_num': row.get('shop_num'), 'shop_name': row.get('shop_name'), 'owner': row.get('owner'), 
                        'address': row.get('address'), 'advance': row.get('advance'), 'base_rent': row.get('base_rent'),
                        'rent_amt': row.get('rent_amt', '0'), 'rent_status': row.get('rent_status', 'Pending'),
                        'genset_amt': row.get('genset_amt', '0'), 'genset_status': row.get('genset_status', 'Pending'),
                        'eb_amt': row.get('eb_amt', '0'), 'eb_status': row.get('eb_status', 'Pending'),
                        'room_rent_amt': row.get('room_rent_amt', '0'), 'room_rent_status': row.get('room_rent_status', 'NA')
                    }
                    shop = Shop(**shop_data)
                    self.shops[shop.shop_num] = shop
        except Exception as e:
            messagebox.showerror("Error Loading Data", f"Could not load data from {DATA_FILE}.\nError: {e}")
            self.add_sample_data()

    def save_data_to_csv(self):
        try:
            with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.get_csv_fieldnames())
                writer.writeheader()
                for shop in self.shops.values():
                    writer.writerow(shop.__dict__)
        except Exception as e:
            messagebox.showerror("Error Saving Data", f"Could not save data to {DATA_FILE}.\nError: {e}")

    def add_sample_data(self):
        shop1 = Shop("Shop 1", "Frozen Cups", "Mr. Arun", "123 Anna Salai", "2L", "23k", "23000", "Paid", "1480", "Paid", "0", "NA", "5000", "Paid")
        shop2 = Shop("Shop 2", "Yum Sandwich", "Ms. Priya", "456 OMR", "1.5L", "18k", "18000", "Paid", "930", "Pending", "450", "Paid", "0", "NA")
        shop3 = Shop("Shop 3", "Irani Chai", "Mr. Kumar", "789 ECR", "1.75L", "21k", "21000", "Pending", "1480", "Pending", "550", "Paid", "4500", "Pending")
        self.shops = {shop.shop_num: shop for shop in [shop1, shop2, shop3]}
    
    # --- Management Tab and its helpers (No changes in this section) ---
    def create_management_tab(self):
        management_frame = ttk.Frame(self.notebook, padding="10"); self.notebook.add(management_frame, text="Shop Management")
        paned_window = ttk.PanedWindow(management_frame, orient=tk.HORIZONTAL); paned_window.pack(fill=tk.BOTH, expand=True)
        list_frame = ttk.Frame(paned_window, width=350)
        ttk.Label(list_frame, text="All Shops", font=("Arial", 14, "bold")).pack(pady=5)
        tree_frame = ttk.Frame(list_frame); tree_frame.pack(fill=tk.BOTH, expand=True)
        columns = ("shop_num", "shop_name"); self.shop_list_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
        self.shop_list_tree.heading("shop_num", text="Shop Num"); self.shop_list_tree.heading("shop_name", text="Shop Name")
        self.shop_list_tree.column("shop_num", width=100); self.shop_list_tree.column("shop_name", width=200)
        self.shop_list_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); self.shop_list_tree.bind("<<TreeviewSelect>>", self.on_shop_select)
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.shop_list_tree.yview); scrollbar.pack(side=tk.RIGHT, fill="y")
        self.shop_list_tree.configure(yscrollcommand=scrollbar.set)
        button_frame = ttk.Frame(list_frame); button_frame.pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="Add New Shop", command=self.open_add_shop_window).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_shop).pack(side=tk.LEFT, expand=True, padx=5)
        paned_window.add(list_frame, weight=1)
        details_forms_frame = ttk.Frame(paned_window); self.create_details_forms(details_forms_frame); paned_window.add(details_forms_frame, weight=2)
    def create_details_forms(self, parent_frame):
        details_lf = ttk.LabelFrame(parent_frame, text="Basic Details", padding="15"); details_lf.pack(fill=tk.X, padx=10, pady=(0, 10))
        details_lf.columnconfigure(1, weight=1); self.detail_entries = {}
        fields = ["Shop Number:", "Shop Name:", "Shop Owner:", "Owner Address:", "Advance Paid Details:", "Base Rent + Maintenance:"]
        for i, label_text in enumerate(fields):
            ttk.Label(details_lf, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = tk.Text(details_lf, height=3, width=50) if "Address" in label_text else ttk.Entry(details_lf, width=60)
            entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5); self.detail_entries[label_text] = entry
        payments_lf = ttk.LabelFrame(parent_frame, text="Monthly Payment Details", padding="15"); payments_lf.pack(fill=tk.X, padx=10, pady=10)
        payments_lf.columnconfigure(1, weight=1); self.payment_entries = {}
        payment_fields = ["Rent", "Room Rent", "Genset", "EB"]
        for i, p_type in enumerate(payment_fields):
            ttk.Label(payments_lf, text=f"{p_type} Amount:").grid(row=i, column=0, sticky="w", padx=5, pady=5)
            amt_entry = ttk.Entry(payments_lf); amt_entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            ttk.Label(payments_lf, text="Status:").grid(row=i, column=2, sticky="w", padx=10, pady=5)
            if p_type in ["EB", "Room Rent", "Genset"]: combo_values = ["Paid", "Pending", "NA"]
            else: combo_values = ["Paid", "Pending"]
            status_combo = ttk.Combobox(payments_lf, values=combo_values, state="readonly"); status_combo.grid(row=i, column=3, padx=5, pady=5, sticky="ew")
            self.payment_entries[p_type] = (amt_entry, status_combo)
        ttk.Button(parent_frame, text="Save All Details", command=self.save_all_details).pack(side=tk.RIGHT, padx=10, pady=20)
    def open_add_shop_window(self):
        add_window = tk.Toplevel(self.root); add_window.title("Add New Shop"); add_window.transient(self.root)
        lf = ttk.LabelFrame(add_window, text="Enter New Shop Details", padding="15"); lf.pack(padx=15, pady=15, fill="both", expand=True)
        lf.columnconfigure(1, weight=1); new_shop_entries = {}
        fields = ["Shop Number:", "Shop Name:", "Shop Owner:", "Owner Address:", "Advance Paid Details:", "Base Rent + Maintenance:"]
        for i, label_text in enumerate(fields):
            ttk.Label(lf, text=label_text).grid(row=i, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(lf, width=40); entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5); new_shop_entries[label_text] = entry
        ttk.Button(lf, text="Save New Shop", command=lambda: self.save_new_shop(add_window, new_shop_entries)).grid(row=len(fields), columnspan=2, pady=15)
        new_shop_entries["Shop Number:"].focus_set()
    def on_shop_select(self, event):
        selected_items = self.shop_list_tree.selection()
        if not selected_items: self.clear_all_forms(); return
        shop = self.shops.get(selected_items[0])
        if shop:
            self.clear_all_forms(); self.detail_entries["Shop Number:"].config(state='normal')
            self.detail_entries["Shop Number:"].insert(0, shop.shop_num); self.detail_entries["Shop Number:"].config(state='readonly')
            self.detail_entries["Shop Name:"].insert(0, shop.shop_name); self.detail_entries["Shop Owner:"].insert(0, shop.owner)
            self.detail_entries["Owner Address:"].insert("1.0", shop.address); self.detail_entries["Advance Paid Details:"].insert(0, shop.advance)
            self.detail_entries["Base Rent + Maintenance:"].insert(0, shop.base_rent)
            self.payment_entries["Rent"][0].insert(0, shop.rent_amt); self.payment_entries["Rent"][1].set(shop.rent_status)
            self.payment_entries["Room Rent"][0].insert(0, shop.room_rent_amt); self.payment_entries["Room Rent"][1].set(shop.room_rent_status)
            self.payment_entries["Genset"][0].insert(0, shop.genset_amt); self.payment_entries["Genset"][1].set(shop.genset_status)
            self.payment_entries["EB"][0].insert(0, shop.eb_amt); self.payment_entries["EB"][1].set(shop.eb_status)
    def save_all_details(self):
        shop_num = self.detail_entries["Shop Number:"].get()
        if not shop_num: messagebox.showwarning("No Selection", "Please select a shop to save."); return
        shop = self.shops.get(shop_num)
        if shop:
            shop.shop_name = self.detail_entries["Shop Name:"].get(); shop.owner = self.detail_entries["Shop Owner:"].get()
            shop.address = self.detail_entries["Owner Address:"].get("1.0", tk.END).strip(); shop.advance = self.detail_entries["Advance Paid Details:"].get()
            shop.base_rent = self.detail_entries["Base Rent + Maintenance:"].get()
            shop.rent_amt, shop.rent_status = self.payment_entries["Rent"][0].get(), self.payment_entries["Rent"][1].get()
            shop.room_rent_amt, shop.room_rent_status = self.payment_entries["Room Rent"][0].get(), self.payment_entries["Room Rent"][1].get()
            shop.genset_amt, shop.genset_status = self.payment_entries["Genset"][0].get(), self.payment_entries["Genset"][1].get()
            shop.eb_amt, shop.eb_status = self.payment_entries["EB"][0].get(), self.payment_entries["EB"][1].get()
            self.save_data_to_csv(); self.refresh_all_data(); self.shop_list_tree.selection_set(shop.shop_num)
            messagebox.showinfo("Success", f"All details for {shop.shop_name} have been updated and saved.")
    def save_new_shop(self, window, entries):
        shop_num = entries["Shop Number:"].get(); shop_name = entries["Shop Name:"].get()
        if not shop_num or not shop_name: messagebox.showerror("Error", "Shop Number and Shop Name are required.", parent=window); return
        if shop_num in self.shops: messagebox.showerror("Error", f"Shop Number '{shop_num}' already exists.", parent=window); return
        new_shop = Shop(shop_num, shop_name, owner=entries["Shop Owner:"].get(), address=entries["Owner Address:"].get(), advance=entries["Advance Paid Details:"].get(), base_rent=entries["Base Rent + Maintenance:"].get())
        self.shops[shop_num] = new_shop
        self.save_data_to_csv(); self.refresh_all_data(); window.destroy()
        messagebox.showinfo("Success", f"Shop '{shop_name}' has been added and saved.")
    def delete_selected_shop(self):
        selected_items = self.shop_list_tree.selection()
        if not selected_items: messagebox.showwarning("No Selection", "Please select a shop to delete."); return
        shop_num = selected_items[0]; shop_name = self.shops[shop_num].shop_name
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{shop_name}'?"):
            del self.shops[shop_num]; self.save_data_to_csv(); self.refresh_all_data(); self.clear_all_forms()
            messagebox.showinfo("Deleted", f"Shop '{shop_name}' has been deleted and data saved.")
    def clear_all_forms(self):
        self.detail_entries["Shop Number:"].config(state='normal')
        for widget in self.detail_entries.values():
            if isinstance(widget, tk.Text): widget.delete("1.0", tk.END)
            else: widget.delete(0, tk.END)
        for amt_entry, status_combo in self.payment_entries.values():
            amt_entry.delete(0, tk.END); status_combo.set('')
    def populate_shop_list(self):
        for item in self.shop_list_tree.get_children(): self.shop_list_tree.delete(item)
        for shop_num, shop in self.shops.items(): self.shop_list_tree.insert("", tk.END, values=(shop.shop_num, shop.shop_name), iid=shop_num)
    
    # --- Dashboard Tab - THIS SECTION IS CORRECTED ---
    def create_dashboard_tab(self):
        dashboard_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(dashboard_frame, text="Payment Status Dashboard")
        
        controls_frame = ttk.Frame(dashboard_frame)
        controls_frame.pack(fill=tk.X, pady=5)
        ttk.Button(controls_frame, text="Refresh / Show All", command=self.populate_payment_dashboard).pack(side=tk.LEFT, padx=5)
        ttk.Button(controls_frame, text="Show Pending Only", command=lambda: self.populate_payment_dashboard(filter_pending=True)).pack(side=tk.LEFT, padx=5)
        
        # This outer frame ensures the canvas and scrollbar are contained properly
        container = ttk.Frame(dashboard_frame)
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.dashboard_grid_frame = ttk.Frame(canvas) # The grid is inside the canvas

        # This ensures the scroll region is updated when the grid size changes
        self.dashboard_grid_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas_frame_id = canvas.create_window((0, 0), window=self.dashboard_grid_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # This is the crucial part: when the canvas resizes, update the width of the frame inside it.
        def on_canvas_resize(event):
            canvas.itemconfig(canvas_frame_id, width=event.width)
        
        canvas.bind("<Configure>", on_canvas_resize)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def populate_payment_dashboard(self, filter_pending=False):
        for widget in self.dashboard_grid_frame.winfo_children():
            widget.destroy()
            
        headers = ["Shop Name", "Shop Num", "Rent Amt", "Status", "Room Rent", "Status", "Genset Amt", "Status", "EB Amt", "Status"]
        for i, header in enumerate(headers):
            # This makes each column expand equally
            self.dashboard_grid_frame.columnconfigure(i, weight=1)
            ttk.Label(self.dashboard_grid_frame, text=header, style="Header.TLabel").grid(row=0, column=i, sticky="nsew")
        
        row_num = 1
        sorted_shops = sorted(self.shops.values(), key=lambda s: int(''.join(filter(str.isdigit, s.shop_num)) or 0))

        for shop in sorted_shops:
            is_any_pending = (shop.rent_status == "Pending" or shop.genset_status == "Pending" or 
                              shop.eb_status == "Pending" or shop.room_rent_status == "Pending")
            
            if filter_pending and not is_any_pending:
                continue
                
            row_style = "PendingRow.TLabel" if is_any_pending else "PaidRow.TLabel"
            room_rent_amt_display = shop.room_rent_amt if shop.room_rent_amt and shop.room_rent_amt != '0' else '-'
            room_rent_status_display = shop.room_rent_status if room_rent_amt_display != '-' else '-'
            
            data = [
                shop.shop_name, shop.shop_num, shop.rent_amt, shop.rent_status,
                room_rent_amt_display, room_rent_status_display,
                shop.genset_amt, shop.genset_status, shop.eb_amt, shop.eb_status,
            ]
            
            for col_num, text in enumerate(data):
                anchor_pos = "w" if col_num == 0 else "center"
                ttk.Label(self.dashboard_grid_frame, text=text, style=row_style, anchor=anchor_pos).grid(row=row_num, column=col_num, sticky="nsew")
            
            row_num += 1

    def refresh_all_data(self):
        self.populate_shop_list()
        self.populate_payment_dashboard()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiShopManagerApp(root)
    root.mainloop()
