import tkinter as tk
from tkinter import ttk
import csv

class PaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("支付系统")
        
        # 商品数据
        self.products = []
        try:
            with open('./config.csv', 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.products.append({"name": row["name"], "price": int(row["price"]), "discountable": row.get("discountable", "true").lower() == "true"})
        except Exception as e:
            print(f"读取商品数据失败: {e}")
        
        # 优惠选项
        self.discounts = [
            {"name": "无优惠", "value": 0},
            {"name": "9折", "value": 0.1},
            {"name": "8折", "value": 0.2},
            {"name": "7折", "value": 0.3},
            {"name": "6折", "value": 0.4},
            {"name": "5折", "value": 0.5},
            {"name": "4折", "value": 0.6},
            {"name": "3折", "value": 0.7},
            {"name": "2折", "value": 0.8},
            {"name": "1折", "value": 0.9},
            {"name": "免费", "value": 1}
        ]
        
        # 购物车
        self.cart = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # 商品选择
        ttk.Label(self.root, text="选择商品:").grid(row=0, column=0, padx=5, pady=5)
        self.product_var = tk.StringVar()
        self.product_combobox = ttk.Combobox(self.root, textvariable=self.product_var, 
                                           values=[p["name"] for p in self.products])
        self.product_combobox.grid(row=0, column=1, padx=5, pady=5)
        
        # 数量输入
        ttk.Label(self.root, text="数量:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_var = tk.IntVar(value=1)
        ttk.Entry(self.root, textvariable=self.quantity_var).grid(row=1, column=1, padx=5, pady=5)
        
        # 添加按钮
        ttk.Button(self.root, text="添加到购物车", command=self.add_to_cart).grid(row=2, column=0, columnspan=2, pady=10)
        
        # 优惠选择
        ttk.Label(self.root, text="选择优惠:").grid(row=3, column=0, padx=5, pady=5)
        self.discount_var = tk.StringVar()
        self.discount_combobox = ttk.Combobox(self.root, textvariable=self.discount_var, 
                                            values=[d["name"] for d in self.discounts])
        self.discount_combobox.current(0)
        self.discount_combobox.grid(row=3, column=1, padx=5, pady=5)
        
        # 购物车列表
        self.cart_listbox = tk.Listbox(self.root, height=5)
        self.cart_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # 总价显示
        ttk.Label(self.root, text="总价:").grid(row=5, column=0, padx=5, pady=5)
        self.total_var = tk.StringVar(value="0.00")
        ttk.Label(self.root, textvariable=self.total_var).grid(row=5, column=1, padx=5, pady=5)
        
        # 计算按钮
        ttk.Button(self.root, text="计算总价", command=self.calculate_total).grid(row=6, column=0, columnspan=2, pady=10)
        
        # 删除按钮
        ttk.Button(self.root, text="删除选中商品", command=self.remove_from_cart).grid(row=7, column=0, columnspan=2, pady=10)
    
    def add_to_cart(self):
        product_name = self.product_var.get()
        quantity = self.quantity_var.get()
        
        if not product_name or quantity <= 0:
            return
            
        product = next((p for p in self.products if p["name"] == product_name), None)
        if product:
            self.cart.append({"product": product, "quantity": quantity})
            self.update_cart_display()
    
    def update_cart_display(self):
        self.cart_listbox.delete(0, tk.END)
        discount_name = self.discount_var.get()
        discount = next((d for d in self.discounts if d["name"] == discount_name), None)
        
        for item in self.cart:
            original_price = item['product']['price'] * item['quantity']
            if discount and item['product']['discountable'] is True:
                discounted_price = original_price * (1 - discount["value"])
                self.cart_listbox.insert(tk.END, 
                                       f"{item['product']['name']}  x{item['quantity']}  {original_price} (折后: {discounted_price:.2f})")
            else:
                self.cart_listbox.insert(tk.END, 
                                       f"{item['product']['name']}  x{item['quantity']}  {original_price}")
    
    def calculate_total(self):
        discount_name = self.discount_var.get()
        discount = next((d for d in self.discounts if d["name"] == discount_name), None)
        
        total = sum(item["product"]["price"] * item["quantity"] for item in self.cart)
        if discount:
            total *= (1 - discount["value"])
            
        self.total_var.set(f"{total:.2f}")
        
    def remove_from_cart(self):
        selected_index = self.cart_listbox.curselection()
        if selected_index:
            self.cart.pop(selected_index[0])
            self.update_cart_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PaymentApp(root)
    root.mainloop()