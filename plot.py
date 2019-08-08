from bokeh.plotting import figure
from datetime import date, timedelta
from bokeh.models import ColumnDataSource, CustomJS, HoverTool, DatetimeTickFormatter,\
                         Band,Panel, Tabs, SingleIntervalTicker, PrintfTickFormatter, Range1d, LinearAxis \
                        ,CrosshairTool, Span, TapTool, Dropdown, OpenURL
from bokeh.models.widgets import CheckboxButtonGroup, Select, DataTable, TableColumn, Div

from bokeh.layouts import row, column
from bokeh.themes import built_in_themes
from bokeh.io import curdoc
# from bokeh.themes import built_in_themes

import pandas as pd
import numpy as np
from bokeh.palettes import Category20
from bokeh.events import DoubleTap

import requests
import json
#palletes
RED = Category20[7][6]
RED_LIGHT = Category20[8][7]

GREEN = Category20[5][4]
GREEN_LIGHT = Category20[10][5]

BLUE = Category20[3][0]
BLUE_LIGHT = Category20[3][1]

ORANGE = Category20[3][2]
PURPLE = Category20[9][8]
BROWN = Category20[11][10]
time_frame = "/week"

TOOLS = "pan,xwheel_zoom,ywheel_zoom,reset,hover"
url = "http://127.0.0.1:5000/data/day?company=Nabil%20Bank%20Limited"
r = requests.get(url)
company_data = json.loads(r.text)
source = ColumnDataSource(company_data)

print('*******************************************')
# news_data_to_list = open('news_new.txt', 'r')
# news_data_to_list = list(news_data_to_list)
# news_data_to_list = news_data_to_list[:50]
# print(news_data_to_list)

nabil_news = pd.read_csv('nabil.csv')
nabil_news_list = list(nabil_news['news'])
nabil_news_list = nabil_news_list[:10]
print('*******************************************')


#######################
axes_data = {
    'x_min':date(2017, 9,24),
    'x_max':date(2017, 11,15),
    'y_min':min(source.data['open'][-2],source.data['close'][-2]) - 100, 
    'y_max':max(source.data['open'][-2],source.data['close'][-2]) + 100
}

########################

