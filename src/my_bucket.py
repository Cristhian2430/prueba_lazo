import os
from google.cloud import storage
from google.oauth2 import service_account

import os

class my_storage:
    def __init__(self,nombre_bucket="bucket_escuelas",env="DEV",ruta_credenciales="") -> None:
        print("Loading my storage")
        # Instantiates a client
        self.nombre_bucket =  nombre_bucket # Cambia esto al nombre de tu bucket
        self.env = env
        self.ruta_credenciales = ruta_credenciales
        if self.env=="DEV":
            #current_directory = os.getcwd()
            #print("Directorio actual:", current_directory)
            credentials = service_account.Credentials.from_service_account_file(self.ruta_credenciales)
            self.storage_client = storage.Client(credentials=credentials)
        else:
            self.storage_client = storage.Client()

        self.bucket = self.storage_client.bucket(self.nombre_bucket)

    def save(self,local_csv_file,name):
        # Nombre que le darás al archivo en Google Cloud Storage
        nombre_archivo_gcs = os.path.join("ESCUELA_1/DATA/",name)  # Cambia esto a la ruta deseada
        # Cargar el archivo CSV en el bucket
        blob = self.bucket.blob(nombre_archivo_gcs)

        # Subir el archivo al bucket
        blob.upload_from_filename(local_csv_file)

        print(f"Archivo {local_csv_file} cargado a {nombre_archivo_gcs} en el bucket {self.nombre_bucket}")