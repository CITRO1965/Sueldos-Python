import mysql.connector
from mysql.connector import Error

def obtener_conexion(database_name='nombre_de_tu_bd'):
    """
    Establece y retorna la conexión activa con el servidor MySQL.
    Ajusta las credenciales según tu entorno.
    """
    # try:
       # conexion = mysql.connector.connect(
       #     host='localhost',       # O la IP de tu servidor MySQL
       #     port=3306,
       #     user='root',           # Tu usuario de MySQL
       #     password='ElbaNerone', # Tu contraseña de MySQL
       #     database=sueldosre
       # )
       # if conexion.is_connected():
       #     return conexion
    # except Error as e:
    #    print(f"Error al conectar con la base de datos MySQL: {e}")
    #    return None