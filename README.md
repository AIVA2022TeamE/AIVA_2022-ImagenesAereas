# AIVA_2022-ImagenesAereas
Repositorio para la práctica de la asignatura aplicaciones industriales y comerciales consistente en el reconocimiento de imágenes aéreas

El objetivo de este producto es desarrollar el sistema TrafficDetector, que es capaz de contar los vehículos que aparecen en una imagen. Dada una imagen aérea, se podrá visualizar un mapa de calor del flujo del tráfico.
También es posible introducir el nombre de una calle y de esta manera obtener el número de vehículos que aparecen en esa calle concreta, siempre que la calle aparezca en la imagen.
Las imágenes con las que se trabaja tienen esta apariencia:

<p>
  <img src="./images/austin1.jpg" alt=""> </p>

Este es un posible caso de uso de la aplicación:

<p>
  <img src="./images/UseCaseDiagram3.svg" alt=""> </p>

Este repositorio cuenta con:
* Un directorio ```documents``` donde se pueden ver los documentos que hemos desarrollado para este proyecto.
* Un directorio ```test``` donde se encuentran los tests automáticos que utilizaremos para comprobar que el sistema realiza sus funciones correctamente.

## Instalación de TrafficDetector

### Opción 1: Github

i) La versión de Python que se va a emplear es 3.10.3

ii) Es necesario ejecutar el siguiente comando para instalar las librerías necesarias para la ejecución del proyecto (la ejecución de dicho comando debe realizarse en el directorio que contenga el archivo requirements.txt).

  * pip install -r requirements.txt

iii) Existen dos maneras para descargar el programa mediante Github:

  * Descargar directamente el programa abriendo la pestaña verde Code situada en la parte superior del Github, y posteriormente pulsar en descargar zip
  * Otra opción es lanzar el siguiente comando:  
    * git clone https://github.com/AIVA2022TeamE/AIVA_2022-ImagenesAereas

iv) El siguiente paso es la ejecución del programa. Para ello se debe lanzar el siguiente comando desde el directorio src:

  * python Principal.py --input="input/path" --output="output/path"

### Opción 2: Docker



## Tests
Se han implementado una serie de tests que prueban el correcto funcionamiento del sistema. 
Gracias a estos se puede definir y acotar la funcionalidad del sistema y sus funciones.

### Ejecución de los tests
Se ha diseñado un `Dockerfile` siguiendo las prácticas de <infrastructure-as-code> donde se encuentran
varios <stages>. Cabe resaltar que se hace uso de <BuildKit> por lo que deberá estar disponible en
la máquina donde se quiera ejecutar. 

Para la ejecución de los test vale con ejecutar el siguiente comando:
`docker build --target test .`

#### En Local
Si se quiere probar en local hará falta instalarse todos los requisitos y los datos que se encuentran
en la carpeta compartida:
[Datos en Google Drive](https://drive.google.com/drive/folders/1Ey2Gqbc6ZLqrLN8X1DMXFGKI48vYWFrJ?usp=sharing)

Posteriormente habrá que ejecutar el comando:
`python -m unittest test/*`
