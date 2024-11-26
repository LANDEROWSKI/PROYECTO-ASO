import tkinter as tk
from tkinter import ttk, messagebox

# Simulación de sistema de archivos
class FileSystem:
    def __init__(self):
        self.root = {'/': {}}  # Representación inicial del sistema de archivos
        self.current_path = '/'

    def list_dir(self):
        """Lista los archivos y directorios en el directorio actual."""
        return self.root[self.current_path].keys()

    def create_file(self, name):
        """Crea un archivo en el directorio actual."""
        if name in self.root[self.current_path]:
            return False, "Ya existe un archivo o directorio con ese nombre."
        self.root[self.current_path][name] = None  # None representa un archivo
        return True, "Archivo creado con éxito."

    def create_dir(self, name):
        """Crea un directorio en el directorio actual."""
        if name in self.root[self.current_path]:
            return False, "Ya existe un archivo o directorio con ese nombre."
        self.root[self.current_path][name] = {}
        return True, "Directorio creado con éxito."

    def delete(self, name):
        """Elimina un archivo o directorio."""
        if name not in self.root[self.current_path]:
            return False, "El archivo o directorio no existe."
        del self.root[self.current_path][name]
        return True, "Eliminado con éxito."

    def change_dir(self, name):
        """Cambia al directorio especificado."""
        if name == "..":  # Subir al directorio padre
            if self.current_path == '/':
                return False, "Ya estás en la raíz."
            self.current_path = '/'.join(self.current_path.strip('/').split('/')[:-1]) or '/'
            return True, "Directorio cambiado."
        elif name in self.root[self.current_path] and isinstance(self.root[self.current_path][name], dict):
            self.current_path = f"{self.current_path.rstrip('/')}/{name}".strip('/')
            return True, "Directorio cambiado."
        return False, "El directorio no existe."

# Interfaz gráfica con Tkinter
class FileSystemApp:
    def __init__(self, root):
        self.fs = FileSystem()
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")

        # Crear widgets
        self.path_label = tk.Label(root, text=f"Ruta actual: {self.fs.current_path}")
        self.path_label.pack()

        self.listbox = tk.Listbox(root, width=50, height=20)
        self.listbox.pack()

        self.command_frame = tk.Frame(root)
        self.command_frame.pack()

        self.entry = tk.Entry(self.command_frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)

        self.create_file_button = tk.Button(self.command_frame, text="Crear Archivo", command=self.create_file)
        self.create_file_button.pack(side=tk.LEFT, padx=5)

        self.create_dir_button = tk.Button(self.command_frame, text="Crear Directorio", command=self.create_dir)
        self.create_dir_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.command_frame, text="Eliminar", command=self.delete)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.change_dir_button = tk.Button(self.command_frame, text="Cambiar Dir", command=self.change_dir)
        self.change_dir_button.pack(side=tk.LEFT, padx=5)

        self.refresh_listbox()

    def refresh_listbox(self):
        """Actualiza el contenido de la lista."""
        self.listbox.delete(0, tk.END)
        for item in self.fs.list_dir():
            self.listbox.insert(tk.END, item)
        self.path_label.config(text=f"Ruta actual: {self.fs.current_path}")

    def create_file(self):
        """Crea un archivo."""
        name = self.entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Por favor, introduce un nombre.")
            return
        success, message = self.fs.create_file(name)
        if success:
            self.refresh_listbox()
        messagebox.showinfo("Resultado", message)

    def create_dir(self):
        """Crea un directorio."""
        name = self.entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Por favor, introduce un nombre.")
            return
        success, message = self.fs.create_dir(name)
        if success:
            self.refresh_listbox()
        messagebox.showinfo("Resultado", message)

    def delete(self):
        """Elimina un archivo o directorio."""
        name = self.entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Por favor, introduce un nombre.")
            return
        success, message = self.fs.delete(name)
        if success:
            self.refresh_listbox()
        messagebox.showinfo("Resultado", message)

    def change_dir(self):
        """Cambia de directorio."""
        name = self.entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Por favor, introduce un nombre.")
            return
        success, message = self.fs.change_dir(name)
        if success:
            self.refresh_listbox()
        messagebox.showinfo("Resultado", message)

# Ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = FileSystemApp(root)
    root.mainloop()
