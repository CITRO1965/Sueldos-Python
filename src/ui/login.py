import os
import tkinter as tk
from tkinter import messagebox, ttk
from src.database.users import buscar_usuario_dbf, obtener_empresas_dbf, buscar_empresa_detalles_dbf
from src.utils.security import hb_descend
from src.context import contexto_app

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

    def validar_ingreso(self):
            usuario = self.txt_usuario.get().strip().upper()
            clave = self.txt_clave.get().strip()
            empresa_seleccionada = self.cbo_empresas.get().strip()

            if not usuario or not clave:
                messagebox.showwarning("Atención", "Debe ingresar usuario y contraseña.")
                return

            # 1. Buscar usuario en USERS.DBF
            user_db = buscar_usuario_dbf(usuario)

            if not user_db:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            # 2. Extraer la clave en raw/bytes
            clave_raw = (
                user_db.get("clave_raw")
                or user_db.get("clave")
                or user_db.get("CLAVE")
                or user_db.get("clave_bytes")
            )

            if isinstance(clave_raw, str):
                clave_raw = clave_raw.encode("cp850", errors="ignore")

            # =========================================================
            # SECCIÓN A MODIFICAR: DESENCRIPTACIÓN Y DEPURACIÓN
            # =========================================================
            # 3. Desencriptar clave Harbour
            clave_desencriptada = hb_descend(clave_raw)

            # Normalizamos ambas claves (mayúsculas y sin espacios)
            clave_ingresada_clean = clave.strip().upper()
            clave_bd_clean = clave_desencriptada.strip().upper()

            # Imprimimos en la Terminal para ver la diferencia exactas
            print("\n--- DEPURACIÓN DE CONTRASEÑA ---")
            print(f"Clave ingresada en pantalla : '{clave_ingresada_clean}'")
            print(f"Clave desencriptada de BD  : '{clave_bd_clean}'")
            print(f"Bytes puros del DBF        : {clave_raw}")
            print("--------------------------------\n")

            # 4. Comparar contraseña
            if clave_ingresada_clean != clave_bd_clean:
                messagebox.showerror(
                    "Error de Autenticación",
                    f"Contraseña incorrecta.\n\nIngresada: '{clave_ingresada_clean}'\nDesencriptada BD: '{clave_bd_clean}'"
                )
                return
            # =========================================================

            # 5. Si la clave coincide, continuar con la empresa
            datos_empresa = buscar_empresa_detalles_dbf(empresa_seleccionada)

            if datos_empresa:
                try:
                    ruta_final = contexto_app.establecer_empresa(
                        nombre_empresa=datos_empresa["empresa"],
                        directorio_relativo=datos_empresa["directorio"],
                    )
                    contexto_app.usuario = usuario

                    if not os.path.exists(ruta_final):
                        messagebox.showerror(
                            "Error de Directorio",
                            f"La carpeta de la empresa no existe:\n{ruta_final}",
                        )
                        return

                    # 6. Transición a la Ventana Principal
                    self.destroy()
                    app_main = VentanaPrincipal()
                    app_main.mainloop()

                except Exception as e:
                    messagebox.showerror("Error de Configuración", str(e))
            else:
                messagebox.showerror("Error", "No se encontró la configuración de la empresa.")
                
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


    def al_cerrar(self):
        self.grab_release()
        self.parent.destroy()

        # Ejemplo de fragmento dentro de la validación del Login en src/ui/login.py

    def al_confirmar_login(self):
       usuario = self.txt_usuario.get().strip()
       clave = self.txt_clave.get().strip()
       empresa_seleccionada = self.cbo_empresa.get().strip()

       if self.validar_credenciales(usuario, clave):
          datos_empresa = buscar_empresa_detalles_dbf(empresa_seleccionada)

          if datos_empresa:
             try:
                ruta_final = contexto_app.establecer_empresa(
                    nombre_empresa=datos_empresa["empresa"],
                    directorio_relativo=datos_empresa["directorio"],
                )
                contexto_app.usuario = usuario

                # Buscamos los archivos DBF en la carpeta resuelta
                if os.path.exists(ruta_final):
                    archivos = [f for f in os.listdir(ruta_final) if f.upper().endswith(".DBF")]
                    lista_tablas = ", ".join(archivos[:4]) if archivos else "No se encontraron DBFs"
                    
                    # Cartel informativo en pantalla
                    messagebox.showinfo(
                        "Conexión Exitosa a Empresa",
                        f"Empresa: {contexto_app.empresa_nombre}\n"
                        f"Es Viáticos: {contexto_app.es_viaticos}\n\n"
                        f"Ruta DBF Resuelta:\n{ruta_final}\n\n"
                        f"Tablas detectadas ({len(archivos)}):\n{lista_tablas}"
                    )
                else:
                    messagebox.showerror("Error", f"La carpeta no existe:\n{ruta_final}")
                    return

                self.destroy()
                app_main = VentanaPrincipal()
                app_main.mainloop()

             except Exception as e:
                 messagebox.showerror("Error de Configuración", str(e))
          else:
               messagebox.showerror("Error", "No se encontró la configuración de la empresa.")