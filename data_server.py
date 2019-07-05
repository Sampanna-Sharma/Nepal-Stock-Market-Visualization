from flask import Flask, jsonify, request
import pandas as pd
import numpy as np
from flask_cors import CORS


data_df = pd.read_csv("stockprice_15_04_2019-25_10_2017.csv")

app = Flask(__name__)
CORS(app)

@app.route('/data', methods = ['GET'])
def data():
    company_name = request.args.get('company')
    print("here",company_name)
    company_data = data_df.loc[data_df['traded_companies'] == company_name]
    company_data["date"] = pd.to_datetime(company_data['date'], cache = True)
    company_date = np.array(company_data["date"],dtype = np.datetime64).tolist()
    company_date = list(map(lambda x: x/1000000,company_date))
    company_close = np.array(company_data["closing_price"]).tolist()
    company_open = np.array(company_data["previous_closing"]).tolist()
    company_diff = np.array(company_data["difference_rs"]).tolist()
    company_high = np.array(company_data["max_price"]).tolist()
    company_low = np.array(company_data["min_price"]).tolist()
 
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
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug= True,port=3000)