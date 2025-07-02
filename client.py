import tkinter as tk
from tkinter import messagebox, PhotoImage
import subprocess
import sys
import requests
import webbrowser
import os

# Auto-install 'requests' if missing
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
except ImportError:
    install("requests")
    import requests

# Your server URL
SERVER_URL = 'http://127.0.0.1:5000'  # Change to your actual server IP

class CheatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Cheat Login")
        self.root.geometry("800x500")
        self.root.configure(bg="#111")
        self.username_str = ""
        self.dropdown_visible = False
        self.login_page()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="Username", font=("Segoe UI", 14), bg="#111", fg="white").pack(pady=(60, 5))
        self.username = tk.Entry(self.root, font=("Segoe UI", 13))
        self.username.pack()
        tk.Label(self.root, text="Password", font=("Segoe UI", 14), bg="#111", fg="white").pack(pady=5)
        self.password = tk.Entry(self.root, show="*", font=("Segoe UI", 13))
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.login, font=("Segoe UI", 12), width=15, bg="#333", fg="white").pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register, font=("Segoe UI", 12), width=15, bg="#444", fg="white").pack()

    def register(self):
        data = self.send_request('/register', {
            'username': self.username.get(),
            'password': self.password.get()
        })
        messagebox.showinfo("Register", data.get('msg', 'Registered!' if data['success'] else 'Failed'))

    def login(self):
        data = self.send_request('/login', {
            'username': self.username.get(),
            'password': self.password.get()
        })
        if data['success']:
            self.username_str = self.username.get()
            self.cheat_menu()
        else:
            messagebox.showerror("Login Failed", data.get('msg', 'Unknown error'))

    def cheat_menu(self):
        self.clear()
        self.root.geometry("800x500")
        self.root.configure(bg="#111")

        # ☰ Dropdown Button
        self.dropdown_btn = tk.Button(self.root, text="☰", font=("Segoe UI", 14), command=self.toggle_dropdown, bg="#222", fg="white", bd=0, activebackground="#444")
        self.dropdown_btn.place(x=760, y=5, width=30, height=30)

        # Dropdown Frame (Initially Hidden)
        self.dropdown_frame = tk.Frame(self.root, bg="#222", highlightbackground="white", highlightthickness=1)
        tk.Label(self.dropdown_frame, text=self.username_str, bg="#222", fg="white", font=("Segoe UI", 10)).pack(pady=(5, 0), padx=10)
        tk.Button(self.dropdown_frame, text="X", command=self.root.quit, bg="#aa2222", fg="white", bd=0).pack(pady=5, padx=10, fill="x")

        # 🎮 Game Buttons (Horizontal Row)
        btn_names = [("CS2", "https://yourlink.com/cs2"),
                     ("Roblox", "https://yourlink.com/roblox"),
                     ("Skate 3", "https://yourlink.com/skate3")]

        x_start = 130
        spacing = 180
        for i, (name, link) in enumerate(btn_names):
            b = tk.Button(self.root, text=name, font=("Segoe UI", 16), width=12, height=2,
                          bg="#222", fg="white", bd=0,
                          activebackground="#444", activeforeground="white",
                          command=lambda url=link: self.open_link(url))
            b.place(x=x_start + i * spacing, y=200)
            self.animate_button(b)

        # 🌐 Bottom-right icon
        try:
            self.link_img = PhotoImage(file="link_icon.png")
            link_btn = tk.Button(self.root, image=self.link_img, command=lambda: self.open_link("https://yourlink.com/info"),
                                 bg="#111", bd=0, activebackground="#111", cursor="hand2")
            link_btn.place(x=770, y=460)
        except Exception as e:
            print("Missing link_icon.png or load failed")

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
        else:
            self.dropdown_frame.place(x=650, y=40, width=140)
        self.dropdown_visible = not self.dropdown_visible

    def animate_button(self, btn):
        def on_enter(e): btn.config(bg="#555")
        def on_leave(e): btn.config(bg="#222")
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def open_link(self, url):
        webbrowser.open(url)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def send_request(self, endpoint, data):
        try:
            r = requests.post(SERVER_URL + endpoint, json=data)
            return r.json()
        except Exception as e:
            return {'success': False, 'msg': str(e)}

# 🪄 Hide console window (optional)
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

root = tk.Tk()
app = CheatClient(root)
root.mainloop()
