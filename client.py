import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import requests
import webbrowser
import os
import threading

# Auto-install requests
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
except ImportError:
    install("requests")
    import requests

SERVER_URL = 'http://127.0.0.1:5000'  # Replace with your server IP
SESSION_FILE = "session.txt"

class CheatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Free Cheat Login")
        self.root.geometry("800x500")
        self.root.configure(bg="#111")
        self.username_str = ""
        self.dropdown_visible = False
        self.auto_login()

    def auto_login(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    user, pw = f.read().strip().split(":")
                data = self.send_request('/login', {'username': user, 'password': pw})
                if data['success']:
                    self.username_str = user
                    self.cheat_menu()
                    return
            except:
                pass
        self.login_page()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="Username", font=("Segoe UI", 14), bg="#111", fg="white").pack(pady=(60, 5))
        self.username = tk.Entry(self.root, font=("Segoe UI", 13))
        self.username.pack()
        tk.Label(self.root, text="Password", font=("Segoe UI", 14), bg="#111", fg="white").pack(pady=5)
        self.password = tk.Entry(self.root, show="*", font=("Segoe UI", 13))
        self.password.pack()

        self.remember_var = tk.IntVar()
        tk.Checkbutton(self.root, text="Remember Me", variable=self.remember_var, bg="#111", fg="white", selectcolor="#111").pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login, font=("Segoe UI", 12), width=15, bg="#333", fg="white").pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register, font=("Segoe UI", 12), width=15, bg="#444", fg="white").pack()

    def register(self):
        data = self.send_request('/register', {
            'username': self.username.get(),
            'password': self.password.get()
        })
        messagebox.showinfo("Register", data.get('msg', 'Registered!' if data['success'] else 'Failed'))

    def login(self):
        user = self.username.get()
        pw = self.password.get()
        data = self.send_request('/login', {'username': user, 'password': pw})
        if data['success']:
            self.username_str = user
            if self.remember_var.get():
                with open(SESSION_FILE, "w") as f:
                    f.write(f"{user}:{pw}")
            self.cheat_menu()
        else:
            messagebox.showerror("Login Failed", data.get('msg', 'Unknown error'))

    def cheat_menu(self):
        self.clear()
        self.root.geometry("800x500")
        self.root.configure(bg="#111")

        # ☰ Dropdown Button
        self.dropdown_btn = tk.Button(self.root, text="☰", font=("Segoe UI", 14), command=self.toggle_dropdown,
                                      bg="#222", fg="white", bd=0, activebackground="#444")
        self.dropdown_btn.place(x=760, y=5, width=30, height=30)

        # Dropdown Frame
        self.dropdown_frame = tk.Frame(self.root, bg="#222", highlightbackground="white", highlightthickness=1)
        tk.Label(self.dropdown_frame, text=self.username_str, bg="#222", fg="white", font=("Segoe UI", 10)).pack(pady=(5, 0), padx=10)
        tk.Button(self.dropdown_frame, text="Sign Out", command=self.sign_out, bg="#444", fg="white", bd=0).pack(pady=3, padx=10, fill="x")
        tk.Button(self.dropdown_frame, text="X", command=self.root.quit, bg="#aa2222", fg="white", bd=0).pack(pady=3, padx=10, fill="x")

        # Game Buttons (Horizontal)
        btn_info = [
            ("CS2", "https://yourlink.com/cs2"),
            ("Roblox", "https://yourlink.com/roblox"),
            ("Skate 3", "https://yourlink.com/skate3")
        ]

        x_start = 130
        spacing = 180
        for i, (name, link) in enumerate(btn_info):
            b = tk.Button(self.root, text=name, font=("Segoe UI", 16), width=12, height=2,
                          bg="#333333", fg="white", bd=0,
                          activeforeground="white", cursor="hand2",
                          command=lambda url=link: self.open_link(url))
            b.place(x=x_start + i * spacing, y=200)
            self.animate_button_fade(b)

        # Bottom-right link emoji
        link_btn = tk.Button(self.root, text="🔗", font=("Segoe UI", 16), command=lambda: self.open_link("https://yourlink.com/info"),
                             bg="#111", fg="white", bd=0, activebackground="#111", activeforeground="lightblue", cursor="hand2")
        link_btn.place(x=770, y=460)

    def toggle_dropdown(self):
        if self.dropdown_visible:
            self.dropdown_frame.place_forget()
        else:
            self.dropdown_frame.place(x=650, y=40, width=140)
        self.dropdown_visible = not self.dropdown_visible

    def sign_out(self):
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.username_str = ""
        self.dropdown_visible = False
        self.login_page()

    def animate_button_fade(self, button):
        normal_bg = "#333333"
        hover_bg = "#3399FF"
        steps = 10

        def fade_to(color1, color2):
            r1, g1, b1 = self.hex_to_rgb(color1)
            r2, g2, b2 = self.hex_to_rgb(color2)
            dr = (r2 - r1) / steps
            dg = (g2 - g1) / steps
            db = (b2 - b1) / steps

            def update(step=0):
                if step > steps: return
                nr = int(r1 + dr * step)
                ng = int(g1 + dg * step)
                nb = int(b1 + db * step)
                button.config(bg=self.rgb_to_hex((nr, ng, nb)))
                self.root.after(15, update, step + 1)

            update()

        def on_enter(e): fade_to(normal_bg, hover_bg)
        def on_leave(e): fade_to(hover_bg, normal_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, rgb):
        return "#%02x%02x%02x" % rgb

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

# 🪄 Hide console window (Windows only)
if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

root = tk.Tk()
app = CheatClient(root)
root.mainloop()
