#!/usr/bin/python
import time
from flask import Flask, jsonify, abort, make_response, request
import pandas as pd
import matplotlib
import json
#import jsonpickle

matplotlib.use('Agg')

app = Flask(__name__)
#df = None
#url = None

@app.route('/')
def saludo():
	global df
	print("hola")
	return str(df.shape)

# 1. Cargar datos en formato CSV o TSV desde un URL
@app.route('/setSource', methods = ['POST'])
def setSource():
	global url
	global df
	url = request.json.get('url',"")
	c = request.json.get('sep',"\t")
	print("Nuevo url %s separador %s\n"%(url,c))
	df = pd.read_csv(url,sep=c)
	return "OK"

# 2. Consultar el numero de filas y columnas que tienen esos datos
@app.route("/getSize", methods = [ 'GET' ])
def getSize():
        global df
        return str(df.shape)

# 3. Mostrar el nombre de los atributos de los datos
@app.route("/showAttributes", methods = [ 'GET' ])
def showAttributes():
        global df
        return str(df.columns)

# 4. Mostrar el tipo de datos de los atributos
@app.route("/showDataTypes", methods = ['GET'])
def showDataTypes():
        global df
        return str(df.dtypes)

# 5. Agrupacion
@app.route('/calcAggr', methods = ['POST'])
def calcAggr():
        global df
        results = []
        campo1 = request.json.get("field1","")
        campo2 = request.json.get("field2","")
        items = [{
         'field': campo1,
         'mean': df[campo1].mean()
        },
        {
         'field': campo2,
         'mean': df[campo2].mean()
        }
        ]
        results.append(items)
        return jsonify({'results': results}), 201


# 6. Agrupacion y promedio
@app.route('/calcAggregate', methods = ['POST'])
def calcAggregate():
        global df
        results = []
        campo1 = request.json.get("field1","")
        campo2 = request.json.get("field2","")
        media  = df.groupby(campo1)[campo2].mean()
        min = df.groupby(campo1)[campo2].min()
        mediana =df.groupby(campo1)[campo2].median()
        max = df.groupby(campo1)[campo2].max()
        items = [{
         'field1': campo1,
         'field2': campo2,
         'media': media.tolist(),
	 'min' : min.tolist(),
         'mediana' : mediana.tolist(),
         'max' : max.tolist()
        }]
        results.append(items)
#        return jsonify({'results': results, 'a': a}), 200

# TODO: pendiente retornar los arreglos
        return str("ok")


# 7. Grafica
@app.route('/plotFigure', methods = ['POST'])
def plotFigure():
        global df
        first = request.json.get("field1","")
        second = request.json.get("field2","")
        result = df.groupby(first)[second].mean()
        fig = result.plot().get_figure()
        fig.savefig('demo.png')
        return str("ok")

if __name__ == '__main__':
    #df = pd.read_csv('/myhome/gapminder.tsv', sep='\t')
    df = pd.read_csv('/myhome/c6dm-udt9.csv', sep=',')
    app.run(host='0.0.0.0',debug=True)

