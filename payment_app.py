import tkinter as tk
from tkinter import ttk
import csv

class PaymentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("支付系统")
        self.root.configure(bg='#f0f0f0')
        style = ttk.Style()
        style.configure('TLabel', background='#f0f0f0', font=('Microsoft YaHei', 9))
        style.configure('TButton', font=('Microsoft YaHei', 9), padding=5)
        style.configure('TCombobox', font=('Microsoft YaHei', 9))
        style.configure('TEntry', font=('Microsoft YaHei', 9))
        
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
        
        # 时间显示
        self.time_label = ttk.Label(self.root, text="", font=('Microsoft YaHei', 10))
        self.time_label.grid(row=8, column=1, sticky="se", padx=5, pady=5)
        self.update_time()
        
        # 添加边框和间距
        for child in self.root.winfo_children():
            child.grid_configure(padx=10, pady=5)
    
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
            
    def update_time(self):
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M')
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

class SplashScreen:
    def __init__(self, root):
        self.root = root
        self.root.overrideredirect(True)
        width = 400
        height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        self.root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
        self.label = tk.Label(root, text="支付程序", font=('Helvetica', 18))
        self.label.pack(expand=True)
        
        self.root.after(5000, self.destroy)
    
    def destroy(self):
        self.root.destroy()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("登录/注册")
        self.root.geometry("300x200")
        
        ttk.Label(root, text="用户名:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(root, text="密码:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.login_button = ttk.Button(root, text="登录", command=self.verify_login)
        self.login_button.grid(row=2, column=0, pady=10)
        
        self.register_button = ttk.Button(root, text="注册", command=self.register_user)
        self.register_button.grid(row=2, column=1, pady=10)
        
        self.status_label = ttk.Label(root, text="", foreground="red")
        self.status_label.grid(row=3, column=0, columnspan=2)
    
    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            with open('./data/UesrConfig.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        u, p = line.strip().split(',')
                        if username == u and password == p:
                            self.root.destroy()
                            return True
            self.status_label.config(text="用户名或密码错误")
            return False
        except Exception as e:
            self.status_label.config(text=f"登录失败: {str(e)}")
            return False
            
    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(text="用户名和密码不能为空")
            return
            
        try:
            # 检查是否有现有用户
            with open('./data/UesrConfig.txt', 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                
                # 如果有现有用户，则要求输入现有用户信息
                if lines:
                    existing_user = lines[0].split(',')[0]
                    if username != existing_user:
                        self.status_label.config(text=f"请输入现有用户 '{existing_user}' 进行验证", foreground="blue")
                        return
                    else:
                        self.status_label.config(text="验证通过，可以继续注册", foreground="green")
                        # 继续执行注册流程
                
                # 检查用户是否已存在
                for line in lines:
                    u, _ = line.split(',')
                    if username == u:
                        self.status_label.config(text="用户名已存在")
                        return
            
            # 添加新用户
            with open('./data/UesrConfig.txt', 'a') as f:
                f.write(f"\n{username},{password}")
                
            self.status_label.config(text="注册成功", foreground="green")
        except Exception as e:
            self.status_label.config(text=f"注册失败: {str(e)}", foreground="red")

if __name__ == "__main__":
    splash_root = tk.Tk()
    splash = SplashScreen(splash_root)
    splash_root.mainloop()
    
    login_root = tk.Tk()
    login = LoginWindow(login_root)
    login_root.mainloop()
    
    # 只有登录窗口正常关闭(即登录成功)才会打开主界面
    if not login_root.winfo_exists():
        root = tk.Tk()
        app = PaymentApp(root)
        root.mainloop()