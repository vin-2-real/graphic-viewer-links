# client.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
import webbrowser
import subprocess
import sys

# Auto-install required modules
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import requests
except ImportError:
    install("requests")
    import requests

try:
    from PIL import Image, ImageTk
except ImportError:
    install("pillow")
    from PIL import Image, ImageTk


SERVER_URL = 'http://YOUR_SERVER_IP:5000'

def send_request(endpoint, data):
    try:
        r = requests.post(SERVER_URL + endpoint, json=data)
        return r.json()
    except Exception as e:
        return {'success': False, 'msg': str(e)}

class CheatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Login/Register")
        self.root.geometry("400x300")
        self.login_page()

    def login_page(self):
        self.clear()
        tk.Label(self.root, text="Username").pack()
        self.username = tk.Entry(self.root)
        self.username.pack()
        tk.Label(self.root, text="Password").pack()
        self.password = tk.Entry(self.root, show="*")
        self.password.pack()
        tk.Button(self.root, text="Login", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register).pack()

    def register(self):
        data = send_request('/register', {
            'username': self.username.get(),
            'password': self.password.get()
        })
        messagebox.showinfo("Register", data.get('msg', 'Registered!' if data['success'] else 'Failed'))

    def login(self):
        data = send_request('/login', {
            'username': self.username.get(),
            'password': self.password.get()
        })
        if data['success']:
            self.cheat_menu()
        else:
            messagebox.showerror("Login Failed", data.get('msg', 'Unknown error'))

    def cheat_menu(self):
        self.clear()
        self.root.geometry("500x400")
        links = {
            "CS2": "https://yourlink.com/cs2",
            "Roblox": "https://yourlink.com/roblox",
            "Skate 3": "https://yourlink.com/skate3"
        }
        for i, (name, url) in enumerate(links.items()):
            img = ImageTk.PhotoImage(Image.open(f"{name.lower()}.png").resize((150, 100)))
            b = tk.Button(self.root, image=img, command=lambda u=url: webbrowser.open(u))
            b.image = img
            b.place(x=30 + (i * 160), y=100)

        # Top right image
        top_img = ImageTk.PhotoImage(Image.open("info_icon.png").resize((40, 40)))
        top_btn = tk.Button(self.root, image=top_img, command=lambda: webbrowser.open("https://yourdiscord.com"))
        top_btn.image = top_img
        top_btn.place(x=450, y=10)

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = CheatClient(root)
root.mainloop()
