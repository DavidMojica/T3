# EJECUTAR DESDE UNA CARPETA APARTE DEL PROYECTO PARA QUE NO HAYA COMPLICACIONES CON EL ENTORNO VIRTUAL.
import json
import psycopg2

# Configuración de la base de datos PostgreSQL
db_settings = {
    'dbname': 'ssbello7',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': '5432',
}

# Ruta al archivo JSON
json_file_path = 'extras\Colombia.json'  

# Conectarse a la base de datos
connection = psycopg2.connect(**db_settings)
cursor = connection.cursor()

#Cambia el id del pais conforme su id en la base de datos, puse 1 porque estaba creando los municipios de colombia.
id_pais = 1

print(json_file_path)
with open(json_file_path, 'r') as json_file:
    print("gol")


# Cerrar la conexión
cursor.close()
connection.close() 