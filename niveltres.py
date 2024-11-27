import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from PIL import Image, ImageTk, ImageDraw
import time
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

# Inicializar estructura de archivos compartida
filesystem = {}

# Cargar el sistema de archivos desde el archivo JSON si existe
if os.path.exists("niveltres.json"):
    with open("niveltres.json", "r") as f:
        filesystem = json.load(f)
else:
    # Inicializar un directorio vacío compartido
    filesystem = {
        "root": {
            "folders": {},
            "files": {}
        }
    }

# Asegurarse de que el usuario actual esté en el sistema de archivos
current_user = None

def save_filesystem():
    with open("niveluno.json", "w") as f:
        json.dump(filesystem, f, indent=4)

def logout(window):
    window.destroy()
    root.deiconify()
    # Guardar el sistema de archivos al cerrar sesión
    save_filesystem()

def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    
    if username in users and users[username] == password:
        current_user = username
        welcome_label.config(text=f"¡Bienvenido {username}!", fg="#2ecc71")
        welcome_label.pack()
        animate_welcome()
        root.after(2000, lambda: [root.withdraw(), open_desktop()])
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def animate_welcome():
    for i in range(3):
        welcome_label.after(300 * i, lambda: welcome_label.config(fg="#e74c3c"))
        welcome_label.after(600 * i, lambda: welcome_label.config(fg="#2ecc71"))

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
root.configure(bg="#34495e")

# Estilo de la interfaz
title_label = tk.Label(root, text="Sistema de Archivos Virtual", font=("Arial", 32, "bold"), bg="#34495e", fg="#ecf0f1")
title_label.pack(pady=20, anchor='center')

profile_label = tk.Label(root, bg="#34495e")
profile_label.pack(pady=20, anchor='center')

username_label = tk.Label(root, text="Usuario", font=("Arial", 18), bg="#34495e", fg="#ecf0f1")
username_label.pack(pady=5, anchor='center')
username_entry = tk.Entry(root, justify="center", font=("Arial", 18), width=25, bg="#ecf0f1", fg="#34495e", bd=2, relief="groove")
username_entry.pack(pady=5, anchor='center')
username_entry.bind("<KeyRelease>", update_profile_icon)

password_label = tk.Label(root, text="Contraseña", font=("Arial", 18), bg="#34495e", fg="#ecf0f1")
password_label.pack(pady=5, anchor='center')
password_entry = tk.Entry(root, show="*", justify="center", font=("Arial", 18), width=25, bg="#ecf0f1", fg="#34495e", bd=2, relief="groove")
password_entry.pack(pady=5, anchor='center')

login_button = tk.Button(root, text="Iniciar Sesión", command=login, bg="#27ae60", fg="white", font=("Arial", 20, "bold"), width=20, bd=3, relief="raised")
login_button.pack(pady=20, anchor='center')

welcome_label = tk.Label(root, text="", font=("Arial", 24), bg="#34495e", fg="#ecf0f1", anchor='center')

# Mejorar el enfoque en los campos de entrada
username_entry.focus_set()

