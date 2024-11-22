# Seminario 1:  JPEG, JPEG2000, FFMPEG
Este proyecto fue realizado en Google Colab y se centra en la manipulación y compresión de imágenes y videos utilizando diversas técnicas de codificación. A continuación se describe brevemente el contenido y las funcionalidades implementadas.

## Descripción del Proyecto

El proyecto abarca diversas etapas de procesamiento y compresión de imágenes, comenzando con la instalación y configuración de **FFmpeg**, seguido de la implementación de técnicas de conversión de color, compresión, codificación de imágenes y más.

### Funcionalidades Implementadas

1. **Instalación y configuración de FFmpeg**: Instalación de la última versión de FFmpeg y verificación de su funcionamiento en el sistema.
2. **Conversión RGB a YUV y viceversa**: Implementación de una clase en Python para convertir entre los valores RGB y YUV.
3. **Reducción de calidad de imágenes**: Usando FFmpeg, se automatiza la compresión y redimensionado de imágenes.
4. **Lectura serpenteante de archivos JPEG**: Método para leer los bytes de una imagen JPEG en el orden serpenteante.
5. **Compresión extrema y transformación a blanco y negro**: Aplicación de compresión de alta calidad y transformación a escala de grises usando FFmpeg.
6. **Codificación Run-Length**: Implementación de un método para aplicar la codificación de longitud de corrida a una serie de bytes.
7. **Transformada Discreta de Coseno (DCT)**: Creación de una clase que aplica la DCT a los datos de entrada.
8. **Transformada Discreta de Onda (DWT)**: Creación de una clase para realizar la codificación o decodificación utilizando DWT.
9. **Pruebas Unitarias con IA**: Se implementaron pruebas unitarias automatizadas para cada método y clase utilizando IA.

## Mejoras en la Versión Actual

Hemos subido una versión mejorada del código 'first_seminar_OK.ipynb'


## Instrucciones

1. **Instalación de dependencias**: Asegúrate de tener las bibliotecas necesarias instaladas en tu entorno. Utiliza el siguiente comando para instalar FFmpeg:

   ```bash
   sudo apt-get install ffmpeg
2. **Ejecutar el código en Google Colab**: Puedes cargar el script first_seminar.py y ejecutar cada una de las funciones según las instrucciones proporcionadas.

3. **Ejecutar pruebas unitarias**: Asegúrate de ejecutar las pruebas unitarias para verificar el correcto funcionamiento del código. Las pruebas están integradas en el archivo de script.

## Contribuciones
Si deseas contribuir al proyecto, puedes realizar mejoras en las funciones existentes o agregar nuevas técnicas de compresión y codificación. Si tienes alguna sugerencia o duda, no dudes en abrir un "issue" en este repositorio.





# Laboratorio 1: API and Dockerization
Este proyecto cubre la creación de una API básica utilizando FastAPI y su dockerización para permitir su ejecución en cualquier entorno.

## Ejercicio 1: Desarrollo de una API con FastAPI y Docker

### Paso 1: Creación del Proyecto
1. Creamos un nuevo proyecto en PyCharm llamado `practice1` y selecciona un entorno virtual (Python 3.11).
2. Instalamos las dependencias necesarias:
   ```bash
   pip install fastapi uvicorn
   
### Paso 2: Creación de la API con FastAPI
En el archivo `main.py`, creamos la API con una ruta básica:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
```
### Paso 3: Ejecución Local de la API
Ejecutamos la API localmente con Uvicorn:

```bash
uvicorn main:app --reload
```
Accedemos a la API en http://127.0.0.1:8000 y la documentación interactiva en http://127.0.0.1:8000/docs.

### Paso 4: Dockerización de la Aplicación
Creamos el archivo Dockerfile:
```
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Creamos el archivo requirements.txt:
```
fastapi
uvicorn
```
Construimos y ejecutamos el contenedor Docker:
```
docker build -t practice1 .
docker run -d -p 8000:8000 practice1
```
### Paso 5: Verificación en Docker
Accedemos a la API dockerizada en http://127.0.0.1:8000 para verificar su funcionamiento.

## Ejercicio 2: Dockerizar FFmpeg
Creamos un nuevo proyecto llamado ffmpeg-docker y en el archivo Dockerfile agregamos lo siguiente:
```
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ffmpeg
CMD ["ffmpeg", "-version"]
```
Construimos la imagen Docker:
```
docker build -t ffmpeg-container .
```
Ejecutamos el contenedor para verificar la instalación de FFmpeg:
```
docker run --rm ffmpeg-container
```
En Docker Desktop, ya tenemos las dos imágenes que hemos creado:
![image](https://github.com/user-attachments/assets/e6a663b1-5d32-4555-a6bb-f180e8130250)

## Ejercicio 3: Actualización y Pruebas
Añadimos las clases del Seminario 1 al archivo main.py y los unit tests al archivo test_main.py.
Para ejecutar la API, usamos el siguiente comando:
```
uvicorn main:app --reload
```
Para ejecutar los tests, usa:
```
python test_main.py
```
Resultados obtenidos:
![image](https://github.com/user-attachments/assets/ab3cb570-0185-44b1-a4f3-89d25bb1dbe2)

## Ejercicio 4: Añadir Endpoints
Hemos añadido tres nuevos endpoints a la API:

/convert_rgb_to_yuv: Convierte una imagen de formato RGB a YUV.
/convert_yuv_to_rgb: Convierte una imagen de formato YUV a RGB.
/compress_to_bw: Comprime y convierte una imagen a escala de grises (blanco y negro).
Estos tres endpoints están disponibles y accesibles desde la documentación interactiva en http://127.0.0.1:8000/docs.
![unnamed](https://github.com/user-attachments/assets/791cdfb1-28f3-4922-b100-9ee3600898db)
![unnamed (1)](https://github.com/user-attachments/assets/9357d6f4-ee5f-4261-9768-d7bf55b2429c)
![Captura](https://github.com/user-attachments/assets/e96094be-daa0-4de1-b564-34d7bbce2325)


## Contribuciones
Si deseas contribuir al proyecto, puedes realizar mejoras en las funciones existentes o agregar nuevas técnicas de compresión y codificación. Si tienes alguna sugerencia o duda, no dudes en abrir un "issue" en este repositorio.
