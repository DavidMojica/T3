import json
from models import Pais, Departamento, Municipio
from django.db import transaction

def load_cities(json_path):
     with open(json_path, 'r') as json_file:
        data = json.load(json_file)
        
        with transaction.atomic():
            for entry in data:
                # Crea o recupera el país
                pais, created = Pais.objects.get_or_create(description=entry['departamento'])

                # Crea el departamento relacionado con el país
                departamento, _ = Departamento.objects.get_or_create(
                    description=entry['departamento'],
                    pertenece_pais=pais
                )

                # Crea los municipios relacionados con el departamento
                for ciudad in entry['ciudades']:
                    Municipio.objects.create(
                        description=ciudad,
                        pertenece_departamento=departamento
                    )
                    
                    
if __name__ == '__main__':
    json_file_path = 'Colombia.json'  # Reemplaza con la ruta de tu archivo JSON
    load_cities(json_file_path)