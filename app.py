from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, Select, HoverTool, DatetimeTickFormatter
from bokeh.layouts import row, column
from bokeh.embed import components
from bokeh.resources import CDN
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.palettes import Category20
from flask_cors import CORS

#palletes
RED = Category20[7][6]
GREEN = Category20[5][4]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]

#Default Data

data = pd.read_csv("stockprice_15_04_2019-25_10_2017.csv")
company_data = data.loc[data['traded_companies'] == 'Nabil Bank Limited']

company_data["date"] = pd.to_datetime(company_data['date'], cache = True)
company_date = np.array(company_data["date"],dtype = np.datetime64).tolist()
c = []
for op,cl in zip(company_data["previous_closing"], company_data["closing_price"]):
    if cl > op:
        c.append(GREEN)
    elif cl< op:
        c.append(RED)
    else:
        c.append(BLUE)


nabil_data = dict(  time = company_date,
                    open = company_data["previous_closing"].to_list(),
                    close = company_data["closing_price"].to_list(),
                    high = company_data["max_price"].to_list(),
                    low = company_data["min_price"].to_list(),
                    color = c)

source = ColumnDataSource(nabil_data)




# widgets
TOOLS = "pan,xwheel_zoom,reset,hover"


app = Flask(__name__)
CORS(app)

def plot():


    p = figure(x_axis_type="datetime",title = "CandleStick",plot_width=1200, plot_height=500,
          tools=TOOLS, active_scroll = 'xwheel_zoom', toolbar_location = "above")

    p.xaxis.formatter = DatetimeTickFormatter(
                                days=["%F"],
                                months=["%F"],
                                years=["%F"],)
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "price"

    p.segment(x0='time', y0='low', x1='time', y1='high', line_width=1, color='black', source=source)
    p.segment(x0='time', y0='open', x1='time', y1='close', line_width=6, color='color', source=source)
    p.line(x='time', y='close', alpha = 0.5, color = ORANGE, source = source)

    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Date", "@time{%F}"),
        ("Open", "@open"),
        ("Close", "@close"),
        ("High", "@high"),
        ("Low", "@low"),
        ]
    hover.formatters={"@time":'datetime',}
    hover.mode = "vline"

    callback = CustomJS(args=dict(source=source), code="""
        var company_name = cb_obj.value
        var data = source.data;
        let xhr  = new XMLHttpRequest();
        var url = "http://localhost:3000/data?company="+company_name.replace(/ /g,"%20")
        xhr.open('GET',url);
        xhr.send();
        response = []
        console.log(url)
        xhr.onload = function(){
            var response = xhr.response;
            response = JSON.parse(response);
            console.log(response)
            
        
        data['color'] = response.color
        data['open'] = response.open
        data['close'] = response.close
        data['high'] = response.high
        data['low'] = response.low
        data['time'] = response.time
        
        source.change.emit();
        console.log("check",data)}
        """)


    #Selection
    option = list(set(data.traded_companies.dropna()))
    Company_select = Select(value="Nabil Bank Limited", options=option)
    Company_select.js_on_change('value', callback)

    layout = column(Company_select, p)
    return layout

@app.route('/')
def index():
	plt = plot()

	script, div = components(plt)
	return render_template("index.html", script=script, div=div)

if __name__ == "__main__":
    app.run(debug = True)