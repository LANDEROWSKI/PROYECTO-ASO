import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk


class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")
        self.files = {}  # Diccionario para almacenar archivos y sus datos

        # Dimensiones de la ventana principal
        self.root.geometry("800x600")

        # Crear botones de la interfaz
        button_font = ("Arial", 16, "bold")

        # Cargar íconos
        create_icon = ImageTk.PhotoImage(Image.open("icons/create.png").resize((40, 40)))
        read_icon = ImageTk.PhotoImage(Image.open("icons/read.png").resize((40, 40)))
        write_icon = ImageTk.PhotoImage(Image.open("icons/write.png").resize((40, 40)))
        delete_icon = ImageTk.PhotoImage(Image.open("icons/delete.png").resize((40, 40)))
        list_icon = ImageTk.PhotoImage(Image.open("icons/list.png").resize((40, 40)))

        # Botones
        tk.Button(root, text=" Crear Archivo", font=button_font, image=create_icon, compound="left",
                  command=self.create_file, padx=10, pady=10).pack(pady=15)
        tk.Button(root, text=" Leer Archivo", font=button_font, image=read_icon, compound="left",
                  command=self.read_file, padx=10, pady=10).pack(pady=15)
        tk.Button(root, text=" Escribir Archivo", font=button_font, image=write_icon, compound="left",
                  command=self.write_file, padx=10, pady=10).pack(pady=15)
        tk.Button(root, text=" Eliminar Archivo", font=button_font, image=delete_icon, compound="left",
                  command=self.delete_file, padx=10, pady=10).pack(pady=15)
        tk.Button(root, text=" Mostrar Archivos", font=button_font, image=list_icon, compound="left",
                  command=self.list_files, padx=10, pady=10).pack(pady=15)

        # Evitar recolección de basura de íconos
        self.icons = [create_icon, read_icon, write_icon, delete_icon, list_icon]

    def create_file(self):
        file_name = self.show_dialog("Crear Archivo", "Nombre del archivo:")
        if not file_name:
            messagebox.showerror("Error", "Debe ingresar un nombre de archivo.")
            return

        if file_name in self.files:
            messagebox.showwarning("Advertencia", f"El archivo '{file_name}' ya existe.")
        else:
            self.files[file_name] = {"content": "", "permissions": "rw"}
            messagebox.showinfo("Éxito", f"Archivo '{file_name}' creado exitosamente.")

    def read_file(self):
        self.show_file_selection("Leer Archivo", self.display_file_content)

    def write_file(self):
        self.show_file_selection("Escribir Archivo", self.update_file_content)

    def delete_file(self):
        self.show_file_selection("Eliminar Archivo", self.remove_file)

    def list_files(self):
        """Muestra los archivos en una nueva ventana como lista."""
        if not self.files:
            messagebox.showinfo("Archivos Disponibles", "No hay archivos en el sistema.")
            return

        # Crear una nueva ventana
        list_window = tk.Toplevel(self.root)
        list_window.title("Archivos Disponibles")
        list_window.geometry("500x400")
        list_window.configure(bg="white")

        # Agregar un título a la ventana
        tk.Label(list_window, text="Archivos en el sistema:", font=("Arial", 16), bg="white").pack(pady=10)

        # Crear un Listbox para mostrar los archivos
        file_listbox = tk.Listbox(list_window, font=("Arial", 14), height=15)
        file_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        # Agregar los archivos al Listbox
        for file_name in self.files:
            file_listbox.insert(tk.END, file_name)

        # Botón para cerrar la ventana
        close_button = tk.Button(list_window, text="Cerrar", font=("Arial", 14), command=list_window.destroy)
        close_button.pack(pady=10)

    def show_file_selection(self, title, action=None):
        if not self.files:
            messagebox.showinfo("Archivos Disponibles", "No hay archivos en el sistema.")
            return

        selection_window = tk.Toplevel(self.root)
        selection_window.title(title)
        selection_window.geometry("500x400")
        selection_window.configure(bg="white")

        tk.Label(selection_window, text="Seleccione un archivo:", font=("Arial", 16), bg="white").pack(pady=10)

        file_listbox = tk.Listbox(selection_window, font=("Arial", 14), height=10)
        file_listbox.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for file_name in self.files:
            file_listbox.insert(tk.END, file_name)

        def on_select():
            selected = file_listbox.curselection()
            if not selected:
                messagebox.showerror("Error", "Debe seleccionar un archivo.")
                return

            file_name = file_listbox.get(selected[0])
            selection_window.destroy()
            if action:
                action(file_name)

        tk.Button(selection_window, text="Seleccionar", font=("Arial", 14), command=on_select).pack(pady=10)

    def display_file_content(self, file_name):
        file_data = self.files[file_name]
        if "r" in file_data["permissions"]:
            content = file_data["content"]

            content_window = tk.Toplevel(self.root)
            content_window.title(f"Contenido de '{file_name}'")
            content_window.geometry("600x400")
            content_window.configure(bg="white")

            content_label = tk.Label(content_window, text=content, font=("Arial", 18), wraplength=500, justify="center")
            content_label.pack(pady=20)

            tk.Button(content_window, text="Cerrar", font=("Arial", 14), command=content_window.destroy).pack(pady=10)
        else:
            messagebox.showerror("Permiso Denegado", f"No tiene permiso para leer '{file_name}'.")

    def update_file_content(self, file_name):
        file_data = self.files[file_name]
        if "w" in file_data["permissions"]:
            new_content = self.show_dialog("Escribir Archivo", "Ingrese el contenido:")
            if new_content is not None:
                file_data["content"] = new_content
                messagebox.showinfo("Éxito", f"Contenido actualizado en '{file_name}'.")
        else:
            messagebox.showerror("Permiso Denegado", f"No tiene permiso para escribir en '{file_name}'.")

    def remove_file(self, file_name):
        del self.files[file_name]
        messagebox.showinfo("Éxito", f"Archivo '{file_name}' eliminado.")

    def show_dialog(self, title, prompt):
        return simpledialog.askstring(title, prompt, parent=self.root)


def show_image_presentation(root, callback):
    presentation_window = tk.Toplevel(root)
    presentation_window.geometry("800x600")
    presentation_window.title("Presentación")
    presentation_window.configure(bg="black")

    image = Image.open("presentacion.png")
    image = image.resize((800, 600), Image.LANCZOS)
    img = ImageTk.PhotoImage(image)

    label = tk.Label(presentation_window, image=img, bg="black")
    label.image = img
    label.pack()

    presentation_window.after(2000, lambda: (presentation_window.destroy(), callback()))


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    show_image_presentation(root, root.deiconify)
    app = FileSystemSimulator(root)
    root.mainloop()