def plot():
    # curdoc().theme = 'dark_minimal'
    list_of_news = news_list()

    candle = candle_plot()

    #bullinder band
    bullinder = bullinder_band()
    candle.add_layout(bullinder)

    #transaction plot
    transac_plot = transaction_plot()
    transac_plot.x_range = candle.x_range

    #moving average plot
    MA_plot = movingavg_plot()
    MA_plot.x_range = candle.x_range

    #RSI plot
    rsi_plt = rsi_plot()
    rsi_plt.x_range = candle.x_range

    #MACD plot
    macd_plt = macd_plot()
    macd_plt.x_range = candle.x_range

    #Support line
    support = Span( dimension='width', line_color=BLUE,
                    line_dash='solid', line_width=2)
    support.visible = False
    candle.add_layout(support)

    #Resistance line
    resistance = Span( dimension='width', line_color=GREEN,
                    line_dash='solid', line_width=2)
    resistance.visible = False
    candle.add_layout(resistance)
    

    #linking crosshairs among figures
    add_vlinked_crosshairs(candle, transac_plot, MA_plot, rsi_plt, macd_plt)

    option = ["Nabil Bank Limited", "Arun Valley Hydropower Development Co. Ltd.",
                "Citizen Bank International Limited", "Bank of Kathmandu Ltd.", "Nepal Bangladesh Bank Limited"]
    menu = ["day","week", "month","quater", "year"]
    timeframe_dropdown = Select(title = 'Set Interval',value = 'day', options=menu)

   #Company Selections
    Company_select = Select(title = 'Company:',value="Nabil Bank Limited", options=option)

    #checkboxes
    checkbox_button_group = CheckboxButtonGroup(
        labels=["Bullinder Band", "Support & Resistance"])
    #Tap callback
    callback_tap = CustomJS(args=dict(button = checkbox_button_group,
                            supp=support,resis = resistance), code="""
        
        if (button.active.includes(1)){
            if (!resis.visible && !supp.visible){
            resis.location = cb_obj.y
            resis.visible = true}

            else if(!supp.visible){
                supp.location = cb_obj.y
                supp.visible = true
            }
            
       }
        else{supp.visible = false}
    """)


    #Radio_option
    callback_radio = CustomJS(args=dict(p=bullinder,supp=support,resis = resistance), code="""
        if (cb_obj.active.includes(0)){
            p.visible = true}
        else{ p.visible = false}

        if (cb_obj.active.includes(1) == false){
            resis.visible = false
            supp.visible = false
        }
    """)
     #Selection
    callback_select = CustomJS(args=dict(source=source,p=candle, list_of_news = list_of_news,x_range=candle.x_range, y_range = candle.y_range,company_select=Company_select, 
                                timeframe_dropdown=timeframe_dropdown), 
    code="""
    timeframe_dropdown.value = "day"
    var company_name = company_select.value
    
    var data = source.data;

    let xhr  = new XMLHttpRequest();
    var url = `http://localhost:5000/data/day?company=`+company_name.replace(/ /g,"%20")
    xhr.open('GET',url);
    xhr.send();
    response = []
    console.log(url)
    xhr.onload = function(){
        var response = xhr.response;
        response = JSON.parse(response);
        console.log(response)
        
    for (key in response) {
        data[key] = response[key];
        }

    
    source.change.emit()
    p.reset.emit()
    list_of_news.change.emit()
    
    var start = data['close'][data['close'].length -1] 
    var end = data['close'][data['close'].length -1] 

    for(var i =data['close'].length -50;i<=data['close'].length-1;i++)
    {
        if (start>data['close'][i])
        {
            start = data['close'][i]
        }
        if (end<data['close'][i])
        {
            end = data['close'][i]
        }
    }
    
    y_range.setv({"start": start-50, "end": end+50})

    var xstart = data['time'][data['time'].length-50] 
    var xstop = data['time'][data['time'].length-1]
    x_range.setv({"start":xstart, "end":xstop})

   
    
    if (timeframe_dropdown == '/month' || timeframe_dropdown == '/quater' || timeframe_dropdown == '/year'){
        xstart = data['time'][0] 
        xstop = data['time'][data['time'].length-1]
        x_range.setv({"start":xstart, "end":xstop})

        for(var i =0;i<=data['close'].length-1;i++)
        {
        if (start>data['close'][i])
        {
            start = data['close'][i]
        }
        if (end<data['close'][i])
        {
            end = data['close'][i]
        }
        }
        y_range.setv({"start": start-300, "end": end+300})
        }
        
    
    console.log(p)

    x_range.change.emit()
    y_range.change.emit()
    
        }
    """)

    callback_dropdown = CustomJS(args=dict(source=source,p=candle,company_select=Company_select, 
                                timeframe_dropdown=timeframe_dropdown, time_frame =time_frame,
                                x_range = candle.x_range, y_range = candle.y_range,ma_plt = MA_plot), 
    code="""
    time_frame = "/" + timeframe_dropdown.value
    var company_name = company_select.value
    var timeframe_list = ['year','month', 'week', 'day', 'quater']
    if (timeframe_list.includes(cb_obj.value)){
        time_frame = "/" + cb_obj.value
    }
    
    console.log('Company name: ' , company_name)
    var data = source.data;
    let xhr  = new XMLHttpRequest();
    var url = `http://localhost:5000/data${time_frame}?company=`+company_name.replace(/ /g,"%20")
    xhr.open('GET',url);
    xhr.send();
    response = []
    console.log(url)
    xhr.onload = function(){
        var response = xhr.response;
        response = JSON.parse(response);
        console.log(response)
        
    for (key in response) {
        data[key] = response[key];
        }
    
    source.change.emit()
    p.reset.emit()
    var start = data['close'][data['close'].length -1] 
    var end = data['close'][data['close'].length -1] 

    for(var i =data['close'].length -50;i<=data['close'].length-1;i++)
    {
        if (start>data['close'][i])
        {
            start = data['close'][i]
        }
        if (end<data['close'][i])
        {
            end = data['close'][i]
        }
    }
    
    y_range.setv({"start": start-50, "end": end+50})

    var xstart = data['time'][data['time'].length-50] 
    var xstop = data['time'][data['time'].length-1]
    x_range.setv({"start":xstart, "end":xstop})

   
    
    if (time_frame == '/month' || time_frame == '/quater' || time_frame == '/year'){
        xstart = data['time'][0] 
        xstop = data['time'][data['time'].length-1]
        x_range.setv({"start":xstart, "end":xstop})

        for(var i =0;i<=data['close'].length-1;i++)
        {
        if (start>data['close'][i])
        {
            start = data['close'][i]
        }
        if (end<data['close'][i])
        {
            end = data['close'][i]
        }
        }
        y_range.setv({"start": start-300, "end": end+300})
        }
        
    
    console.log(p)

    x_range.change.emit()
    y_range.change.emit()
    ma_plt.x_range.setv({"start": xstart, "end": xstop})
    ma_plt.x_range.change.emit()
        }
    """)


    tab_trans = Panel(child=transac_plot, title="Transactions")
    tab_MA = Panel(child=MA_plot, title="Moving Average")
    tab_RSI = Panel(child=rsi_plt, title="RSI")
    tab_MACD = Panel(child=macd_plt, title="MACD")

    tabs = Tabs(tabs=[tab_trans, tab_MA, tab_RSI, tab_MACD])
    tabs.tabs_location = "above"
    


    #adding callbacks
    checkbox_button_group.js_on_click(callback_radio)
    Company_select.js_on_change('value', callback_select)
    timeframe_dropdown.js_on_change('value', callback_dropdown)

    #Ontap callback
    candle.js_on_event(DoubleTap, callback_tap)
    
    #final layout
    layout = column(row(Company_select,timeframe_dropdown),row(checkbox_button_group)
                ,row(column(candle,tabs), list_of_news) )
    
    
    return layout

