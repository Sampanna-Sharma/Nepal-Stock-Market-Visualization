from bokeh.plotting import figure
from datetime import date, timedelta
from bokeh.models import ColumnDataSource, CustomJS, Select, HoverTool, DatetimeTickFormatter,\
                         Band,Panel, Tabs, SingleIntervalTicker, PrintfTickFormatter, Range1d, LinearAxis
from bokeh.layouts import row, column
from bokeh.models.widgets import CheckboxGroup, Dropdown
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


TOOLS = "xpan,xwheel_zoom,reset,hover"
data = pd.read_csv("processed_data.csv")
company_data = data.loc[data['traded_companies'] == 'Nabil Bank Limited']

dates = pd.to_datetime(company_data['time'].astype(int), unit = 'ms')
company_data['time'] = dates


company_data_year = company_data.groupby(company_data['time'].dt.to_period('M'))['high'].agg(['max'])
company_data_year['min'] = company_data.groupby(company_data['time'].dt.to_period('M'))['low'].agg(['min'])
company_data_year['no_of_trans'] = company_data.groupby(company_data['time'].dt.to_period('M'))['no_trans'].agg(['sum'])
company_data_year['open'] = company_data.groupby(company_data['time'].dt.to_period('M'))['open'].agg(['first'])
company_data_year['close'] = company_data.groupby(company_data['time'].dt.to_period('M'))['close'].agg(['last'])
company_data_year.loc[company_data_year.close > company_data_year.open, 'color'] = 'green'
company_data_year.loc[company_data_year.close <= company_data_year.open, 'color'] = 'red'


