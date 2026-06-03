import customtkinter as ctk

from tkinter import ttk

from app.services import inventory_service

from app.utils.message_service import (

    show_info,
    show_warning,
    show_error,
    ask_yes_no

)

# =========================================
# INVENTORY PAGE
# =========================================
class InventoryPage(ctk.CTkFrame):

    LOW_STOCK_THRESHOLD = 5

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#1e1e1e"
        )

        self.setup_ui()

        self.refresh_page()

    # =====================================================
    # UI SETUP
    # =====================================================

    def setup_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Inventory Management",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(
            pady=(25, 20)
        )

        dashboard_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        dashboard_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.total_products_label = self.create_card(
            dashboard_frame,
            "Total Products",
            "0"
        )

        self.total_quantity_label = self.create_card(
            dashboard_frame,
            "Total Quantity",
            "0"
        )

        self.total_value_label = self.create_card(
            dashboard_frame,
            "Inventory Value",
            "0.00"
        )

        self.low_stock_label = self.create_card(
            dashboard_frame,
            "Low Stock",
            "0"
        )

        # =================================================
        # FORM
        # =================================================

        form_frame = ctk.CTkFrame(
            self,
            fg_color="#2a2a2a"
        )

        form_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # =================================================
        # ITEM NAME
        # =================================================

        self.name_input = ctk.CTkEntry(
            form_frame,
            placeholder_text="Item Name",
            width=250,
            height=40
        )

        self.name_input.grid(
            row=0,
            column=0,
            padx=10,
            pady=15
        )

        # =================================================
        # CATEGORY
        # =================================================

        self.category_combo = ctk.CTkComboBox(

            form_frame,

            values=[

                "Materials",
                "Services",
                "Equipment",
                "Labor",
                "Consumables",
                "Office Supplies",
                "Rental Assets"

            ],

            width=180,
            height=40

        )

        self.category_combo.grid(
            row=0,
            column=1,
            padx=10,
            pady=15
        )

        self.category_combo.set(
            "Materials"
        )

        # =================================================
        # QUANTITY
        # =================================================

        self.qty_input = ctk.CTkEntry(
            form_frame,
            placeholder_text="Quantity",
            width=140,
            height=40
        )

        self.qty_input.grid(
            row=0,
            column=2,
            padx=10,
            pady=15
        )

        # =================================================
        # PRICE
        # =================================================

        self.price_input = ctk.CTkEntry(
            form_frame,
            placeholder_text="Price",
            width=140,
            height=40
        )

        self.price_input.grid(
            row=0,
            column=3,
            padx=10,
            pady=15
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        buttons = [

            ("Add Item", self.add_item),
            ("Update Item", self.update_item),
            ("Delete Item", self.delete_item),
            ("Refresh", self.refresh_page)

        ]

        for text, command in buttons:

            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                height=40,
                corner_radius=10,
                font=("Segoe UI", 14, "bold")
            )

            btn.pack(
                side="left",
                padx=8
            )

        # =================================================
        # SEARCH
        # =================================================

        self.search_input = ctk.CTkEntry(
            self,
            placeholder_text="Search inventory...",
            height=40
        )

        self.search_input.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        self.search_input.bind(
            "<KeyRelease>",
            lambda e: self.search_inventory()
        )

        # =================================================
        # TABLE FRAME
        # =================================================

        table_frame = ctk.CTkFrame(
            self,
            fg_color="#2a2a2a"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # =================================================
        # TABLE STYLE
        # =================================================

        style = ttk.Style()

        style.theme_use("default")

        style.configure(

            "Treeview",

            background="#2b2b2b",

            foreground="white",

            rowheight=35,

            fieldbackground="#2b2b2b",

            bordercolor="#2b2b2b",

            borderwidth=0,

            font=("Segoe UI", 11)

        )

        style.map(
            "Treeview",
            background=[("selected", "#1f6feb")]
        )

        style.configure(

            "Treeview.Heading",

            background="#1f1f1f",

            foreground="white",

            relief="flat",

            font=("Segoe UI", 12, "bold")

        )

        style.map(
            "Treeview.Heading",
            background=[("active", "#333333")]
        )

        # =================================================
        # TABLE
        # =================================================

        columns = (
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price"
        )

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=20
        )

        for column in columns:

            self.table.heading(
                column,
                text=column
            )

            self.table.column(
                column,
                anchor="center",
                width=180
            )

        self.table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.table.bind(
            "<<TreeviewSelect>>",
            self.load_selected_item
        )

    # =====================================================
    # CREATE CARD
    # =====================================================

    def create_card(self, parent, title, value):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=120,
            fg_color="#2a2a2a"
        )

        card.pack(
            side="left",
            padx=10,
            fill="both",
            expand=True
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI", 16, "bold")
        )

        title_label.pack(
            pady=(20, 10)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI", 24, "bold"),
            text_color="#4CAF50"
        )

        value_label.pack()

        return value_label

    # =====================================================
    # REFRESH PAGE
    # =====================================================

    def refresh_page(self):

        self.load_inventory()

        self.update_dashboard()

    # =====================================================
    # LOAD INVENTORY
    # =====================================================

    def load_inventory(self):

        for row in self.table.get_children():

            self.table.delete(row)

        items = inventory_service.get_all_items()

        try:

            currency = inventory_service.get_currency()

        except:

            currency = "USD"

        symbol = f"{currency} "

        for item in items:

            item_id = item[0]

            name = item[1]

            category = item[2]

            quantity = item[3]

            price = float(item[4])

            formatted_price = (
                f"{symbol}{price:,.2f}"
            )

            self.table.insert(

                "",
                "end",

                values=(

                    item_id,
                    name,
                    category,
                    quantity,
                    formatted_price

                )

            )

    # =====================================================
    # UPDATE DASHBOARD
    # =====================================================

    def update_dashboard(self):

        items = inventory_service.get_all_items()

        total_products = len(items)

        total_quantity = 0

        total_value = 0

        low_stock = 0

        for item in items:

            quantity = int(item[3])

            price = float(item[4])

            total_quantity += quantity

            total_value += quantity * price

            if quantity <= self.LOW_STOCK_THRESHOLD:

                low_stock += 1

        self.total_products_label.configure(
            text=str(total_products)
        )

        self.total_quantity_label.configure(
            text=str(total_quantity)
        )

        try:

            currency = inventory_service.get_currency()

        except:

            currency = "USD"

        symbol = f"{currency} "

        self.total_value_label.configure(
            text=f"{symbol}{total_value:,.2f}"
        )

        self.low_stock_label.configure(
            text=str(low_stock)
        )

    # =====================================================
    # SEARCH
    # =====================================================

    def search_inventory(self):

        keyword = self.search_input.get()

        items = inventory_service.search_items(
            keyword
        )

        for row in self.table.get_children():

            self.table.delete(row)

        try:

            currency = inventory_service.get_currency()

        except:

            currency = "USD"

        symbol = f"{currency} "

        for item in items:

            item_id = item[0]

            name = item[1]

            category = item[2]

            quantity = item[3]

            price = float(item[4])

            formatted_price = (
                f"{symbol}{price:,.2f}"
            )

            self.table.insert(

                "",
                "end",

                values=(

                    item_id,
                    name,
                    category,
                    quantity,
                    formatted_price

                )

            )

    # =====================================================
    # LOAD SELECTED ITEM
    # =====================================================

    def load_selected_item(self, event):

        selected = self.table.selection()

        if not selected:
            return

        values = self.table.item(
            selected[0],
            "values"
        )

        self.name_input.delete(0, "end")
        self.name_input.insert(0, values[1])

        self.category_combo.set(values[2])

        self.qty_input.delete(0, "end")
        self.qty_input.insert(0, values[3])

        self.price_input.delete(0, "end")

        clean_price = str(values[4])

        try:

            currency = inventory_service.get_currency()

        except:

            currency = "USD"

        symbol = f"{currency} "

        clean_price = clean_price.replace(
            symbol,
            ""
        ).replace(",", "")

        self.price_input.insert(
            0,
            clean_price
        )

    # =====================================================
    # ADD ITEM
    # =====================================================

    def add_item(self):

        try:

            name = self.name_input.get().strip()

            category = self.category_combo.get()

            quantity_text = (
                self.qty_input.get().strip()
            )

            price_text = (
                self.price_input.get().strip()
            )

            if not name:

                show_error(
                    "Error",
                    "Item name is required."
                )

                return

            if not quantity_text:

                show_error(
                    "Error",
                    "Quantity is required."
                )

                return

            if not price_text:

                show_error(
                    "Error",
                    "Price is required."
                )

                return

            try:

                quantity = int(quantity_text)

            except:

                show_error(
                    "Error",
                    "Quantity must be a whole number."
                )

                return

            try:

                price = float(price_text)

            except:

                show_error(
                    "Error",
                    "Price must be numeric."
                )

                return

            if quantity < 0:

                show_error(
                    "Error",
                    "Quantity cannot be negative."
                )

                return

            if price < 0:

                show_error(
                    "Error",
                    "Price cannot be negative."
                )

                return

            inventory_service.add_item(
                name,
                category,
                quantity,
                price
            )

            show_info(
                "Success",
                "Inventory item added successfully."
            )

            self.refresh_page()

            self.clear_inputs()

        except Exception as e:

            show_error(
                "Error",
                str(e)
            )

    # =====================================================
    # UPDATE ITEM
    # =====================================================

    def update_item(self):

        try:

            selected = self.table.selection()

            if not selected:

                show_warning(
                    "Warning",
                    "Please select an item."
                )

                return

            values = self.table.item(
                selected[0],
                "values"
            )

            item_id = int(values[0])

            name = self.name_input.get().strip()

            category = self.category_combo.get()

            quantity_text = (
                self.qty_input.get().strip()
            )

            price_text = (
                self.price_input.get().strip()
            )

            if not name:

                show_error(
                    "Error",
                    "Item name is required."
                )

                return

            if not quantity_text:

                show_error(
                    "Error",
                    "Quantity is required."
                )

                return

            if not price_text:

                show_error(
                    "Error",
                    "Price is required."
                )

                return

            try:

                quantity = int(quantity_text)

            except:

                show_error(
                    "Error",
                    "Quantity must be a whole number."
                )

                return

            try:

                price = float(price_text)

            except:

                show_error(
                    "Error",
                    "Price must be numeric."
                )

                return

            if quantity < 0:

                show_error(
                    "Error",
                    "Quantity cannot be negative."
                )

                return

            if price < 0:

                show_error(
                    "Error",
                    "Price cannot be negative."
                )

                return

            inventory_service.update_item(
                item_id,
                name,
                category,
                quantity,
                price
            )

            show_info(
                "Success",
                "Inventory item updated successfully."
            )

            self.refresh_page()

            self.clear_inputs()

        except Exception as e:

            show_error(
                "Error",
                str(e)
            )

    # =====================================================
    # DELETE ITEM
    # =====================================================

    def delete_item(self):

        try:

            selected = self.table.selection()

            if not selected:

                show_warning(
                    "Warning",
                    "Please select an item."
                )

                return

            values = self.table.item(
                selected[0],
                "values"
            )

            item_id = int(values[0])

            confirm = ask_yes_no(
                "Confirm Delete",
                "Delete selected inventory item?"
            )

            if not confirm:

                return

            inventory_service.delete_item(
                item_id
            )

            show_info(
                "Success",
                "Inventory item deleted successfully."
            )

            self.refresh_page()

            self.clear_inputs()

        except Exception as e:

            show_error(
                "Error",
                str(e)
            )

    # =====================================================
    # CLEAR INPUTS
    # =====================================================

    def clear_inputs(self):

        self.name_input.delete(0, "end")

        self.qty_input.delete(0, "end")

        self.price_input.delete(0, "end")

        self.category_combo.set(
            "Materials"
        )