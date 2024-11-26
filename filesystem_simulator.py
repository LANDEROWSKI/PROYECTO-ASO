import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time
import cv2


class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")
        self.files = {}
        self.folders = {}

    def show_linux_desktop(self):
        desktop_window = tk.Toplevel(self.root)
        desktop_window.geometry("800x600")
        desktop_window.title("Escritorio Linux")
        desktop_window.configure(bg="#a9a6a5")

        # Crear barra de tareas
        taskbar = tk.Frame(desktop_window, bg="gray20", height=40)
        taskbar.pack(side="bottom", fill="x")

        # Cargar íconos de la barra de tareas
        wifi_icon = ImageTk.PhotoImage(Image.open("icons/wifi.png").resize((20, 20)))
        battery_icon = ImageTk.PhotoImage(Image.open("icons/battery.png").resize((20, 20)))
        sound_icon = ImageTk.PhotoImage(Image.open("icons/sound.png").resize((20, 20)))

        # Prevenir recolección de basura
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
        desktop_menu = tk.Menu(desktop_window, tearoff=0)
        desktop_menu.add_command(label="Crear Archivo", command=self.create_file)
        desktop_menu.add_command(label="Crear Carpeta", command=self.create_folder)

        def show_desktop_menu(event):
            desktop_menu.post(event.x_root, event.y_root)

        desktop_window.bind("<Button-3>", show_desktop_menu)

        # Crear ícono de carpeta
        folder_icon = ImageTk.PhotoImage(Image.open("icons/folder.png").resize((60, 60)))
        self.folder_icon = folder_icon

        def add_folder_icon(x, y, folder_name):
            folder_button = tk.Button(
                desktop_window, image=folder_icon, bg="#a9a6a5", bd=0, command=lambda: self.open_folder(folder_name)
            )
            folder_button.place(x=x, y=y)
            folder_label = tk.Label(desktop_window, text=folder_name, bg="#a9a6a5", font=("Arial", 10))
            folder_label.place(x=x, y=y + 65)

            # Menú contextual para la carpeta
            folder_menu = tk.Menu(desktop_window, tearoff=0)
            folder_menu.add_command(label="Renombrar", command=lambda: self.rename_folder(folder_name))
            folder_menu.add_command(label="Eliminar", command=lambda: self.delete_folder(folder_name))

            def show_folder_menu(event):
                folder_menu.post(event.x_root, event.y_root)

            folder_button.bind("<Button-3>", show_folder_menu)

        # Agregar una carpeta al escritorio como ejemplo
        self.folders["Nueva_Carpeta"] = []
        add_folder_icon(100, 100, "Nueva_Carpeta")

    # Funciones relacionadas con archivos y carpetas
    def create_file(self):
        filename = simpledialog.askstring("Crear Archivo", "Ingrese el nombre del archivo:")
        if filename:
            if filename in self.files:
                messagebox.showerror("Error", "El archivo ya existe.")
            else:
                self.files[filename] = ""
                messagebox.showinfo("Éxito", f"Archivo '{filename}' creado exitosamente.")

    def create_folder(self):
        folder_name = simpledialog.askstring("Crear Carpeta", "Ingrese el nombre de la carpeta:")
        if folder_name:
            if folder_name in self.folders:
                messagebox.showerror("Error", "La carpeta ya existe.")
            else:
                self.folders[folder_name] = []
                messagebox.showinfo("Éxito", f"Carpeta '{folder_name}' creada exitosamente.")

    def rename_folder(self, folder_name):
        # Garantizar que el cuadro de diálogo sea modal y evite conflictos
        try:
            new_name = simpledialog.askstring(
                "Renombrar Carpeta",
                f"Renombrar '{folder_name}' a:",
                parent=self.root  # Asegurar que pertenece a la ventana principal
            )
            if new_name:
                if new_name in self.folders:
                    messagebox.showerror(
                        "Error", 
                        "El nuevo nombre ya existe.", 
                        parent=self.root
                    )
                else:
                    # Actualizar el nombre de la carpeta
                    self.folders[new_name] = self.folders.pop(folder_name)
                    messagebox.showinfo(
                        "Éxito", 
                        f"Carpeta renombrada a '{new_name}'.", 
                        parent=self.root
                    )
        except Exception as e:
            print(f"Error al renombrar carpeta: {e}")


    def delete_folder(self, folder_name):
        if messagebox.askyesno("Eliminar Carpeta", f"¿Seguro que desea eliminar '{folder_name}'?"):
            del self.folders[folder_name]
            messagebox.showinfo("Éxito", f"Carpeta '{folder_name}' eliminada.")

    def open_folder(self, folder_name):
        folder_window = tk.Toplevel(self.root)
        folder_window.geometry("400x300")
        folder_window.title(f"Carpeta: {folder_name}")
        tk.Label(folder_window, text=f"Archivos en '{folder_name}':", font=("Arial", 12)).pack(pady=10)
        for file in self.folders[folder_name]:
            tk.Label(folder_window, text=file, font=("Arial", 10)).pack(anchor="w", padx=20)


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
