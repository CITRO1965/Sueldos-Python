import os
import tkinter as tk
from tkinter import messagebox
from src.database.users import buscar_usuario_dbf
from src.utils.security import hb_decrypt


class LoginVentana(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Acceso al Sistema")

        # Tamaños y centrado en pantalla
        ancho = 420
        alto = 220
        pos_x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        pos_y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.resizable(False, False)

        # Cargar ícono de la ventana si existe
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        ico_path = os.path.join(base_dir, "src", "assets", "Sueldos.ico")
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)

        # Configurar modalidad
        self.transient(parent)
        self.grab_set()

        self.intentos = 0
        self.login_exitoso = False

        self.crear_widgets(base_dir)

        # Evento al cerrar (X)
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def crear_widgets(self, base_dir):
        # Frame principal (2 columnas)
        frame_main = tk.Frame(self)
        frame_main.pack(expand=True, fill="both", padx=15, pady=15)

        # Columna Izquierda: Imagen
        img_path = os.path.join(base_dir, "src", "assets", "llaves.png")
        if os.path.exists(img_path):
            self.img_llaves = tk.PhotoImage(file=img_path)
            if self.img_llaves.width() > 150:
                self.img_llaves = self.img_llaves.subsample(2, 2)
            lbl_img = tk.Label(frame_main, image=self.img_llaves)
            lbl_img.pack(side="left", padx=(0, 15))

        # Columna Derecha: Formulario
        frame_form = tk.Frame(frame_main)
        frame_form.pack(side="right", expand=True, fill="both")

        lbl_usuario = tk.Label(frame_form, text="Usuario:", anchor="w")
        lbl_usuario.pack(fill="x", pady=(5, 2))

        self.txt_usuario = tk.Entry(frame_form)
        self.txt_usuario.pack(fill="x", pady=(0, 10))
        self.txt_usuario.focus_set()

        lbl_clave = tk.Label(frame_form, text="Clave:", anchor="w")
        lbl_clave.pack(fill="x", pady=(0, 2))

        self.txt_clave = tk.Entry(frame_form, show="*")
        self.txt_clave.pack(fill="x", pady=(0, 15))

        btn_ingresar = tk.Button(
            frame_form, text="Ingresar", command=self.validar_ingreso
        )
        btn_ingresar.pack(fill="x")

    def validar_ingreso(self):
        usuario = self.txt_usuario.get().strip()
        clave_ingresada = self.txt_clave.get().strip()

        if not usuario or not clave_ingresada:
            messagebox.showwarning(
                "Atención", "Por favor ingrese usuario y clave"
            )
            return

        # Búsqueda en la DBF
        registro = buscar_usuario_dbf(usuario, r"G:\Proyectos\datos\USERS.DBF")

        print("\n--- DEBUG LOGIN ---")
        print("Registro DBF:", registro)

        if registro:
            clave_dbf = registro.get("CLAVE", "").strip()
            clave_descifrada = hb_decrypt(clave_dbf)

            print("Clave tipeada     :", repr(clave_ingresada))
            print("Clave desencriptada:", repr(clave_descifrada))
            print("--------------------\n")

            if clave_ingresada.upper() == clave_descifrada.upper():
                self.login_exitoso = True
                self.al_cerrar()
                return

        self.intentos += 1
        if self.intentos >= 3:
            messagebox.showerror(
                "Error", "Límite de intentos alcanzado. El sistema se cerrará."
            )
            self.al_cerrar()
        else:
            messagebox.showwarning("Error", "Usuario o clave incorrecta")
            self.txt_clave.delete(0, tk.END)
            self.txt_usuario.focus_set()

    def al_cerrar(self):
        self.grab_release()
        self.parent.destroy()