from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS, Select, HoverTool, DatetimeTickFormatter, Band,Panel, Tabs
from bokeh.layouts import row, column
import pandas as pd
import numpy as np
from bokeh.palettes import Category20
#palletes
RED = Category20[7][6]
GREEN = Category20[5][4]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]


TOOLS = "pan,xwheel_zoom,reset,hover"
data = pd.read_csv("processed_data.csv")
company_data = data.loc[data['traded_companies'] == 'Nabil Bank Limited']




def candle_plot(traded_companies):

    source = ColumnDataSource(company_data)

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

    p.x_range.follow = "end"
    #p.x_range.follow_interval = 10

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





    #second plot    
    p4 = figure(x_axis_type="datetime",active_scroll = 'xwheel_zoom',title = "Bollinger Band",plot_width=1200, plot_height=500, tools=TOOLS+ ',crosshair')
    p4.line(x='time', y='ma20', color=RED, alpha = 0.6,source=source, legend = "Moving Average :- 20")
    p4.line(x='time', y='close', color='black', line_width = 2,source=source, legend = "closing_price")

    band = Band(base='time', lower='bband_l', upper='bband_u', source=source, level='underlay',
                    fill_alpha=0.5, line_width=1, line_color='black', fill_color=BLUE_LIGHT)
    p4.add_layout(band)

    callback = CustomJS(args=dict(source=source,p=p,p4=p4), code="""
        var company_name = cb_obj.value
        var data = source.data;
        let xhr  = new XMLHttpRequest();
        var url = "http://localhost:5000/data?company="+company_name.replace(/ /g,"%20")
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
        data['ma20'] = response.ma20
        data['ma50'] = response.ma50
        data['mad'] = response.mad
        data['std20'] = response.std20
        data['bband_u'] = response.bband_u
        data['bband_l'] = response.bband_l
        source.change.emit()
        p.reset.emit()
        p4.reset.emit();}
        """)
    #Selection
    option = ["Nabil Bank Limited", "Bank of Asia Nepal Limited", "Arun Valley Hydropower Development Co. Ltd.",
                "Citizen Bank International Limited", "Bank of Kathmandu Ltd.", "Nepal Bangladesh Bank Limited"]
    Company_select = Select(value="Nabil Bank Limited", options=option)
    Company_select.js_on_change('value', callback)
    tab1 = Panel(child=p, title="candle stick")
    tab2 = Panel(child=p4, title="bollinder")

    tabs = Tabs(tabs=[ tab1, tab2 ])

    layout = column(Company_select,tabs)

    return layout