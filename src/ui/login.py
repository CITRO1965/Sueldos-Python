import tkinter as tk
from tkinter import ttk, messagebox
import os

# 1. Obtener la ruta hasta la carpeta 'src'
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_LLAVES = os.path.join(SRC_DIR, "assets", "llaves.png")

class LoginVentana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent  # Guardamos la referencia al padre (main.py)
        self.login_exitoso = False

        self.title("Ingreso al sistema")
        self.resizable(False, False)

        # Configuración modal
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.al_cerrar)

        # Dimensions y centrado
        ancho_ventana = 450
        alto_ventana = 280
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        pos_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        pos_y = int((alto_pantalla / 2) - (alto_ventana / 2))
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
        
        # Color celeste de fondo idéntico a tu pantalla original
        COLOR_FONDO = "#87CEEB"
        self.configure(bg=COLOR_FONDO)

        # Contenedor Principal
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(fill="both", expand=True, padx=15, pady=15)

        # --- PANEL IZQUIERDO: Imagen (Opcional) ---
        frame_imagen = tk.Frame(frame_principal, bg=COLOR_FONDO)
        frame_imagen.pack(side="left", padx=(0, 15))

        # Si colocas un archivo 'llaves.png' en la raíz, se mostrará automáticamente
        if os.path.exists(RUTA_LLAVES):
           # Guardamos la imagen en 'self.img' para que Python no la borre de memoria (Garbage Collector)
           self.img = tk.PhotoImage(file=RUTA_LLAVES)
           lbl_img = tk.Label(frame_imagen, image=self.img, bg=COLOR_FONDO)
           lbl_img.pack()
        else:
           # Si por alguna razón la imagen no existe en disco, muestra un texto alternativo
           lbl_img = tk.Label(frame_imagen, text="[ Logo ]", bg=COLOR_FONDO)
           lbl_img.pack()

        # --- PANEL DERECHO: Campos de Entrada ---
        frame_campos = tk.LabelFrame(frame_principal, bg=COLOR_FONDO, bd=1, relief="solid")
        frame_campos.pack(side="right", fill="both", expand=True, padx=5, pady=5)

        # Usuario
        tk.Label(frame_campos, text="Usuario", font=("Arial", 9, "bold"), bg=COLOR_FONDO).grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.txt_usuario = tk.Entry(frame_campos, font=("Arial", 10), bg="#E0F7FA") # Tono verdoso claro al enfocar
        self.txt_usuario.grid(row=0, column=1, padx=10, pady=8, sticky="ew")

        # Password
        tk.Label(frame_campos, text="Password", font=("Arial", 9, "bold"), bg=COLOR_FONDO).grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self.txt_password = tk.Entry(frame_campos, font=("Arial", 10), show="*")
        self.txt_password.grid(row=1, column=1, padx=10, pady=8, sticky="ew")

        # Empresas (Desplegable Combo)
        tk.Label(frame_campos, text="Empresas", font=("Arial", 9, "bold"), bg=COLOR_FONDO).grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self.combo_empresas = ttk.Combobox(frame_campos, state="readonly", font=("Arial", 9))
        self.combo_empresas['values'] = ("MEDANO VIATICOS", "EMPRESA PRUEBA S.A.") # Carga estática inicial
        self.combo_empresas.current(0)
        self.combo_empresas.grid(row=2, column=1, padx=10, pady=8, sticky="ew")

        frame_campos.columnconfigure(1, weight=1)

        # --- BOTONES SUPERIORES / INFERIORES ---
        frame_botones = tk.Frame(self, bg=COLOR_FONDO)
        frame_botones.pack(fill="x", side="bottom", padx=15, pady=(0, 15))

        btn_salir = tk.Button(frame_botones, text="Salir", width=10, command=self.al_cerrar)
        btn_salir.pack(side="right", padx=5)

        btn_ok = tk.Button(frame_botones, text="OK", width=10, command=self.validar_ingreso)
        btn_ok.pack(side="right", padx=5)

        # Configuración modal y foco al FINAL de __init__
        self.transient(parent)
        self.grab_set()

        # Forzar el foco a la ventana y luego al Entry
        self.after(100, self.activar_foco_inicial)

    def activar_foco_inicial(self):
        self.focus_force()            # Fuerza la ventana activa en Windows
        self.txt_usuario.focus_set()  # Coloca el cursor en el Entry

    def validar_ingreso(self):
        usuario = self.txt_usuario.get()
        clave = self.txt_password.get()

        # Ejemplo simple de validación (luego conectarás con MySQL)
        if usuario != "" and clave != "":
            self.login_exitoso = True
            self.grab_release() # Libera el bloqueo modal
            self.destroy()      # Cierra la ventana de login
        else:
            messagebox.showwarning("Atención", "Debe completar usuario y contraseña")

    def al_cerrar(self):
        self.grab_release()     # Libera el foco modal
        self.parent.destroy()   # Destruye la ventana principal (cerrando la app completa)        