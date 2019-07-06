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


if __name__ == "__main__":
    app.run(debug = True)