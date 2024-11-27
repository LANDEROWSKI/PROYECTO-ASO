import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json
import os
import time
import cv2
import subprocess


class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")

        # Mostrar mensaje de bienvenida
        messagebox.showinfo("Bienvenido", "Bienvenido al Simulador de Sistema de Archivos")

        # Archivo para guardar el sistema de archivos
        self.filesystem_file = "filesystem.json"

        # Cargar sistema de archivos existente o crear uno nuevo
        if os.path.exists(self.filesystem_file):
            with open(self.filesystem_file, "r") as f:
                self.filesystem = json.load(f)
        else:
            self.filesystem = {"root": {"folders": {}, "files": {}}}

        self.icon_size = (60, 60)
        self.grid_size = (8, 6)  # 8 columnas x 6 filas
        self.icon_spacing = 100

    def save_filesystem(self):
        """Guardar el sistema de archivos en un archivo JSON."""
        with open(self.filesystem_file, "w") as f:
            json.dump(self.filesystem, f, indent=4)

    def show_linux_desktop(self):
        self.desktop_window = tk.Toplevel(self.root)
        self.desktop_window.geometry("800x600")
        self.desktop_window.title("Escritorio Linux")
        self.desktop_window.configure(bg="#a9a6a5")

        # Crear barra de tareas
        taskbar = tk.Frame(self.desktop_window, bg="gray20", height=40)
        taskbar.pack(side="bottom", fill="x")

        # Cargar íconos de la barra de tareas
        wifi_icon = ImageTk.PhotoImage(Image.open("icons/wifi.png").resize((20, 20)))
        battery_icon = ImageTk.PhotoImage(Image.open("icons/battery.png").resize((20, 20)))
        sound_icon = ImageTk.PhotoImage(Image.open("icons/sound.png").resize((20, 20)))

        self.taskbar_icons = [wifi_icon, battery_icon, sound_icon]

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

        # Crear menú contextual para el escritorio
        desktop_menu = tk.Menu(self.desktop_window, tearoff=0)
        desktop_menu.add_command(label="Crear Archivo", command=lambda: self.create_file("root"))
        desktop_menu.add_command(label="Crear Carpeta", command=lambda: self.create_folder("root"))

        def show_desktop_menu(event):
            desktop_menu.post(event.x_root, event.y_root)

        self.desktop_window.bind("<Button-3>", show_desktop_menu)
        
        # Renderizar los íconos del escritorio
        self.render_icons(self.desktop_window, "root")

    def render_icons(self, parent_window, path):
        """Renderizar íconos de archivos y carpetas."""
        for widget in parent_window.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                widget.destroy()

        x, y = 20, 20
        for folder in self.filesystem[path]["folders"]:
            self.add_icon(parent_window, x, y, folder, is_folder=True, path=path)
            x += self.icon_spacing
            if x >= self.icon_spacing * self.grid_size[0]:
                x = 20
                y += self.icon_spacing

        for file in self.filesystem[path]["files"]:
            self.add_icon(parent_window, x, y, file, is_folder=False, path=path)
            x += self.icon_spacing
            if x >= self.icon_spacing * self.grid_size[0]:
                x = 20
                y += self.icon_spacing

        # Agregar íconos para ejecutar niveluno.py, niveltres.py, niveldos.py y nivelseguridad.py
        self.add_python_icon(parent_window, x, y, "niveluno.py", "icons/uno.png")
        x += self.icon_spacing
        if x >= self.icon_spacing * self.grid_size[0]:
            x = 20
            y += self.icon_spacing
        self.add_python_icon(parent_window, x, y, "niveltres.py", "icons/tres.png")
        x += self.icon_spacing
        if x >= self.icon_spacing * self.grid_size[0]:
            x = 20
            y += self.icon_spacing
        self.add_python_icon(parent_window, x, y, "niveldos.py", "icons/dos.png")
        x += self.icon_spacing
        if x >= self.icon_spacing * self.grid_size[0]:
            x = 20
            y += self.icon_spacing
        self.add_python_icon(parent_window, x, y, "nivelseguridad.py", "icons/seguridad.png")

    def add_icon(self, parent_window, x, y, name, is_folder, path):
        """Agregar ícono de archivo o carpeta."""
        icon = ImageTk.PhotoImage(
            Image.open("icons/folder.png" if is_folder else "icons/file.png").resize(self.icon_size)
        )
        button = tk.Button(
            parent_window,
            image=icon,
            bg="#a9a6a5",
            bd=0,
            command=lambda: self.open_folder_window(path, name) if is_folder else self.open_file(path, name),
        )
        button.image = icon
        button.place(x=x, y=y)
        label = tk.Label(parent_window, text=name, bg="#a9a6a5", font=("Arial", 10))
        label.place(x=x, y=y + self.icon_size[1] + 5)

        # Menú contextual
        menu = tk.Menu(parent_window, tearoff=0)
        menu.add_command(label="Renombrar", command=lambda: self.rename_item(path, name, is_folder))
        menu.add_command(label="Eliminar", command=lambda: self.delete_item(path, name, is_folder))

        def show_context_menu(event):
            menu.post(event.x_root, event.y_root)

        button.bind("<Button-3>", show_context_menu)

    def add_python_icon(self, parent_window, x, y, filename, icon_path):
        """Agregar un ícono en el escritorio para ejecutar un archivo Python."""
        python_icon = ImageTk.PhotoImage(Image.open(icon_path).resize(self.icon_size))
        button = tk.Button(
            parent_window,
            image=python_icon,
            bg="#a9a6a5",
            bd=0,
            command=lambda: self.execute_python_file(filename),
        )
        button.image = python_icon
        button.place(x=x, y=y)
        label = tk.Label(parent_window, text=filename, bg="#a9a6a5", font=("Arial", 10))
        label.place(x=x, y=y + self.icon_size[1] + 5)

    def execute_python_file(self, filename):
        """Ejecutar un archivo Python."""
        try:
            subprocess.Popen(["python", filename])
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo ejecutar el archivo {filename}: {e}")

    def create_file(self, path):
        filename = simpledialog.askstring("Crear Archivo", "Ingrese el nombre del archivo:", parent=self.desktop_window)
        if filename:
            if filename in self.filesystem[path]["files"]:
                messagebox.showerror("Error", "El archivo ya existe.", parent=self.desktop_window)
            else:
                self.filesystem[path]["files"][filename] = ""
                self.save_filesystem()
                self.render_icons(self.desktop_window, path)

    def create_folder(self, path):
        folder_name = simpledialog.askstring("Crear Carpeta", "Ingrese el nombre de la carpeta:", parent=self.desktop_window)
        if folder_name:
            if folder_name in self.filesystem[path]["folders"]:
                messagebox.showerror("Error", "La carpeta ya existe.", parent=self.desktop_window)
            else:
                self.filesystem[path]["folders"][folder_name] = {"folders": {}, "files": {}}
                self.save_filesystem()
                self.render_icons(self.desktop_window, path)

    def rename_item(self, path, name, is_folder):
        new_name = simpledialog.askstring("Renombrar", f"Renombrar '{name}' a:", parent=self.desktop_window)
        if new_name:
            if is_folder:
                self.filesystem[path]["folders"][new_name] = self.filesystem[path]["folders"].pop(name)
            else:
                self.filesystem[path]["files"][new_name] = self.filesystem[path]["files"].pop(name)
            self.save_filesystem()
            self.render_icons(self.desktop_window, path)

    def delete_item(self, path, name, is_folder):
        if messagebox.askyesno("Eliminar", f"¿Seguro que desea eliminar '{name}'?", parent=self.desktop_window):
            if is_folder:
                del self.filesystem[path]["folders"][name]
            else:
                del self.filesystem[path]["files"][name]
            self.save_filesystem()
            self.render_icons(self.desktop_window, path)

    def open_folder_window(self, parent_path, folder_name):
        folder_window = tk.Toplevel(self.desktop_window)
        folder_window.geometry("800x600")
        folder_window.title(f"Carpeta: {folder_name}")
        folder_path = f"{parent_path}/folders/{folder_name}"

        # Crear menú contextual para la carpeta
        folder_menu = tk.Menu(folder_window, tearoff=0)
        folder_menu.add_command(label="Crear Archivo", command=lambda: self.create_file(folder_path))
        folder_menu.add_command(label="Crear Carpeta", command=lambda: self.create_folder(folder_path))

        def show_folder_menu(event):
            folder_menu.post(event.x_root, event.y_root)

        folder_window.bind("<Button-3>", show_folder_menu)
        self.render_icons(folder_window, folder_path)

    def open_file(self, path, filename):
        file_window = tk.Toplevel(self.desktop_window)
        file_window.geometry("600x400")
        file_window.title(f"Archivo: {filename}")

        text_area = tk.Text(file_window, wrap="word")
        text_area.insert("1.0", self.filesystem[path]["files"][filename])
        text_area.pack(expand=True, fill="both")

        def save_file():
            self.filesystem[path]["files"][filename] = text_area.get("1.0", "end-1c")
            self.save_filesystem()
            messagebox.showinfo("Guardado", "Archivo guardado exitosamente.", parent=file_window)

        save_button = tk.Button(file_window, text="Guardar", command=save_file)
        save_button.pack(side="bottom", pady=10)


# Función de presentación
def show_video_presentation(root, callback):
    presentation_window = tk.Toplevel(root)
    presentation_window.geometry("800x600")
    presentation_window.title("Cargando...")
    presentation_window.configure(bg="black")

    video_label = tk.Label(presentation_window, bg="black")
    video_label.pack(expand=True, fill="both")

    cap = cv2.VideoCapture("./material/presentacion.mp4")

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (800, 600))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            video_label.img_tk = img_tk
            video_label.config(image=img_tk)
            presentation_window.after(15, update_frame)
        else:
            cap.release()
            presentation_window.destroy()
            callback()

    update_frame()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    def after_presentation():
        app = FileSystemSimulator(root)
        app.show_linux_desktop()

    show_video_presentation(root, after_presentation)
    root.mainloop()
