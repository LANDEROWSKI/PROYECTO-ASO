import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time
import cv2


class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")
        self.filesystem = {"root": {"folders": {}, "files": []}}
        self.current_path = "root"

        self.icon_size = (60, 60)
        self.grid_size = 4
        self.icon_spacing = 100

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
        desktop_menu.add_command(label="Crear Archivo", command=self.create_file)
        desktop_menu.add_command(label="Crear Carpeta", command=self.create_folder)

        def show_desktop_menu(event):
            desktop_menu.post(event.x_root, event.y_root)

        self.desktop_window.bind("<Button-3>", show_desktop_menu)
        self.render_icons()

    def render_icons(self):
        # Eliminar íconos existentes
        for widget in self.desktop_window.winfo_children():
            if isinstance(widget, tk.Button) or isinstance(widget, tk.Label):
                widget.destroy()

        # Renderizar carpetas y archivos
        items = self.filesystem[self.current_path]
        x, y = 20, 20
        for folder in items["folders"]:
            self.add_icon(x, y, folder, is_folder=True)
            x += self.icon_spacing
            if x >= self.icon_spacing * self.grid_size:
                x = 20
                y += self.icon_spacing
        for file in items["files"]:
            self.add_icon(x, y, file, is_folder=False)
            x += self.icon_spacing
            if x >= self.icon_spacing * self.grid_size:
                x = 20
                y += self.icon_spacing

    def add_icon(self, x, y, name, is_folder):
        icon = ImageTk.PhotoImage(
            Image.open("icons/folder.png" if is_folder else "icons/file.png").resize(self.icon_size)
        )
        button = tk.Button(
            self.desktop_window, image=icon, bg="#a9a6a5", bd=0,
            command=lambda: self.open_folder(name) if is_folder else None
        )
        button.image = icon
        button.place(x=x, y=y)
        label = tk.Label(self.desktop_window, text=name, bg="#a9a6a5", font=("Arial", 10))
        label.place(x=x, y=y + self.icon_size[1] + 5)

        # Menú contextual
        menu = tk.Menu(self.desktop_window, tearoff=0)
        menu.add_command(label="Crear Archivo", command=self.create_file)
        menu.add_command(label="Crear Carpeta", command=self.create_folder)

        def show_context_menu(event):
            menu.post(event.x_root, event.y_root)

        button.bind("<Button-3>", show_context_menu)

    def create_file(self):
        filename = simpledialog.askstring("Crear Archivo", "Ingrese el nombre del archivo:")
        if filename:
            if filename in self.filesystem[self.current_path]["files"]:
                messagebox.showerror("Error", "El archivo ya existe.")
            else:
                self.filesystem[self.current_path]["files"].append(filename)
                self.render_icons()

    def create_folder(self):
        folder_name = simpledialog.askstring("Crear Carpeta", "Ingrese el nombre de la carpeta:")
        if folder_name:
            if folder_name in self.filesystem[self.current_path]["folders"]:
                messagebox.showerror("Error", "La carpeta ya existe.")
            else:
                self.filesystem[self.current_path]["folders"][folder_name] = {"folders": {}, "files": []}
                self.render_icons()

    def open_folder(self, folder_name):
        contents = self.filesystem[self.current_path]["folders"][folder_name]

        # Crear una nueva ventana para mostrar los contenidos
        folder_window = tk.Toplevel(self.desktop_window)
        folder_window.title(f"Carpeta: {folder_name}")
        folder_window.geometry("600x400")
        folder_window.configure(bg="#e8e8e8")

        # Texto descriptivo
        tk.Label(folder_window, text=f"Contenido de {folder_name}:", font=("Arial", 14), bg="#e8e8e8").pack(pady=10)

        # Mostrar contenido
        content_frame = tk.Frame(folder_window, bg="#e8e8e8")
        content_frame.pack(fill="both", expand=True)
        content_text = "\n".join(["Archivos:"] + contents["files"] + ["\nCarpetas:"] + list(contents["folders"].keys()))
        tk.Label(content_frame, text=content_text, font=("Arial", 12), bg="#e8e8e8").pack(pady=10)


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
