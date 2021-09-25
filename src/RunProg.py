from mainProg import dataF
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource


dataF["Start_string"]=dataF["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
dataF["Stop_string"]=dataF["Stop"].dt.strftime("%Y-%m-%d %H:%M:%S")
cds=ColumnDataSource(dataF)



p=figure(x_axis_type="datetime", height=100, sizing_mode='scale_width', title="Motion Graph")
p.title.align = "center"
p.yaxis.minor_tick_line_color=None
p.yaxis.ticker.min_interval=1
p.ygrid.visible = False

hover=HoverTool(tooltips=[("Start", "@Start_string"),("Stop", "@Stop_string")])
p.add_tools(hover)

p.quad(left="Start",right="Stop",top=1, bottom=0, color="green", source=cds)

output_file("Graph.html")
show(p)
