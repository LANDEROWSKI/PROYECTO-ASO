import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk  # Para manejar imágenes


class FileSystemSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Sistema de Archivos")
        self.files = {}  

        self.root.geometry("600x400")


        button_font = ("Arial", 14)

        create_icon = ImageTk.PhotoImage(Image.open("icons/create.png").resize((32, 32)))
        read_icon = ImageTk.PhotoImage(Image.open("icons/read.png").resize((32, 32)))
        write_icon = ImageTk.PhotoImage(Image.open("icons/write.png").resize((32, 32)))
        delete_icon = ImageTk.PhotoImage(Image.open("icons/delete.png").resize((32, 32)))
        list_icon = ImageTk.PhotoImage(Image.open("icons/list.png").resize((32, 32)))

        tk.Button(root, text=" Crear Archivo", font=button_font, image=create_icon, compound="left",
                  command=self.create_file).pack(pady=10)
        tk.Button(root, text=" Leer Archivo", font=button_font, image=read_icon, compound="left",
                  command=self.read_file).pack(pady=10)
        tk.Button(root, text=" Escribir Archivo", font=button_font, image=write_icon, compound="left",
                  command=self.write_file).pack(pady=10)
        tk.Button(root, text=" Eliminar Archivo", font=button_font, image=delete_icon, compound="left",
                  command=self.delete_file).pack(pady=10)
        tk.Button(root, text=" Mostrar Archivos", font=button_font, image=list_icon, compound="left",
                  command=self.list_files).pack(pady=10)


        self.icons = [create_icon, read_icon, write_icon, delete_icon, list_icon]

    def create_file(self):
        file_name = simpledialog.askstring("Crear Archivo", "Nombre del archivo:")
        if not file_name:
            messagebox.showerror("Error", "Debe ingresar un nombre de archivo.")
            return

        if file_name in self.files:
            messagebox.showwarning("Advertencia", f"El archivo '{file_name}' ya existe.")
        else:
            self.files[file_name] = {"content": "", "permissions": "rw"}  # rw: Leer y Escribir
            messagebox.showinfo("Éxito", f"Archivo '{file_name}' creado exitosamente.")

    def read_file(self):
        file_name = simpledialog.askstring("Leer Archivo", "Nombre del archivo:")
        if not file_name:
            return

        if file_name in self.files:
            file_data = self.files[file_name]
            if "r" in file_data["permissions"]:
                content = file_data["content"]
                messagebox.showinfo("Contenido del Archivo", f"Contenido de '{file_name}':\n{content}")
            else:
                messagebox.showerror("Permiso Denegado", f"No tiene permiso para leer '{file_name}'.")
        else:
            messagebox.showerror("Error", f"El archivo '{file_name}' no existe.")

    def write_file(self):
        file_name = simpledialog.askstring("Escribir Archivo", "Nombre del archivo:")
        if not file_name:
            return

        if file_name in self.files:
            file_data = self.files[file_name]
            if "w" in file_data["permissions"]:
                new_content = simpledialog.askstring("Escribir Archivo", "Ingrese el contenido:")
                if new_content is not None:
                    file_data["content"] = new_content
                    messagebox.showinfo("Éxito", f"Contenido escrito en '{file_name}'.")
            else:
                messagebox.showerror("Permiso Denegado", f"No tiene permiso para escribir en '{file_name}'.")
        else:
            messagebox.showerror("Error", f"El archivo '{file_name}' no existe.")

    def delete_file(self):
        file_name = simpledialog.askstring("Eliminar Archivo", "Nombre del archivo:")
        if not file_name:
            return

        if file_name in self.files:
            del self.files[file_name]
            messagebox.showinfo("Éxito", f"Archivo '{file_name}' eliminado.")
        else:
            messagebox.showerror("Error", f"El archivo '{file_name}' no existe.")

    def list_files(self):
        if self.files:
            file_list = "\n".join([f"{name} (Permisos: {data['permissions']})" for name, data in self.files.items()])
            messagebox.showinfo("Archivos Existentes", f"Archivos:\n{file_list}")
        else:
            messagebox.showinfo("Archivos Existentes", "No hay archivos en el sistema.")


def show_image_presentation(root, callback):
    presentation_window = tk.Toplevel(root)
    presentation_window.geometry("600x400")
    presentation_window.title("Presentación")
    presentation_window.configure(bg="black")


    presentation_window.attributes("-topmost", True)


    image = Image.open("presentacion.png") 
    image = image.resize((600, 400), Image.LANCZOS)
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