def open_desktop():
    # Abrir una nueva ventana de escritorio
    desktop_window = tk.Toplevel(root)
    open_desktop.create_file_position_counter = 0

    def create_tree_view(parent, node, parent_name="root"):
        for folder_name, folder_content in node.get("folders", {}).items():
            folder_id = tree.insert(parent, "end", text=folder_name, image=folder_icon, values=("folder", parent_name + "/" + folder_name))
            create_tree_view(folder_id, folder_content, parent_name=parent_name + "/" + folder_name)
        for file_name in node.get("files", {}):
            tree.insert(parent, "end", text=file_name, image=file_icon, values=("file", parent_name + "/" + file_name))

    def create_folder(parent_name="root"):
        folder_name = simpledialog.askstring("Crear carpeta", "Nombre de la carpeta:", parent=desktop_window)
        if folder_name:
            current_node = navigate_to_node(parent_name)
            if folder_name in current_node["folders"]:
                messagebox.showerror("Error", "La carpeta ya existe. Por favor, elige otro nombre.")
            else:
                current_node["folders"][folder_name] = {"folders": {}, "files": {}}
                save_filesystem()
                refresh_tree_view()

    def create_file(parent_name="root"):
        file_name = simpledialog.askstring("Crear archivo", "Nombre del archivo:", parent=desktop_window)
        if file_name:
            current_node = navigate_to_node(parent_name)
            if file_name in current_node["files"]:
                messagebox.showerror("Error", "El archivo ya existe. Por favor, elige otro nombre.")
            else:
                current_node["files"][file_name] = ""
                save_filesystem()
                refresh_tree_view()

    def navigate_to_node(path):
        current_node = filesystem["root"]
        for part in path.split("/"):
            if part and part in current_node["folders"]:
                current_node = current_node["folders"][part]
        return current_node

    def refresh_tree_view():
        for item in tree.get_children():
            tree.delete(item)
        create_tree_view("", filesystem["root"])

    def open_file(file_path):
        current_node = navigate_to_node("/".join(file_path.split("/")[:-1]))
        file_name = file_path.split("/")[-1]
        file_content = current_node["files"].get(file_name, "")

        file_window = tk.Toplevel(desktop_window)
        file_window.geometry("800x600")
        file_window.title(file_name)

        text_area = tk.Text(file_window, wrap='word', font=("Arial", 16), height=20, width=70)
        text_area.insert("1.0", file_content)
        text_area.pack(padx=10, pady=10)

        def save_file():
            current_node["files"][file_name] = text_area.get("1.0", tk.END).strip()
            save_filesystem()

        save_button = tk.Button(file_window, text="Guardar", command=save_file, bg="#28a745", fg="white", font=("Arial", 14))
        save_button.pack(pady=10)

    def generate_tree_diagram():
        def plot_tree(node, ax, x, y, dx):
            ax.text(x, y, list(node.keys())[0], fontsize=10, ha='center', bbox=dict(facecolor='white', edgecolor='black'))
            sub_node = node[list(node.keys())[0]]
            y -= 1
            for i, key in enumerate(sub_node["folders"].keys()):
                new_x = x - dx + 2 * dx * i / max(1, len(sub_node["folders"]) - 1)
                ax.plot([x, new_x], [y + 1, y], color='black')
                plot_tree({key: sub_node["folders"][key]}, ax, new_x, y, dx / 2)
            for j, key in enumerate(sub_node["files"].keys()):
                new_x = x - dx + 2 * dx * (len(sub_node["folders"]) + j) / max(1, len(sub_node["folders"]) + len(sub_node["files"]) - 1)
                ax.plot([x, new_x], [y + 1, y], color='black')
                ax.text(new_x, y, key, fontsize=10, ha='center', bbox=dict(facecolor='lightgrey', edgecolor='black'))

        diagram_window = tk.Toplevel(desktop_window)
        diagram_window.geometry("800x600")
        diagram_window.title("Diagrama de Árbol de Archivos")

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.axis('off')
        plot_tree({"root": filesystem["root"]}, ax, 0, 0, 10)

        canvas = FigureCanvasTkAgg(fig, master=diagram_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    desktop_window.geometry("800x600")
    desktop_window.title(f"Escritorio de {current_user}")
    desktop_window.configure(bg="white")

    # Cargar íconos
    folder_icon = ImageTk.PhotoImage(Image.open("./icons/folder.png").resize((32, 32), Image.LANCZOS))
    file_icon = ImageTk.PhotoImage(Image.open("./icons/file.png").resize((32, 32), Image.LANCZOS))

    # Crear árbol de directorios
    tree = ttk.Treeview(desktop_window)
    tree.pack(side="left", fill="y", padx=10, pady=10)
    tree["columns"] = ("type", "path")
    tree.column("#0", width=250)
    create_tree_view("", filesystem["root"])

    # Crear barra de herramientas
    toolbar = tk.Frame(desktop_window, bg="white", height=80)
    toolbar.pack(side="top", fill="x", padx=10, pady=10)
    
    create_folder_button = tk.Button(toolbar, text="Crear Carpeta", command=lambda: create_folder(tree.item(tree.focus())["values"][1] if tree.focus() else "root"), bg="#28a745", fg="white", font=("Arial", 14))
    create_folder_button.pack(side="top", pady=5)

    create_file_button = tk.Button(toolbar, text="Crear Archivo", command=lambda: create_file(tree.item(tree.focus())["values"][1] if tree.focus() else "root"), bg="#28a745", fg="white", font=("Arial", 14))
    create_file_button.pack(side="top", pady=5)

    generate_diagram_button = tk.Button(toolbar, text="Generar Diagrama", command=generate_tree_diagram, bg="#007bff", fg="white", font=("Arial", 14))
    generate_diagram_button.pack(side="top", pady=5)

    tree.bind("<Double-1>", lambda event: open_file(tree.item(tree.focus())["values"][1]) if tree.item(tree.focus())["values"][0] == "file" else None)

# Iniciar el bucle principal de la interfaz
root.mainloop()
