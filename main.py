import sys
import os

# Agrega la carpeta actual al camino de búsqueda de módulos de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from src.ui.login import LoginVentana

def main():
    root = tk.Tk()
    # app = LoginVentana(root)
    root.title('Tkinter Window Demo')

    # window_width = 300
    # window_height = 200

    # get the screen dimension
    # screen_width = root.winfo_screenwidth()
    #screen_height = root.winfo_screenheight()

    # find the center point
    # center_x = int(screen_width/2 - window_width / 2)
    # center_y = int(screen_height/2 - window_height / 2)

    # set the position of the window to the center of the screen
    # root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')    
    root.state('zoomed')
    root.resizable(False, False)
    root.iconbitmap(r'G:\Proyectos\src\assets\Sueldos.ico')

    # Abrir la ventana modal de login sobre 'root'
    login = LoginVentana(root)
    
    # Pausa la ejecución hasta que la ventana modal se cierre
    root.wait_window(login)

    # Si el login fue exitoso, continúa con el ciclo principal de la aplicación
    if login.login_exitoso:
       root.mainloop()

if __name__ == "__main__":
    main()