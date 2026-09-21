import os
import tkinter as tk
from tkinter import messagebox, ttk
from src.database.users import buscar_usuario_dbf, obtener_empresas_dbf
from src.utils.security import hb_descend


class LoginVentana(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Ingreso al sistema de sueldos")

        # Ajustamos el alto a 260px para que entre cómodamente el desplegable
        ancho = 420
        alto = 260
        pos_x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        pos_y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.resizable(False, False)

        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        ico_path = os.path.join(base_dir, "src", "assets", "Sueldos.ico")
        if os.path.exists(ico_path):
            self.iconbitmap(ico_path)

        self.transient(parent)
        self.grab_set()

        self.intentos = 0
        self.login_exitoso = False
        self.empresa_seleccionada = None

        self.crear_widgets(base_dir)
        self.cargar_empresas()

        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

    def crear_widgets(self, base_dir):
        frame_main = tk.Frame(self)
        frame_main.pack(expand=True, fill="both", padx=15, pady=15)

        # Imagen lateral
        img_path = os.path.join(base_dir, "src", "assets", "llaves.png")
        if os.path.exists(img_path):
            self.img_llaves = tk.PhotoImage(file=img_path)
            if self.img_llaves.width() > 150:
                self.img_llaves = self.img_llaves.subsample(2, 2)
            lbl_img = tk.Label(frame_main, image=self.img_llaves)
            lbl_img.pack(side="left", padx=(0, 15))

        # Formulario
        frame_form = tk.Frame(frame_main)
        frame_form.pack(side="right", expand=True, fill="both")

        # Usuario
        lbl_usuario = tk.Label(
            frame_form, text="Usuario:", anchor="w", font=("Segoe UI", 9, "bold")
        )
        lbl_usuario.pack(fill="x", pady=(2, 2))

        self.txt_usuario = tk.Entry(frame_form)
        self.txt_usuario.pack(fill="x", pady=(0, 5))
        self.txt_usuario.focus_set()

        # Password / Clave
        lbl_clave = tk.Label(
            frame_form, text="Password:", anchor="w", font=("Segoe UI", 9, "bold")
        )
        lbl_clave.pack(fill="x", pady=(0, 2))

        self.txt_clave = tk.Entry(frame_form, show="*")
        self.txt_clave.pack(fill="x", pady=(0, 5))

        # Desplegable de Empresas
        lbl_empresa = tk.Label(
            frame_form, text="Empresas:", anchor="w", font=("Segoe UI", 9, "bold")
        )
        lbl_empresa.pack(fill="x", pady=(0, 2))

        self.cbo_empresas = ttk.Combobox(frame_form, state="readonly")
        self.cbo_empresas.pack(fill="x", pady=(0, 15))

        # Botón Ingresar
        btn_ingresar = tk.Button(
            frame_form, text="Ingresar", command=self.validar_ingreso
        )
        btn_ingresar.pack(fill="x")

    def cargar_empresas(self):
        """Replica la lógica de Harbour leyendo empresas->empresa."""
        lista_empresas = obtener_empresas_dbf(r"S:\antonio\sistema\Resipol\SUELDOS\EMPRESAS.DBF")

        if not lista_empresas:
            # Replicamos: msgstop( "No existen empresas para seleccionar" )
            messagebox.showerror(
                "Error", "No existen empresas para seleccionar"
            )
            self.cbo_empresas["values"] = []
            self.cbo_empresas.set("")
        else:
            self.cbo_empresas["values"] = lista_empresas
            # Replicamos: frmLogin.cboElige.value := nElige (Seleccionar la primera empresa)
            self.cbo_empresas.current(0)

    def validar_ingreso(self):
        usuario = self.txt_usuario.get().strip()
        clave_ingresada = self.txt_clave.get().strip()
        empresa = self.cbo_empresas.get()

        if not usuario or not clave_ingresada:
            messagebox.showwarning(
                "Atención", "Por favor ingrese usuario y clave"
            )
            return

        if not empresa:
            messagebox.showwarning(
                "Atención", "Debe seleccionar una empresa"
            )
            return

        registro = buscar_usuario_dbf(usuario, r"S:\antonio\sistema\Resipol\SUELDOS\USERS.DBF")

        if registro:
            clave_bytes = registro.get("CLAVE", b"")
            pos_delimitador = clave_bytes.find(b"\xe0")
            if pos_delimitador != -1:
                clave_dbf_recortada = clave_bytes[:pos_delimitador]
            else:
                clave_dbf_recortada = clave_bytes.strip()

            clave_desencriptada = hb_descend(clave_dbf_recortada).strip()

            if clave_ingresada.upper() == clave_desencriptada.upper():
                self.login_exitoso = True
                self.empresa_seleccionada = empresa
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