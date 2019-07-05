from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN
from flask import Flask, render_template, request, jsonify

import pandas as pd
import numpy as np
from flask_cors import CORS
from plot import candle_plot


data = pd.read_csv("stockprice_15_04_2019-25_10_2017.csv")




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
    company_data["date"] = pd.to_datetime(company_data['date'], cache = True)
    company_date = np.array(company_data["date"],dtype = np.datetime64).tolist()
    company_date = list(map(lambda x: x/1000000,company_date))
    company_close = np.array(company_data["closing_price"]).tolist()
    company_open = np.array(company_data["previous_closing"]).tolist()
    company_diff = np.array(company_data["difference_rs"]).tolist()
    company_high = np.array(company_data["max_price"]).tolist()
    company_low = np.array(company_data["min_price"]).tolist()

    company_ma20 = company_data['closing_price'].rolling(20).mean().fillna(0).to_numpy()
    company_ma50 = company_data['closing_price'].rolling(50).mean().fillna(0).to_numpy()
    company_std20 = company_data['closing_price'].rolling(20).std().fillna(0).to_numpy()
    company_mad = (company_ma20 - company_ma50).tolist()
    company_bband_u = (company_ma20 + 2 * company_std20).tolist()
    company_bband_l = (company_ma20 - 2 * company_std20).tolist()
 
    c = []
    for op,cl in zip(company_open, company_close):
        if cl > op:
            c.append("green")
        elif cl< op:
            c.append("red")
        else:
            c.append("blue")

    response = {
            'color' : c,
            'time' : company_date,
            'open' : company_open,
            'close' : company_close,
            'high' : company_high,
            'low' : company_low,
            'ma20' : company_ma20.tolist(),
            'ma50' : company_ma50.tolist(),
            'mad' : company_mad,
            'std20': company_std20.tolist(),
            'bband_u' : company_bband_u,
            'bband_l' : company_bband_l,
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug = True)