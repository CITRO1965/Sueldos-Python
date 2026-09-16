import mysql.connector
conexion = mysql.connector.connect(
    host="localhost",      # O la IP de tu servidor MySQL
    user="root",          # Tu usuario de MySQL
    password="ElbaNerone",
    database="sueldosre"
)

cursor = conexion.cursor()
cursor.execute("SELECT VERSION();")
version = cursor.fetchone()

print(f"Conectado exitosamente a MySQL versión: {version[0]}")

cursor.close()
conexion.close()