def bullinder_band():
    band = Band(base='time', lower='bband_l', upper='bband_u', source=source, level='underlay',
                    fill_alpha=0.5, line_width=1, line_color='black', fill_color=BLUE_LIGHT)
    band.visible = False
    
    return band


def news_list():
    # news_dict = {'news' : nabil_news_list,
    #     'links' : ['http://www.reddit.com']*10
    # }
    # source = ColumnDataSource(news_dict)
    columns = [
        TableColumn(field="news", title="News")
    ]

    data_table = DataTable(source=source, columns=columns, width = 300, height=500)
    
    callback_code = """
        row = cb_obj.indices[0]
        console.log('news: ', source.data['news'][row])
        var news_link = source.data['urls'][row]
        window.open(news_link);
    """


    news_click_callback = CustomJS(args = dict(source=source), code = callback_code)


    source.selected.js_on_change('indices', news_click_callback)

    #taptool = data_table.select(type=TapTool)
    # taptool.callback = OpenURL(url = 'https://stackoverflow.com/questions/41511274/turn-bokeh-glyph-into-a-link')
    return data_table


def candle_plot():

    p = figure(x_axis_type="datetime",title = "CandleStick",plot_width=1000, plot_height=500,
          tools=TOOLS, active_scroll = 'xwheel_zoom', toolbar_location = "above",x_range = Range1d(date(2010,1,1),date(2020,1,1)))

    print('################################################')
    # if source.data['color'][-1] == 'blue':
    date_last = source.data['time2'][-1]
    date_2ndlast = source.data['time2'][-2]
    rect_width = date_last-date_2ndlast
    rect_height = source.data['close'][-1]
    # p.rect(x = date_2ndlast+rect_width/2, y = 0, width = rect_width, height = rect_height, alpha = 0.5, color = 'red')
    # if p.y_range.bounds:
    #     rect_height = p.y_range.bounds[1] - p.y_range.bounds[0]

    print('################################################')


    p.xaxis.formatter = DatetimeTickFormatter(
                                days=["%F"],
                                months=["%F"],
                                years=["%F"],)
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "price"

    p.segment(x0='time2', y0='low', x1='time2', y1='high', line_width=1, color='black', source=source)
    p.segment(x0='time2', y0='open', x1='time2', y1='close', line_width=6, color='color', source=source)
    # p.rect(x = date_2ndlast+rect_width/2, y = source.data['close'][-2], width = rect_width, height = rect_height, alpha = 0.5, color = 'red')
    # daylight_savings_start = Span(location=date_2ndlast+rect_width/2,
                            #   dimension='height', line_color='green', line_width=12, line_alpha = 0.5)
    # p.add_layout(daylight_savings_start)
    p.line(x='time2', y='close', alpha = 0.5, color = ORANGE, source = source)


    p.background_fill_color = "red"
    p.background_fill_alpha = 0.1

   
    p.x_range.start=source.data["time2"][-50]
    p.x_range.end= source.data["time2"][-1]
    p.x_range.bounds=(date(2010, 1, 1), date(2019, 12, 31))
    p.x_range.min_interval = timedelta(20)
    #p.x_range.start=source.data["time"][-50]
    #p.x_range.end= source.data["time"][-1]
    # p.y_range.start = axes_data['y_min']
    # p.y_range.end = axes_data['y_max']
    # p.x_range.start = axes_data['x_min']
    # p.x_range.end = axes_data['x_max']
    #p.x_range.bounds=(date(2009, 1, 1), date(2019, 12, 31))
    #p.y_range.bounds=(-50, 3000)
    #p.x_range.min_interval = timedelta(50)
    #p.y_range.min_interval = 100
    #p.x_range.follow = 'end'

    # if p.y_range.bounds:
        # rect_height = p.y_range.bounds[1] - p.y_range.bounds[0]
    
    # p.rect(x = date_2ndlast+rect_width/2, y = source.data['close'][-2], width = rect_width, height = rect_height, alpha = 0.5, color = 'red')


    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Date", "@time2{%F}"),
        ("Open", "@open"),
        ("Close", "@close"),
        ("High", "@high"),
        ("Low", "@low"),
        ]
    hover.formatters={"@time2":'datetime',}
    hover.mode = "vline"
   
    #p.yaxis.ticker = SingleIntervalTicker(interval=100, num_minor_ticks=5)
    p.yaxis[0].formatter = PrintfTickFormatter(format="Rs. %3.3f")
    #p.yaxis[0].ticker.desired_num_ticks = 10

    return p

