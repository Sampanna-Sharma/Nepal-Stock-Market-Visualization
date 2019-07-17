from bokeh.models import ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN
from flask import Flask, render_template, request, jsonify
import _pickle as pickle
import pandas as pd
import numpy as np
from flask_cors import CORS


data = pd.read_csv("processed_data.csv")
predict_data = pd.read_csv("data_set_ready_for_training.csv")
predict_data = predict_data.replace([np.inf, -np.inf], np.nan).dropna()
model = pickle.load(open('stock_predictor.obj','rb'))


app = Flask(__name__)
CORS(app)



@app.route('/')
def index():
    from plot import plot
    plt = plot()
    script, div = components(plt)
    return render_template("index.html", script=script, div=div)


@app.route('/data/year', methods = ['GET'])
def data_serve_year():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates

    company_data_year = pd.DataFrame()
    company_data_year = company_data.groupby(company_data['time'].dt.to_period('Y'))['high'].agg(['max'])
    company_data_year.columns = ['high']
    company_data_year['low'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['low'].agg(['min'])
    company_data_year['no_trans'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('Y'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'
    company_data_year.reset_index(inplace = True)
    company_data_year['time2'] = np.array(company_data_year['time'].apply(lambda d: pd.to_datetime(str(d)))).tolist()
    company_data_year['time2'] = company_data_year['time2'].apply(lambda x: x/1000000)
    company_data_year = company_data_year.drop('time',axis = 1)
    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)

@app.route('/data/month', methods = ['GET'])
def data_serve_month():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates

    company_data_year = pd.DataFrame()
    company_data_year = company_data.groupby(company_data['time'].dt.to_period('M'))['high'].agg(['max'])
    company_data_year.columns = ['high']
    company_data_year['low'] = company_data.groupby(company_data['time'].dt.to_period('M'))['low'].agg(['min'])
    company_data_year['no_trans'] = company_data.groupby(company_data['time'].dt.to_period('M'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('M'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('M'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'
    company_data_year.reset_index(inplace = True)
    company_data_year['time2'] = np.array(company_data_year['time'].apply(lambda d: pd.to_datetime(str(d)))).tolist()
    company_data_year['time2'] = company_data_year['time2'].apply(lambda x: x/1000000)
    company_data_year = company_data_year.drop('time',axis = 1)
    
    response = company_data_year.to_dict(orient='list')
 
    return jsonify(response)

@app.route('/data/week', methods = ['GET'])
def data_serve_week():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates

    company_data_year = pd.DataFrame()
    company_data_year = company_data.groupby(company_data['time'].dt.to_period('W'))['high'].agg(['max'])
    company_data_year.columns = ['high']
    company_data_year['low'] = company_data.groupby(company_data['time'].dt.to_period('W'))['low'].agg(['min'])
    company_data_year['no_trans'] = company_data.groupby(company_data['time'].dt.to_period('W'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('W'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('W'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'
    company_data_year.reset_index(inplace = True)
    company_data_year['time2'] = np.array(company_data_year['time'].apply(lambda x: x.to_timestamp())).tolist()
    company_data_year['time2'] = company_data_year['time2'].apply(lambda x: x/1000000)
    company_data_year = company_data_year.drop('time',axis = 1)
    response = company_data_year.to_dict(orient='list')
    
    return jsonify(response)

@app.route('/data/quater', methods = ['GET'])
def data_serve_quater():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    
    dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
    company_data['time'] = dates

    company_data_year = pd.DataFrame()
    company_data_year = company_data.groupby(company_data['time'].dt.to_period('Q'))['high'].agg(['max'])
    company_data_year.columns = ['high']
    company_data_year['low'] = company_data.groupby(company_data['time'].dt.to_period('Q'))['low'].agg(['min'])
    company_data_year['no_trans'] = company_data.groupby(company_data['time'].dt.to_period('Q'))['no_trans'].agg(['sum'])
    company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('Q'))['open'].agg(['first'])
    company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('Q'))['close'].agg(['last'])
    company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
    company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'
    company_data_year.reset_index(inplace = True)
    company_data_year['time2'] = np.array(company_data_year['time'].apply(lambda x: x.to_timestamp())).tolist()
    company_data_year['time2'] = company_data_year['time2'].apply(lambda x: x/1000000)
    company_data_year = company_data_year.drop('time',axis = 1)
    response = company_data_year.to_dict(orient='list')
    
    return jsonify(response)

@app.route('/data/day', methods = ['GET'])
def data_serve_day():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data.loc[data['traded_companies'] == company_name]
    company_data['time2'] = company_data['time']
    
    response = company_data.drop(["traded_companies"],axis = 1).to_dict(orient='list')

    if (company_name == "Nabil Bank Limited"):
        input_data = predict_data[-1:].drop('news',axis = 1)
        u, l = model.predict(input_data, 0)
        response['open'].append(response['close'][-1])
        response['low'].append(response['close'][-1])
        response['close'].append(l[0])
        response['high'].append(l[0])
        response['color'].append('dodgerblue')
        response['time2'].append(1508976000000)
        del(response['open'][0])
        del(response['low'][0])
        del(response['close'][0])
        del(response['high'][0])
        del(response['color'][0])
        del(response['time2'][0])
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug = True)