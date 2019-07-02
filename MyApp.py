import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_notebook, output_file, save
from bokeh.models import ColumnDataSource, Range1d, HoverTool
from bokeh.models.widgets import Select
from bokeh.layouts import row, column,  gridplot, layout
from bokeh.plotting import curdoc, figure
from bokeh.driving import count

data = pd.read_csv("stockprice_15_04_2019-25_10_2017.csv")

source = ColumnDataSource(dict(
    time=[], low=[], high=[], open=[], close=[]
    , color=[], mad = [], ma20 = [], ma50 = []
))

TOOLS = "pan,wheel_zoom,reset,hover"

p = figure(x_axis_type="datetime",title = "CandleStick",plot_width=1200, plot_height=500,
          tools=TOOLS, active_scroll = 'wheel_zoom', toolbar_location = "above")

p.xaxis.axis_label = "date"
p.yaxis.axis_label = "price"

p.segment(x0='time', y0='low', x1='time', y1='high', line_width=1, color='black', source=source)
p.segment(x0='time', y0='open', x1='time', y1='close', line_width=6, color='color', source=source)
p.line(x='time', y='close', alpha = 0.5, color = 'orange', source = source)


p2 = figure(x_axis_type="datetime",title = "Moving Average",plot_height=250,plot_width = 1700, x_range=p.x_range, tools=TOOLS)
p2.xaxis.axis_label = "date"
p2.yaxis.axis_label = "Avg_price"
p2.line(x='time', y='ma50', color='red', source=source, legend = "Moving Average :- 50")
p2.line(x='time', y='ma20', color='blue', source=source, legend = "Moving Average :- 20")

p3 = figure(x_axis_type="datetime",title = "Moving Average Difference",plot_height=500, plot_width = 500, x_range=p.x_range, tools=TOOLS)
p3.segment(x0='time', y0=0, x1='time', y1='mad', line_width=6, color='black', alpha=0.5, source=source)

option = list(set(data.traded_companies.dropna()))
Company = Select(value="Nabil Bank Limited", options=option)


#for hover info

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


def update(attr, old, new):

    company_data = data.loc[data['traded_companies'] == Company.value]
    company_data["date"] = pd.to_datetime(company_data['date'], cache = True)
    company_date = np.array(company_data["date"],dtype = np.datetime64)
    company_close = np.array(company_data["closing_price"])
    company_open = np.array(company_data["previous_closing"])
    company_high = np.array(company_data["max_price"])
    company_low = np.array(company_data["min_price"])

    c = []
    for op,cl in zip(company_open, company_close):
        if cl > op:
            c.append('green')
        elif cl< op:
            c.append('red')
        else:
            c.append('blue')

    
    source.data['open'] = company_open
    source.data['close'] = company_close
    source.data['high'] = company_high
    source.data['low'] = company_low
    source.data['time'] = company_date
    source.data['color'] = c
    source.data['ma20'] = company_data['closing_price'].rolling(20).mean().to_numpy()
    source.data['ma50'] = company_data['closing_price'].rolling(50).mean().to_numpy()
    source.data['mad'] = source.data['ma20'] - source.data['ma50']

    x_min = company_date.max()  - pd.Timedelta(days=20)
    x_max = company_date.max() + pd.Timedelta(days=1)
    y_max = company_close[-20:].max() + 10
    y_min = company_close[-20:].min() - 10
    
    p.x_range.start =  x_min
    p.x_range.end =  x_max

    p.y_range.start =  y_min
    p.y_range.end =  y_max


    
    


update(None, None, None)


Company.on_change("value",update)
curdoc().add_root(column(Company, row(p,p3), p2))
curdoc().title = "OHLC"