def transaction_plot():
    #transaction graph
    p = figure(x_axis_type="datetime",title = "No of Transactions",plot_height=250,plot_width = 1000, tools=TOOLS,x_range = Range1d(date(2010,1,1),date(2020,1,1)) )
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "No of Transactions"

    p.segment(x0='time2', y0=0, x1='time2', y1='no_trans', line_width=6, color="black", alpha=0.5, source=source)
    p.toolbar.logo = None
    p.toolbar_location = None
    p.min_border_left = 95
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [
        ("Transaction", "@no_trans"),
        ]
    hover.mode = "vline"
    return p

def movingavg_plot():
    p2 = figure(x_axis_type="datetime",title = "Moving Average",plot_height=250,plot_width = 1000, tools=TOOLS ,x_range = Range1d(date(2010,1,1),date(2020,1,1)))
    p2.xaxis.axis_label = "date"
    p2.yaxis.axis_label = "Avg_price"
    p2.line(x='time', y='ma50', color=RED, source=source, legend = "Moving Average :- 50")
    p2.line(x='time', y='ma20', color=BLUE, source=source, legend = "Moving Average :- 20")
    p2.line(x='time', y='ma9', color=GREEN, source=source, legend = "Moving Average :- 9")
    p2.toolbar.logo = None
    p2.toolbar_location = None
    hover = p2.select(dict(type=HoverTool))
    hover.tooltips = [
        ("MA09", "@ma9"),
        ("MA20", "@ma20"),
        ("MA50", "@ma50"),
        ]
    hover.mode = "vline"
    return p2

def macd_plot():
    p2 = figure(x_axis_type="datetime",title = "MACD plot",plot_height=250,plot_width = 1000, tools=TOOLS ,x_range = Range1d(date(2010,1,1),date(2020,1,1)))
    p2.xaxis.axis_label = "date"
    p2.yaxis.axis_label = "Moving Avg Difference"
    p2.line(x='time', y='macd920', color=RED, source=source, legend = "MACD 09-20")
    p2.toolbar.logo = None
    p2.toolbar_location = None
    hover = p2.select(dict(type=HoverTool))
    hover.tooltips = [
        ("MACD", "@macd920"),
        ]
    hover.mode = "vline"
    return p2

def rsi_plot():
    p2 = figure(x_axis_type="datetime",title = "Relative Strength Index",plot_height=250,plot_width = 1000, tools=TOOLS,x_range = Range1d(date(2010,1,1),date(2020,1,1)) )
    p2.xaxis.axis_label = "date"
    p2.yaxis.axis_label = "RSI point"
    p2.line(x='time', y='rsi14', color=RED, source=source, legend = "RSI-14")
    p2.toolbar.logo = None
    p2.toolbar_location = None
    hover = p2.select(dict(type=HoverTool))
    hover.tooltips = [
        ("RSI", "@rsi14"),
        ]
    hover.mode = "vline"
    return p2


