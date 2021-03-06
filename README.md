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

### Github

i) La versión de Python que se va a emplear es 3.10.3

ii) Es necesario ejecutar el siguiente comando para instalar las librerías necesarias para la ejecución del proyecto (la ejecución de dicho comando debe realizarse en el directorio que contenga el archivo requirements.txt):

  * pip install -r requirements.txt

iii) Existen dos maneras para descargar el programa mediante Github:

  * Descargar directamente el programa abriendo la pestaña verde Code situada en la parte superior del Github, y posteriormente pulsar en descargar zip
  * Otra opción es lanzar el siguiente comando:
    
    * git clone https://github.com/AIVA2022TeamE/AIVA_2022-ImagenesAereas

iv) El siguiente paso es la ejecución del programa. 

  a) Para ello se debe lanzar el siguiente comando desde el directorio src:

    * python Principal.py --input="input/path" --output="output/path"
  
  b) Si se utiliza un contenedor docker basta con ejecutar el siguiente comando:
  
    * docker build --target src


## Uso del detector
Se ha desarrollado un despliegue fácil en docker. Para hacer uso de la aplicación es necesario contar con un directorio donde tener todas las imágenes que se quieran escanear. También habrá que especificar un directorio de salida. El uso del contenedor es el siguiente:

### Ejecución del contenedor
Detectar una calle dentro de una imágen. En este ejemplo las imágenes estarían en un directorio del host `$DATA_DIR/input/*.tif`. Es importante mencionar que `$DATA_DIR` debe de ser una ruta absoluta. 

```bash
 docker run --gpus all -v $DATA_DIR:/app/data davidcorreas/traffic_detector --input /app/data/input/austin1.tif --output /app/data/output --street_name "Green Forest Dr, austin"
 ```

 Detectar en imágenes de una carpeta
```bash
 docker run --gpus all -v $DATA_DIR:/app/data davidcorreas/traffic_detector --input /app/data/input --output /app/data/output
 ```

 ### Ejecución del contenedor con GPU
 Para hacer uso de la gpu es posible usar `--gpus all` en el comando `docker run` siempre y cuando haya disponible una gpu en el docker host.

## Tests
Se han implementado una serie de tests que prueban el correcto funcionamiento del sistema. 
Gracias a estos se puede definir y acotar la funcionalidad del sistema y sus funciones.

### Ejecución de los tests
Se ha diseñado un `Dockerfile` siguiendo las prácticas de <infrastructure-as-code> donde se encuentran
varios <stages>. Cabe resaltar que se hace uso de <BuildKit> por lo que deberá estar disponible en
la máquina donde se quiera ejecutar. 

Para la ejecución de los test vale con ejecutar el siguiente comando:
```bash
docker build --target test .
```
  
El siguiente comando de `docker` exporta los resultados del test en una página html en el directorio actual. 
```bash
docker build -t test --output results .
```

#### En Local
Si se quiere probar en local hará falta instalarse todos los requisitos y los datos que se encuentran
en la carpeta compartida:
[Datos en Google Drive](https://drive.google.com/drive/folders/1Ey2Gqbc6ZLqrLN8X1DMXFGKI48vYWFrJ?usp=sharing)

Posteriormente habrá que ejecutar el comando:
`python -m unittest test/*`
  

## Contribución
Debido a que el proyecto depende de binarios externos a python desarrollar en este proyecto puede ser una tarea complicada. Por este motivo se ha decidido hacer un entorno de desarrollo basado en <Docker> y que puede ser fácilmente desplegado en el IDE VSCode.

Todos los ficheros necesarios se encuentran en en directorio `.devcontainer` y puede ser desplegado abrindo el proyecto con VSCode > `Ctrl+Shift+P` > Remote-Container: Open Folder In Container 
