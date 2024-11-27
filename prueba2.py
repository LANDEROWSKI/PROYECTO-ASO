import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
from tkinter import simpledialog
import os

# Usuarios y contraseñas predefinidos
users = {
    "Erick": "12345",
    "Angel": "12345"
}

# Rutas de las fotos de perfil
profile_pics = {
    "Erick": "./material/erick.jpg",
    "Angel": "./material/angel.jpg"
}

def login():
    username = username_entry.get()
    password = password_entry.get()
    
    if username in users and users[username] == password:
        welcome_label.config(text=f"¡Bienvenido {username}!", fg="green")
        welcome_label.pack()
        animate_welcome()
        root.after(2000, lambda: [root.withdraw(), open_desktop()])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def animate_welcome():
    for i in range(3):
        welcome_label.after(300 * i, lambda: welcome_label.config(fg="red"))
        welcome_label.after(600 * i, lambda: welcome_label.config(fg="green"))

def update_profile_icon(event=None):
    username = username_entry.get()
    if username in profile_pics:
        image = Image.open(profile_pics[username])
        image = image.resize((100, 100), Image.LANCZOS)
        profile_img = ImageTk.PhotoImage(image)
        profile_label.config(image=profile_img)
        profile_label.image = profile_img
    else:
        profile_label.config(image='')
        profile_label.image = None

# Configuración de la interfaz principal
root = tk.Tk()
root.title("Login")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

profile_label = tk.Label(root, bg="#f0f0f0")
profile_label.pack(pady=20, anchor='center')

username_entry = tk.Entry(root, justify="center", font=("Arial", 18), width=25)
username_entry.pack(pady=10, anchor='center')
username_entry.bind("<KeyRelease>", update_profile_icon)

password_entry = tk.Entry(root, show="*", justify="center", font=("Arial", 18), width=25)
password_entry.pack(pady=10, anchor='center')

login_button = tk.Button(root, text="Login", command=login, bg="#28a745", fg="white", font=("Arial", 20), width=20)
login_button.pack(pady=20, anchor='center')

welcome_label = tk.Label(root, text="", font=("Arial", 24), bg="#f0f0f0", anchor='center')

def open_desktop():
    desktop_window = tk.Toplevel(root)
    desktop_window.geometry("800x600")
    desktop_window.title("Escritorio Linux")
    desktop_window.configure(bg="#a9a6a5")
    open_desktop.create_file_position_counter = 0

    def create_file(window):
        file_name = simpledialog.askstring("Crear archivo", "Nombre del archivo:")
        if file_name:
            file_icon = ImageTk.PhotoImage(Image.open("./icons/file.png").resize((50, 50)))
            file_label = tk.Label(window, text=file_name, image=file_icon, compound="top", bg="#a9a6a5", font=("Arial", 10), padx=10, pady=5)
            file_label.bind("<Button-1>", lambda e, name=file_name: open_file_window(name))
            file_label.image = file_icon  # Prevenir recolección de basura
            open_desktop.create_file_position_counter += 1
            row = open_desktop.create_file_position_counter // 5
            col = open_desktop.create_file_position_counter % 5
            file_label.place(x=100 + col * 100, y=50 + row * 100)

    def open_file_window(file_name):
        file_window = tk.Toplevel(desktop_window)
        file_window.geometry("600x400")
        file_window.title(file_name)
        
        try:
            with open(f"./{file_name}.txt", "r") as f:
                file_content = f.read()
        except FileNotFoundError:
            file_content = ""
        
        text_area = tk.Text(file_window, wrap='word', font=("Arial", 12), height=15, width=50)
        text_area.insert("1.0", file_content)
        text_area.pack(padx=10, pady=10)
        
        save_button = tk.Button(file_window, text="Guardar", command=lambda: [save_file(file_name, text_area.get("1.0", tk.END)), file_window.destroy()], bg="#28a745", fg="white", font=("Arial", 12))
        save_button.pack(pady=10)

    def save_file(file_name, content):
        with open(f"./{file_name}.txt", "w") as f:
            f.write(content)
        
    

    # Crear barra de tareas
    taskbar = tk.Frame(desktop_window, bg="gray20", height=40)
    taskbar.pack(side="bottom", fill="x")

    # Cargar íconos de la barra de tareas
    wifi_icon = ImageTk.PhotoImage(Image.open("./icons/wifi.png").resize((20, 20)))
    battery_icon = ImageTk.PhotoImage(Image.open("./icons/battery.png").resize((20, 20)))
    sound_icon = ImageTk.PhotoImage(Image.open("./icons/sound.png").resize((20, 20)))

    # Prevenir recolección de basura
    desktop_window.taskbar_icons = [wifi_icon, battery_icon, sound_icon]

    # Widgets para íconos de la barra de tareas
    tk.Label(taskbar, image=wifi_icon, bg="gray20").pack(side="left", padx=5, pady=5)
    tk.Label(taskbar, image=battery_icon, bg="gray20").pack(side="left", padx=5, pady=5)
    tk.Label(taskbar, image=sound_icon, bg="gray20").pack(side="left", padx=5, pady=5)

    # Reloj en la barra de tareas
    clock_label = tk.Label(taskbar, text="", bg="gray20", fg="white", font=("Arial", 12))
    clock_label.pack(side="right", padx=10)

    def update_time():
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d/%m/%Y")
        clock_label.config(text=f"{current_date}    {current_time}")
        clock_label.after(1000, update_time)

    update_time()

    # Habilitar clic derecho para crear archivo
    def on_right_click(event):
        context_menu.post(event.x_root, event.y_root)

    desktop_window.bind("<Button-3>", on_right_click)

    # Crear menú contextual
    context_menu = tk.Menu(desktop_window, tearoff=0)
    context_menu.add_command(label="Crear archivo", command=lambda: create_file(desktop_window))


def delete_all_files():
    for file in os.listdir("./"):
        if file.endswith(".txt"):
            os.remove(file)

delete_all_files()
root.mainloop()
