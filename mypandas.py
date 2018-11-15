#!/usr/bin/python
#import time
from flask import Flask, jsonify, abort, make_response, request, send_file, send_from_directory
import pandas as pd
import matplotlib
#import json
#import jsonpickle

matplotlib.use('Agg')

app = Flask(__name__)
#df = None
#url = None

# 0. Responder con mensaje de bienvenida
@app.route('/')
def welcome():
	global df
	results=[{'msg' : 'Bienvenido'}]
	return jsonify({'results': results}), 200

# 1. Cargar datos en formato CSV o TSV desde un URL
@app.route('/setSource', methods = ['POST'])
def setSource():
	global url
	global df
	url = request.json.get('url',"")
	sep = request.json.get('sep',"\t")
	df = pd.read_csv(url,sep=sep)
	results = [{
	 'msg' : 'Fuente de datos establecida',
	 'url' : url,
	 'separator' : sep
	}]
	return jsonify({'results': results}), 200

# 2. Consultar el numero de filas y columnas que tienen esos datos
@app.route("/getSize", methods = [ 'GET' ])
def getSize():
        global df
        results = [{
         'msg' : 'Número de filas y columnas obtenidas',
         'shape' : df.shape
        }]
        return jsonify({'results': results}), 200

# 3. Mostrar el nombre de los atributos de los datos
@app.route("/showAttributes", methods = [ 'GET' ])
def showAttributes():
        global df
        results = [{
         'msg' : 'Nombre de atributos obtenidos',
         'columns' : str(df.columns)
        }]
        return jsonify({'results': results}), 200

# 4. Mostrar el tipo de datos de los atributos
@app.route("/showDataTypes", methods = ['GET'])
def showDataTypes():
        global df
        results = [{
         'msg' : 'Tipo de datos obtenidos',
         'columns' : str(df.dtypes)
        }]
        return jsonify({'results': results}), 200

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
        return jsonify({'results': results}), 200

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
         'media': str(media),
	 'min' : str(min),
         'mediana' : str(mediana),
         'max' : str(max)
        }]
        results.append(items)
        return jsonify({'results': results}), 200

# 7. Grafica
@app.route('/plotFigure', methods = ['POST'])
def plotFigure():
        global df
        first = request.json.get("field1","")
        second = request.json.get("field2","")
        result = df.groupby(first)[second].mean()
        fig = result.plot().get_figure()
        fig.savefig('/myhome/demo.png')
        return str("ok")

@app.route('/downloadPlotFigure', methods = ['POST'])
def downloadPlotFigure():
        global df
        first = request.json.get("field1","")
        second = request.json.get("field2","")
        result = df.groupby(first)[second].mean()
        fig = result.plot().get_figure()
        fig.savefig('/myhome/demo.png')
        return send_from_directory('/myhome/','demo.png', as_attachment=True)

if __name__ == '__main__':
    df = pd.read_csv('/myhome/c6dm-udt9.csv', sep=',')
    app.run(host='0.0.0.0',debug=True)