def add_vlinked_crosshairs(fig1, fig2,fig3,fig4, fig5):
    js_move = '''if(cb_obj.x >= fig.x_range.start && cb_obj.x <= fig.x_range.end && cb_obj.y >= fig.y_range.start && cb_obj.y <= fig.y_range.end)
                    { cross.spans.height.computed_location = cb_obj.sx }
                 else 
                    { cross.spans.height.computed_location = null }'''
    js_leave = 'cross.spans.height.computed_location = null'
    
    js_movemain = '''if(cb_obj.x >= fig.x_range.start && cb_obj.x <= fig.x_range.end && cb_obj.y >= fig.y_range.start && cb_obj.y <= fig.y_range.end)
                    { cross2.spans.height.computed_location = cb_obj.sx
                      cross3.spans.height.computed_location = cb_obj.sx
                      cross4.spans.height.computed_location = cb_obj.sx
                      cross5.spans.height.computed_location = cb_obj.sx }
                 else 
                    {cross2.spans.height.computed_location = null 
                    cross3.spans.height.computed_location = null
                    cross4.spans.height.computed_location = null
                    cross5.spans.height.computed_location = null}'''

    js_leavemain = '''{cross2.spans.height.computed_location = null 
                    cross3.spans.height.computed_location = null
                    cross4.spans.height.computed_location = null
                    cross5.spans.height.computed_location = null}'''

    cross1 = CrosshairTool()
    cross2 = CrosshairTool()
    cross3 = CrosshairTool()
    cross4 = CrosshairTool()
    cross5 = CrosshairTool()
    fig1.add_tools(cross1)
    fig2.add_tools(cross2)
    fig3.add_tools(cross3)
    fig4.add_tools(cross4)
    fig5.add_tools(cross5)
    args = {'cross2': cross2,'cross3': cross3,'cross4': cross4,'cross5': cross5, 'fig': fig1}
    fig1.js_on_event('mousemove', CustomJS(args = args, code = js_movemain))
    fig1.js_on_event('mouseleave', CustomJS(args = args, code = js_leavemain))
    args = {'cross': cross1, 'fig': fig2}
    fig2.js_on_event('mousemove', CustomJS(args = args, code = js_move))
    fig2.js_on_event('mouseleave', CustomJS(args = args, code = js_leave))
    args = {'cross': cross1, 'fig': fig3}
    fig3.js_on_event('mousemove', CustomJS(args = args, code = js_move))
    fig3.js_on_event('mouseleave', CustomJS(args = args, code = js_leave))
    args = {'cross': cross1, 'fig': fig4}
    fig4.js_on_event('mousemove', CustomJS(args = args, code = js_move))
    fig4.js_on_event('mouseleave', CustomJS(args = args, code = js_leave))
    args = {'cross': cross1, 'fig': fig5}
    fig5.js_on_event('mousemove', CustomJS(args = args, code = js_move))
    fig5.js_on_event('mouseleave', CustomJS(args = args, code = js_leave))






def nepse_plot():
    

    data = pd.read_csv("nepse_data.csv")
    data['time2'] = data['time'] 
    source = ColumnDataSource(data)



    p = figure(x_axis_type="datetime",title = "Nepse CandleStick",plot_width=1200, plot_height=500,
          tools=TOOLS, active_scroll = 'wheel_zoom', toolbar_location = "above")

    p.xaxis.formatter = DatetimeTickFormatter(
                                days=["%F"],
                                months=["%F"],
                                years=["%F"],)
    p.xaxis.axis_label = "date"
    p.yaxis.axis_label = "price"

    p.segment(x0='time2', y0='low', x1='time2', y1='high', line_width=1, color='black', source=source)
    p.segment(x0='time2', y0='open', x1='time2', y1='close', line_width=6, color='black', source=source)
    p.line(x='time2', y='close', alpha = 0.5, color = ORANGE, source = source)
   
    #p.x_range.start=source.data["time"][-50]
    #p.x_range.end= source.data["time"][-1]
    p.x_range.bounds=(date(2010, 1, 1), date(2019, 12, 31))
    p.y_range.bounds=(-50, 3000)
    p.x_range.min_interval = timedelta(50)
    p.y_range.min_interval = 100
    #p.x_range.follow = 'end'
    
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
   
    #p.yaxis.ticker = SingleIntervalTicker(interval=100, num_minor_ticks=5)
    p.yaxis[0].formatter = PrintfTickFormatter(format="Rs. %3.3f")
    #p.yaxis[0].ticker.desired_num_ticks = 10

    return p
