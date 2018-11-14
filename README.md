# Proyecto Final 

## Introduccion

Durante el curso de *Cloud Computing* vimos varios conceptos, temas y tecnologias que nos permiten hoy desarrollar *web services* que pueden procesar datos en la nube de Amazon.

Los objetivos de este proyecto son:

* Poner en practica lo visto en clase relativo a Linux y linea de comandos, virtualizacion con contenedores, Pandas y uso de Amazon EC2 Beanstalk.
* Despliegue de un *web service* en la nube de Amazon en el cual se pueda procesar datos que se encuentran disponibles en Internet.

A continuacion se describen las secciones de las que consta el presente documento:

* [Metas del proyecto](#metas-del-proyecto)
* [Como lograr lo planteado](#como-lograr-lo-planteado)
* [Contenedor con Flask](#contenedor-con-flask)
* [Pandas en contenedores](#pandas-en-contenedores)
* [Publicacion de los *web services* en Amazon Beanstalk](#publicacion-de-los-web-services-en-amazon-beanstalk)
* [Entregables](#entregables)



## Metas del proyecto

El objetivo del proyecto es que usted pueda procesar/analizar en un *web service* datos que se encuentren accesibles a traves de Internet.

Las tareas que debe lograr desarrollar su aplicativo basado en *web services* es:

* Cargar datos en formato CSV o TSV desde un URL
* Consultar el numero de filas y columnas que tienen esos datos
* Mostrar el nombre de los atributos de los datos
* Mostrar el tipo de datos de los atributos
* Se debe permitir calcular funciones de agregacion (media, mediana, mayor, menor) sobre al menos un dato. Dos o mas datos a la vez sera un **plus**. Es decir, si usted tiene unos datos que tienen por ejemplo: edad, salario, nombre, anno de nacimiento; el *web service* deberia permitir el calcular (en una sola invocacion) o la edad promedio o la edad promedio y el salario promedio.
* Un *web service* deberia permitir la agrupacion de datos y con los datos agrupados aplicar una funcion de agregacion. Por ejemplo, el *web service* deberia permitir agrupar los datos por annos y sacar el promedio de salario. Se debera permitir hacer agrupacion de al menos un dato. Dos o mas datos por agrupacion sera un **plus**.
* **BONUS** desarrollar un *web service* que entregue una grafica dados un par de datos. Ejemplo, dado un conjunto de datos que tiene una poblacion, agrupar los datos por anno y a cada anno calcular el ingreso salarial promedio.

## Como lograr lo planteado

Para lograr lo planteado usted necesita de un entorno donde desarrollar su *web service*.
Al final del curso se uso Docker como herramienta para la creacion de entornos de virtualizacion. Para los entornos de *web services* se uso Flask y para el procesamiento de los datos se estudio la herramienta Pandas.

# Obteniendo los contenedores 

## Contenedor con Flask

Para llevar a cabo la consolidacion del entorno de Desarrollo y Despliegue, usted hara uso de contenedores de Docker. 
Durante la clase se llevo a cabo la creacion de varios de estos contenedores. 

Para llevar a cabo en particular este proyecto usted necesita de un contenedor que tenga desplegado, Flask y Pandas.
En la clase se hizo el despliegue de ambos contenedores. 
Para el caso de Flask en la clase se presento la herramienta a traves del desarrollo de una aplicacion basada en *web services* y que implementa una funcionalidad basica del metodo [*Getting Things Done*](https://en.wikipedia.org/wiki/Getting_Things_Done).
Esta aplicacion se encuentra disponible en [Github](https://github.com/josanabr/dockerflask2018/tree/step6).

## Pandas en contenedores

[Pandas](https://pandas.pydata.org/) es una libreria en Python que integra diferentes herramientas para el analisis de datos. 

Durante la clase tambien se desarrollo un contenedor que contenia la funcionalidad de [Pandas](https://github.com/josanabr/pandas).
Este contenedor se caracteriza porque hereda del contenedor que se indico en la [seccion anterior](#contenedor-con-flask).

Durante la clase se hizo un recorrido por Pandas y se trabajo con estos [slides](https://docs.google.com/presentation/d/1pUp34lXHW8vqzV4xkk12ENSX3YpsipdeV7xPwQAgwyI/edit?usp=sharing).

Con los conocimientos de Pandas y lo estudiado en Flask se desarrollo un aplicativo basado en *web services* y donde se hacia el analisis de datos de archivos disponibles en la red.
El aplicativo esta disponible [aqui](mypandas.py).
El aplicativo se puede ejecutar en el contenedor que esta disponible en [este repositorio](https://github.com/josanabr/pandas) de la siguiente forma:

```
docker run --rm -d -p 5000:5000 -v $(pwd):/myhome josanabr/pandas python3 /myhome/mypandas.py
```

**Nota** para ejecutar este contenedor de forma adecuada se requiere que el archivo [gapminder.tsv](gapminder.tsv) se encuentre disponible en el directorio donde se ejecuta el contenedor.

Al ejecutar este contenedor, estos son algunos de los URIs que se encuentran disponibles:

* [/](http://localhost:5000/) entrega el numero de filas y columnas que tiene el *dataframe* que contiene los datos
```
curl -i http://localhost:5000
```
* [/calcularmedia](http://localhost:5000/calcularmedia) este URI permite calcular la media de una columna de los datos en el *dataframe*. 
El acceso a este *end-point* se hace a traves del metodo POST de la siguiente manera.
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "campo": "pop"}' http://localhost:5000/calcularmedia
```
* [/encabezado](http://localhost:5000/encabezado) este URI permite ver los nombres de los atributos del *dataframe*.
```
curl -i http://localhost:5000/encabezado
```
* [/imprimirtipos](http://localhost:5000/imprimirtipos) este URI permite conocer el tipo de los datos de los atributos del *dataframe*.
```
curl -i http://localhost:5000/imprimirtipos
```
* [/seturl](http://localhost:5000/seturl) este URI permite acceder a un archivo CSV o TSV que se encuentre accesible a traves de Internet
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "url": "https://raw.githubusercontent.com/jennybc/gapminder/master/inst/extdata/gapminder.tsv", "sep": "\t"}' http://localhost:5000/seturl
```

## Publicacion de los *web services* en Amazon Beanstalk

Para llevar a cabo la publicacion de este aplicativo en Amazon Beanstalk se creo el [siguiente video](https://www.youtube.com/watch?v=UzrRMandFt0&feature=youtu.be).
En este [enlace](https://docs.google.com/presentation/d/172ayhs3Bfp32ivxpE6PjMCsbTVwQlrvBDcof4iYFWzE/edit?usp=sharing) se presentan unos slides que pueden servir de guia para saber con que se debe contar para poder desplegar un contenedor en Amazon Elastic Beanstalk y hacerlo accesible via *web services*

[Aqui](Dockerrun.aws.json) usted puede encontrar un archivo JSON que sigue la estructura requerida por Amazon para desplegar un contenedor en Amazon Beanstalk.

## Entregables

Para este proyecto se deben entregar dos productos

* Un video en youtube donde se muestre su proyecto en ejecucion y accesible en Amazon Beanstalk
* Un repositorio en Github donde se encuentra todo el codigo de su aplicativo. 
Este repositorio debe contar un README.md que explique que hace su codigo y como se puede acceder a traves de la linea de comandos usando el programa `curl`.

Lo que debe hacer su aplicativo se encuentra descrito en la seccion [Metas del proyecto](#metas-del-proyecto).
