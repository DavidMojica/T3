#Paso 1: crear a colombia en la BD: insert into main_pais (id, description) values(0, 'Colombia');
#paso 2: Cambiar la ruta del archivo de colombia.json. Ejemplo: 'C:\\Users\\swan5\\Desktop\\universidad\\projects\\works\\T3\\extras\\Colombia.json'
#paso 3: ejecutar este script
#EJECUTAR DESDE UNA CARPETA APARTE DEL PROYECTO PARA QUE NO HAYA COMPLICACIONES CON EL ENTORNO VIRTUAL.
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
ruta = ''
json_file_path = ruta

# Conectarse a la base de datos
connection = psycopg2.connect(**db_settings)
cursor = connection.cursor()

#Cambia el id del pais conforme su id en la base de datos
id_pais = 0

with open(json_file_path, 'r') as json_file:
    data = json.load(json_file)

# Iterar sobre los datos y guardar en la base de datos
for entry in data:
    id_departamento = entry['id']
    print(id_departamento)
    departamento = entry['departamento']
    print(departamento)
    ciudades = entry['ciudades']

    cursor.execute("INSERT INTO main_departamento (id, description, pertenece_pais_id) VALUES (%s, %s, %s)", (id_departamento, departamento, id_pais))
    for ciudad in ciudades:
        cursor.execute("INSERT INTO main_municipio (description, guardado_por_id, pertenece_departamento_id) VALUES (%s, %s, %s)", (ciudad, None, id_departamento))
        print(ciudad)

    # Insertar datos en la base de datos
    connection.commit()

# Cerrar la conexión
cursor.close()
connection.close() 