def candle_plot(traded_companies):

    # source = ColumnDataSource(company_data)
    source = ColumnDataSource(company_data_year)

    print('************************************************************')
    # print(source)
    select_plots_checkbox = CheckboxGroup(labels = ['Candle Stick', 'Bollinder Band'], active = [0])
    # print(select_plots_checkbox)
    # print(select_plots_checkbox.active)
    print(source)

    print('************************************************************')


    p = figure(x_axis_type="datetime",title = "CandleStick",plot_width=1200, plot_height=500,
          tools=TOOLS, active_scroll = 'xwheel_zoom', toolbar_location = "above")

    # p.xaxis.formatter = DatetimeTickFormatter(
    #                             days=["%F"],
    #                             months=["%F"],
    #                             years=["%F"],)
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "price"

    # p.segment(x0='time', y0='low', x1='time', y1='high', line_width=1, color='black', source=source)
    p.segment(x0='time', y0='min', x1='time', y1='max', line_width=1, color='black', source=source)
    p.segment(x0='time', y0='open', x1='time', y1='close', line_width=6, color='color', source=source)  #set color = 'color'
    p.line(x='time', y='close', alpha = 0.5, color = ORANGE, source = source)

    #transaction graph
    p.extra_y_ranges["trans"] = Range1d(start=0, end=5000)
    # p.segment(x0='time', y0=0, x1='time', y1='no_trans',y_range_name="trans", line_width=6, color='black', alpha=0.5, source=source, legend = "No. of transactions")
    # p.segment(x0='time', y0=0, x1='time', y1='no_of_trans',y_range_name="trans", line_width=6, color='black', alpha=0.5, source=source, legend = "No. of transactions")



    # p.x_range.start=source.data["time"][-50]
    # p.x_range.end= source.data["time"][-1]
    p.x_range.bounds=(date(2010, 1, 1), date(2019, 12, 31))
    p.x_range.min_interval = timedelta(1)

    
    

    #p.extra_y_ranges["trans"].bounds = "auto"
    p.add_layout(LinearAxis(y_range_name='trans', bounds = (0,1500),axis_label = "No of transaction"), 'right')
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Date", "@time{%F}"),
        ("Open", "@open"),
        ("Close", "@close"),
        ("High", "@max"),
        ("Low", "@min"),
        ]
    hover.formatters={"@time":'datetime',}
    hover.mode = "vline"

   
    #p.yaxis.ticker = SingleIntervalTicker(interval=100, num_minor_ticks=5)
    p.yaxis[0].formatter = PrintfTickFormatter(format="Rs. %3.3f")
    #p.yaxis[0].ticker.desired_num_ticks = 10


    #second plot 
    # commented below this    
    p4 = figure(x_axis_type="datetime",active_scroll = 'xwheel_zoom',title = "Bollinger Band",plot_width=1200, plot_height=500, tools=TOOLS + ', crosshair')
    # p4.line(x='time', y='ma20', color=RED, alpha = 0.6,source=source, legend = "Moving Average :- 20")
    p4.line(x='time', y='close', color='black', line_width = 2,source=source, legend = "closing_price")

    # band = Band(base='time', lower='bband_l', upper='bband_u', source=source, level='underlay',
                    # fill_alpha=0.5, line_width=1, line_color='black', fill_color=BLUE_LIGHT)
    # p4.add_layout(band)

    #commented above this



    #-----------------------------------------------------------------------------------------------------
    # def update_plots(attr, old, new):
    #     if 1 in select_plots_checkbox.active:
    #         p.line(x='time', y='ma20', color=RED, alpha = 0.6,source=source, legend = "Moving Average :- 20")
    #         p.line(x='time', y='close', color='black', line_width = 2,source=source, legend = "closing_price")
    #         p.add_layout(band)
    # select_plots_checkbox.on_change('active', update_plots)

    #-----------------------------------------------------------------------------------------------------


    time_frame = "/week"
    # def dropdown_function(attr, old, new):
    #     time_frame = "/" + dropdown.value
    #     print(time_frame)

    # print("Time frame: ", time_frame)
     
    # dropdown_callback = CustomJS(args=dict(time_frame=time_frame), code = """
    #     console.log('cb_data ', cb_data)
    #     console.log('cb_obj ', cb_obj.value)
    #     console.log('Time frame: ', time_frame)
    # """)



    # menu = [("year", "year"), ("month", "month")]
    # dropdown = Dropdown(label="Select time Scale", button_type="warning", menu=menu)

    # dropdown.js_on_change('value', dropdown_callback)

    # print("Time frame: ", time_frame)

    option = ["Nabil Bank Limited", "Arun Valley Hydropower Development Co. Ltd.",
                "Citizen Bank International Limited", "Bank of Kathmandu Ltd.", "Nepal Bangladesh Bank Limited"]
    menu = [("year", "year"), ("month", "month"), ("week","week"), ("day","day")]


    Company_select = Select(value="Nabil Bank Limited", options=option)
    timeframe_dropdown = Dropdown(value = 'month', label="Select time Scale", button_type="warning", menu=menu)


    callback = CustomJS(args=dict(source=source,p=p,p4=p4,company_select=Company_select, timeframe_dropdown=timeframe_dropdown, time_frame =time_frame), code="""
        time_frame = "/" + timeframe_dropdown.value
        var company_name = company_select.value
        var timeframe_list = ['year','month', 'week', 'day']
        if (timeframe_list.includes(cb_obj.value)){
            time_frame = "/" + cb_obj.value
        }
        else{
            company_name = cb_obj.value
        }
        console.log('Company name: ' , company_name)
        var data = source.data;
        let xhr  = new XMLHttpRequest();
        var url = `http://localhost:5000/data${time_frame}?company=`+company_name.replace(/ /g,"%20")
        xhr.open('GET',url);
        xhr.send();
        response = []
        console.log('******************************************')
        //console.log(time_frame)
        console.log(url)
        //console.log('cb obj : ', cb_obj)
        //console.log('cb_data: ', cb_data)
        console.log('******************************************')
        xhr.onload = function(){
            var response = xhr.response;
            //console.log(response)

            response = JSON.parse(response);
            
        for (key in response) {
            data[key] = response[key];
            }
        
        console.log('Source: ', response)        

        source.change.emit()
        p.reset.emit()
        p4.reset.emit();}
        """)


    #Selection
    
    





    # callback for dropdown of timeframe(below)

    # dropdown_callback = CustomJS(args=dict(source=source,p=p,p4=p4,company_select=Company_select, time_frame =time_frame), code="""
    #     console.log('Company Select: ', company_select.value)
    #     time_frame = "/" + cb_obj.value
    #     var company_name = company_select.value
    #     var data = source.data;
    #     let xhr  = new XMLHttpRequest();
    #     var url = `http://localhost:5000/data${time_frame}?company=`+company_name.replace(/ /g,"%20")
    #     xhr.open('GET',url);
    #     xhr.send();
    #     response = []
    #     console.log('******************************************')
    #     //console.log(time_frame)
    #     //console.log(url)
    #     //console.log('cb obj : ', cb_obj.value)
    #     //console.log('cb_data: ', cb_data)
    #     console.log('******************************************')
    #     xhr.onload = function(){
    #         var response = xhr.response;
    #         //console.log(response)

    #         response = JSON.parse(response);
            
    #     for (key in response) {
    #         data[key] = response[key];
    #         }
        
    #     console.log('Source: ', source)        

    #     source.change.emit()
    #     p.reset.emit()
    #     p4.reset.emit();}
    #     """)


    
    Company_select.js_on_change('value', callback)
    timeframe_dropdown.js_on_change('value', callback)



   


    tab1 = Panel(child=p, title="candle stick")
    tab2 = Panel(child=p4, title="bollinder")

    tabs = Tabs(tabs=[ tab1, tab2 ])

    layout = column(Company_select,tabs,timeframe_dropdown)

    return layout