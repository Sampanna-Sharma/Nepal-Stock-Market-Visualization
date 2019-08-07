from bokeh.plotting import figure, show
from datetime import date, timedelta
from bokeh.models import ColumnDataSource, HoverTool, Rect


from bokeh.palettes import Category20

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
url = "http://127.0.0.1:5000/data/year?company=Nabil%20Bank%20Limited"
r = requests.get(url)
company_data = json.loads(r.text)
source = ColumnDataSource(company_data)

index_of_last = -1
index_of_2ndlast = -2

print('####################################')
date_last = source.data['time2'][index_of_last]
date_2ndlast = source.data['time2'][index_of_2ndlast]
rect_width = date_last - date_2ndlast
rect_height = source.data['close'][index_of_2ndlast] 
print('####################################')



p = figure(x_axis_type="datetime",title = "CandleStick",plot_width=1000, plot_height=500,
          tools=TOOLS, active_scroll = 'xwheel_zoom', toolbar_location = "above")


print('Fugure props :::::::  ',(p.x_range.bounds)   )

p.xaxis.axis_label = "date"
p.yaxis.axis_label = "price"

p.segment(x0='time2', y0='low', x1='time2', y1='high', line_width=1, color='black', source=source)
p.segment(x0='time2', y0='open', x1='time2', y1='close', line_width=6, color='color', source=source)
p.line(x='time2', y='close', alpha = 0.5, color = ORANGE, source = source)






p.x_range.bounds=(date(2010, 1, 1), date(2019, 12, 31))
p.y_range.bounds=(-50, 3000)
p.x_range.min_interval = timedelta(50)
p.y_range.min_interval = 100
#p.x_range.follow = 'end'

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


show(p)
p.rect(x = date_2ndlast+rect_width/2, width = rect_width, y = (p.y_range.bounds[1] - p.y_range.bounds[0])/2, height = p.y_range.bounds[1] - p.y_range.bounds[0], alpha = 0.5)
show(p)

print('Fugure props :::::::  ',(p.y_range.bounds[0])   )

