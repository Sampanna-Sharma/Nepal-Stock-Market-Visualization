from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN
from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np
from flask_cors import CORS
from plot import candle_plot


data = pd.read_csv("processed_data.csv")

app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
	plt = candle_plot(data.traded_companies.dropna())

	script, div = components(plt)
	return render_template("index.html", script=script, div=div)

@app.route('/data', methods = ['GET'])
def data_serve():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    response = company_data.drop(["traded_companies"],axis = 1).to_dict(orient='list')
 
    return jsonify(response)


@app.route('/data/year', methods = ['GET'])
def data_serve_year():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates


    company_data_year = company_data.groupby(company_data['time'].dt.to_period('Y'))['high'].agg(['max'])
    company_data_year['min'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['low'].agg(['min'])
    company_data_year['no_of_trans'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'

    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)

@app.route('/data/month', methods = ['GET'])
def data_serve_month():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates


    company_data_year = company_data.groupby(company_data['time'].dt.to_period('M'))['high'].agg(['max'])
    company_data_year['min'] = company_data.groupby(company_data['time'].dt.to_period('M'))['low'].agg(['min'])
    company_data_year['no_of_trans'] = company_data.groupby(company_data['time'].dt.to_period('M'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('M'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('M'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'

    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)

@app.route('/data/week', methods = ['GET'])
def data_serve_week():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates


    company_data_year = company_data.groupby(company_data['time'].dt.to_period('W'))['high'].agg(['max'])
    company_data_year['min'] = company_data.groupby(company_data['time'].dt.to_period('W'))['low'].agg(['min'])
    company_data_year['no_of_trans'] = company_data.groupby(company_data['time'].dt.to_period('W'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('W'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('W'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'

    print("*******************************************************")
    print(company_data_year.head())
    print("*******************************************************")
    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)

@app.route('/data/day', methods = ['GET'])
def data_serve_day():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates


    company_data_year = company_data.groupby(company_data['time'].dt.to_period('D'))['high'].agg(['max'])
    company_data_year['min'] = company_data.groupby(company_data['time'].dt.to_period('D'))['low'].agg(['min'])
    company_data_year['no_of_trans'] = company_data.groupby(company_data['time'].dt.to_period('D'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('D'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('D'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'

    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug = True)