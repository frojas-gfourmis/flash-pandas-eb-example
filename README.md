# Ejemplo de Flask y Pandas en AWS Elastic Beanstalk
En el presente proyecto presentamos el uso *Flask* y *Pandas* en un contenedor *Docker* que se ejecutará en el servicio de AWS denominadno *Elastic Beanstalk*. El servicio web expuesto permite procesar datos de un archivo en formato .csv.

# Imagen y contenedor

## Construir imagen
```
docker build -t gfourmis/flask-pandas:1.1 .
```

## Ejecutar contenedor
```
docker run --rm -d -p 5000:5000 gfourmis/flask-pandas:1.1
```

## Actualizar imagen de docker a partir del contenedor actual
```
docker login
docker commit container_id gfourmis/flask-pandas:1.1
docker tag gfourmis/flask-pandas:1.1 gfourmis/flask-pandas:1.1
docker push gfourmis/flask-pandas:1.1
```

# Servicio web

Las funcionalidades provistas por el servicio web son:

* Cargar datos en formato CSV o TSV desde un URL
* Consultar el numero de filas y columnas que tienen esos datos
* Mostrar el nombre de los atributos de los datos
* Mostrar el tipo de datos de los atributos
* Agrupacion
* Agrupacion y agregación
* Graficación

## Obtener mensaje de bienvenida
```
curl -i http://localhost:5000
```

### Cargar datos en formato CSV o TSV desde un URL
 ```
curl -i -H "Content-Type: application/json" -X POST -d '{ "url": "https://www.datos.gov.co/resource/c6dm-udt9.csv", "sep": ","}' http://localhost:5000/setSource
```
### Consultar el numero de filas y columnas que tienen esos datos
```
curl -i http://localhost:5000/getSize
```

### Mostrar el nombre de los atributos de los datos
```
curl -i http://localhost:5000/showAttributes
```
### Mostrar el tipo de datos de los atributos
```
curl -i http://localhost:5000/showDataTypes
```
### Agrupacion
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "field1": "cuantia_contrato", "field2": "plazo_de_ejec_del_contrato"}' http://localhost:5000/calcAggr
```
### Agrupacion y agregación
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "field1": "anno_cargue_secop", "field2": "plazo_de_ejec_del_contrato"}' http://localhost:5000/calcAggregate
```
### Graficación
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "field1": "anno_cargue_secop", "field2": "plazo_de_ejec_del_contrato"}' http://localhost:5000/plotFigure
```
```
curl -i -H "Content-Type: application/json" -X POST -d '{ "field1": "anno_cargue_secop", "field2": "plazo_de_ejec_del_contrato"}' http://localhost:5000/downloadPlotFigure
```

## Detener contenedor
```
docker stop container_id
```

## Recursos

* [Video: Ejecución de contenedor Docker en AWS Elastic Beanstalk](https://youtu.be/OWG4yJlmL2A)
* [Video: Ejecución de contenedor Docker en local - Flask + Pandas](https://youtu.be/DMJqFnSn8Ps)
* [Video: Actualización de repositorio en GitHub y Docker - Flask + Pandas](https://youtu.be/DKwpua179TQ)
* [Imagen docker: Flask + Pandas](https://hub.docker.com/r/gfourmis/flask-pandas/)
