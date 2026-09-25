import tkinter as tk
from tkinter import ttk
from src.context import contexto_app


class VentanaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(f"Sistema de Sueldos - {contexto_app.empresa_nombre}")
        self.geometry("900x600")

        # Barra de menú superior (Boceto)
        barra_menu = tk.Menu(self)
        self.config(menu=barra_menu)

        menu_archivos = tk.Menu(barra_menu, tearoff=0)
        menu_archivos.add_command(label="Legajos")
        menu_archivos.add_command(label="Liquidaciones")
        menu_archivos.add_separator()
        menu_archivos.add_command(label="Salir", command=self.quit)
        barra_menu.add_cascade(label="Archivos", menu=menu_archivos)

        # Contenido central
        frame_central = ttk.Frame(self, padding=20)
        frame_central.pack(expand=True, fill="both")

        lbl_bienvenida = ttk.Label(
            frame_central,
            text=f"Bienvenido, {contexto_app.usuario}",
            font=("Arial", 14, "bold")
        )
        lbl_bienvenida.pack(anchor="w", pady=10)

        lbl_info = ttk.Label(
            frame_central,
            text=f"Empresa Activa: {contexto_app.empresa_nombre}\n"
                 f"Ruta de Datos: {contexto_app.ruta_data}\n"
                 f"Maneja Viáticos: {'Sí' if contexto_app.es_viaticos else 'No'}",
            font=("Arial", 10)
        )
        lbl_info.pack(anchor="w", pady=5)

        # Barra de estado inferior (StatusBar)
        self.statusbar = ttk.Label(
            self,
            text=f" Usuario: {contexto_app.usuario}  |  Empresa: {contexto_app.empresa_nombre}  |  Ruta: {contexto_app.ruta_data}",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)