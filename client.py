import tkinter as tk
from tkinter import messagebox
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

# 🚀 Server URL (your old PC server IP and port)
SERVER_URL = 'http://127.0.0.1:5000'  # Change this to your server's IP

class CheatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Cheat Login")
        self.root.geometry("600x400")
        self.username_str = ""
        self.login_page()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="Username", font=("Segoe UI", 12)).pack(pady=(40, 5))
        self.username = tk.Entry(self.root, font=("Segoe UI", 12))
        self.username.pack()
        tk.Label(self.root, text="Password", font=("Segoe UI", 12)).pack(pady=5)
        self.password = tk.Entry(self.root, show="*", font=("Segoe UI", 12))
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.login, font=("Segoe UI", 12), width=15).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register, font=("Segoe UI", 12), width=15).pack()

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
        self.root.geometry("600x400")

        # 🌐 Top-right dropdown menu
        dropdown_frame = tk.Frame(self.root, bg="lightgray", relief=tk.RAISED, bd=1)
        dropdown_btn = tk.Button(self.root, text="☰", font=("Segoe UI", 14), command=lambda: self.toggle_dropdown(dropdown_frame))
        dropdown_btn.place(x=560, y=5, width=30, height=30)
        self.dropdown_frame = dropdown_frame

        tk.Label(dropdown_frame, text=self.username_str, bg="lightgray", font=("Segoe UI", 10)).pack(pady=2, padx=5)
        tk.Button(dropdown_frame, text="X", bg="red", fg="white", command=self.root.quit).pack(pady=2, padx=5)

        # 🎮 Big center buttons
        btn_config = {
            "font": ("Segoe UI", 16),
            "width": 15,
            "height": 2,
            "bg": "#222",
            "fg": "white",
            "activebackground": "#444",
            "activeforeground": "white",
            "bd": 0
        }

        btn_cs2 = tk.Button(self.root, text="CS2", command=lambda: self.open_link("https://yourlink.com/cs2"), **btn_config)
        btn_roblox = tk.Button(self.root, text="Roblox", command=lambda: self.open_link("https://yourlink.com/roblox"), **btn_config)
        btn_skate3 = tk.Button(self.root, text="Skate 3", command=lambda: self.open_link("https://yourlink.com/skate3"), **btn_config)

        btn_cs2.place(x=200, y=100)
        btn_roblox.place(x=200, y=170)
        btn_skate3.place(x=200, y=240)

    def toggle_dropdown(self, frame):
        if frame.winfo_ismapped():
            frame.place_forget()
        else:
            frame.place(x=460, y=35)

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

# 🪄 Hide console window (if run via pythonw or as exe this is irrelevant)
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

root = tk.Tk()
app = CheatClient(root)
root.mainloop()
