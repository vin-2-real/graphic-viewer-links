import tkinter as tk
from tkinter import messagebox
import requests
import os
import ctypes
import webbrowser

# Hide console (Windows only)
try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass

# ========== CONFIG ========== #
SERVER_URL = "http://YOUR.SERVER.IP:PORT"
ASSETS_DIR = "assets"
SESSION_FILE = os.path.join(ASSETS_DIR, "session.txt")

LINK_CS2 = "https://example.com/cs2"
LINK_ROBLOX = "https://example.com/roblox"
LINK_SKATE3 = "https://example.com/skate3"
LINK_ICON = "https://example.com/yourdiscord"

# ========== INIT ========== #
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

root = tk.Tk()
root.geometry("600x400")
root.title("Free Cheat Hub")
root.configure(bg="#1e1e1e")

current_user = None
dropdown_open = False

# ========== FADE UTILS ========== #
def fade_color(widget, start, end, steps=10, delay=20):
    r1, g1, b1 = widget.winfo_rgb(start)
    r2, g2, b2 = widget.winfo_rgb(end)
    r_step = (r2 - r1) // steps
    g_step = (g2 - g1) // steps
    b_step = (b2 - b1) // steps

    def update(step=0):
        if step <= steps:
            r = r1 + r_step * step
            g = g1 + g_step * step
            b = b1 + b_step * step
            hex_color = f'#{r//256:02x}{g//256:02x}{b//256:02x}'
            widget.configure(bg=hex_color)
            root.after(delay, lambda: update(step + 1))

    update()

# ========== GUI BUILDERS ========== #
def build_main_menu(username):
    global dropdown_open, dropdown_frame

    for widget in root.winfo_children():
        widget.destroy()

    dropdown_open = False
    dropdown_frame = tk.Frame(root, bg="#2e2e2e", bd=0, relief="flat")

    # Dropdown button
    def toggle_dropdown():
        nonlocal dropdown_open
        if dropdown_open:
            dropdown_frame.place_forget()
            dropdown_open = False
        else:
            dropdown_frame.place(x=460, y=40, width=120)
            dropdown_open = True

    dropdown_button = tk.Button(root, text="☰", bg="#444", fg="white", font=("Segoe UI", 12),
                                command=toggle_dropdown, bd=0, width=3)
    dropdown_button.place(x=560, y=10)

    # Dropdown content
    tk.Label(dropdown_frame, text=username, bg="#2e2e2e", fg="white", font=("Segoe UI", 10)).pack(pady=(5, 0))

    def logout():
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        build_login_screen()

    tk.Button(dropdown_frame, text="Sign Out", bg="#444", fg="white", font=("Segoe UI", 9),
              command=logout, bd=0).pack(pady=3, fill="x")
    tk.Button(dropdown_frame, text="X", bg="#444", fg="white", font=("Segoe UI", 9),
              command=root.destroy, bd=0).pack(pady=3, fill="x")

    # Button builder
    def build_button(text, link, x):
        btn = tk.Label(root, text=text, bg="#444", fg="white", font=("Segoe UI", 14),
                       padx=40, pady=20, cursor="hand2")
        btn.place(x=x, y=150)

        def on_enter(e): fade_color(btn, "#444", "#3a8ee6")
        def on_leave(e): fade_color(btn, "#3a8ee6", "#444")
        def on_click(e): webbrowser.open(link)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", on_click)

    build_button("CS2", LINK_CS2, 60)
    build_button("Skate3", LINK_SKATE3, 230)
    build_button("Roblox", LINK_ROBLOX, 400)

    # Link icon bottom right
    link_label = tk.Label(root, text="🔗", fg="white", bg="#1e1e1e", font=("Segoe UI", 16), cursor="hand2")
    link_label.place(x=570, y=370)
    link_label.bind("<Button-1>", lambda e: webbrowser.open(LINK_ICON))

def build_login_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login/Register", fg="white", bg="#1e1e1e", font=("Segoe UI", 20)).pack(pady=10)

    user_entry = tk.Entry(root, font=("Segoe UI", 12))
    pass_entry = tk.Entry(root, show="*", font=("Segoe UI", 12))
    remember_var = tk.BooleanVar()

    tk.Label(root, text="Username:", fg="white", bg="#1e1e1e").pack()
    user_entry.pack()
    tk.Label(root, text="Password:", fg="white", bg="#1e1e1e").pack()
    pass_entry.pack()
    tk.Checkbutton(root, text="Remember Me", variable=remember_var,
                   bg="#1e1e1e", fg="white", selectcolor="#1e1e1e").pack()

    def login():
        u, p = user_entry.get(), pass_entry.get()
        try:
            r = requests.post(SERVER_URL + "/login", json={"username": u, "password": p})
            if r.status_code == 200:
                if remember_var.get():
                    with open(SESSION_FILE, "w") as f:
                        f.write(f"{u}:{p}")
                build_main_menu(u)
            else:
                messagebox.showerror("Login Failed", r.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def register():
        u, p = user_entry.get(), pass_entry.get()
        try:
            r = requests.post(SERVER_URL + "/register", json={"username": u, "password": p})
            if r.status_code == 200:
                messagebox.showinfo("Success", "Account registered. You can now login.")
            else:
                messagebox.showerror("Register Failed", r.text)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(root, text="Login", command=login, font=("Segoe UI", 12)).pack(pady=5)
    tk.Button(root, text="Register", command=register, font=("Segoe UI", 12)).pack()

# ========== AUTO-LOGIN ========== #
if os.path.exists(SESSION_FILE):
    try:
        with open(SESSION_FILE, "r") as f:
            data = f.read().strip().split(":")
            if len(data) == 2:
                u, p = data
                r = requests.post(SERVER_URL + "/login", json={"username": u, "password": p})
                if r.status_code == 200:
                    build_main_menu(u)
                else:
                    build_login_screen()
            else:
                build_login_screen()
    except:
        build_login_screen()
else:
    build_login_screen()

root.mainloop()
