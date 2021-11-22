"""
Vizualizing Earthquake Data

Heidi Duus
Ronni Madsen
Rasmus Vahlgreen

Visualization Project 2020

Run with: bokeh serve vis.py --show --session-token-expiration 1000000
"""


import pandas as pd
import warnings
from pyproj import Proj, transform
import math


from bokeh.io import output_file, output_notebook
from bokeh.plotting import figure, show,gmap,curdoc
from bokeh.models import Legend,Select, CheckboxGroup,CustomJS,ColumnDataSource, GMapOptions, Slider, ColorBar,LinearColorMapper, Range1d, HoverTool, PanTool,CDSView, IndexFilter, LinearInterpolator, RadioGroup
from bokeh.layouts import row, column, gridplot,widgetbox, layout
from bokeh.models.widgets import Tabs, Panel, Button, Slider
from bokeh.tile_providers import Vendors, get_provider #ignore error message. These modules exists despite what the IDE says
from bokeh.transform import linear_cmap,factor_cmap, factor_mark
from bokeh.palettes import Blues8
from bokeh.client import push_session, pull_session



warnings.filterwarnings("ignore")

#instantiate a document
curdoc = curdoc()


#Update method for magnitude slider
def updateMag(attr, new, old):
    N = mag_slider.value
    K = depth_slider.value
    M = menu.value
    Y = year_slider.value
    if(M=="All"):
        new1 = ColumnDataSource(data.loc[(data.mag >= N) & (data.depth >= K) & (data.year == Y)])
    else:
        new1 = ColumnDataSource(data.loc[(data.mag >= N) & (data.depth >= K) & (data.year == Y) & (data.month == M)])
    
    #new1.data["frequencies"]
    columndata.data = dict(new1.data)

#Update method for depth slider
def updateDepth(attr, new, old):
    K = depth_slider.value
    N = mag_slider.value
    Y = year_slider.value
    M = menu.value

    if(M=="All"):
        new1 = ColumnDataSource(data.loc[(data.depth >=K) & (data.mag >= N) & (data.year == Y)])

    else:
        new1 = ColumnDataSource(data.loc[(data.depth >=K) & (data.mag >= N) & (data.year == Y) & (data.month == M)])

    columndata.data = dict(new1.data)


#update year slider
def updateYear(attr,new,old):
    K = depth_slider.value
    N = mag_slider.value
    Y = year_slider.value
    M = menu.value

    if(M=="All"):
        new1 = ColumnDataSource(data.loc[(data.year == Y) & (data.mag >= N) & (data.depth >= K)])

    else:
        new1 = ColumnDataSource(data.loc[(data.year == Y) & (data.mag >= N) & (data.depth >= K) & (data.month == M)])

    columndata.data = dict(new1.data)


#update dropdown menu
def updateMenu(attr, new, old):
    val = menu.value
    K = mag_slider.value
    N = depth_slider.value
    Y = year_slider.value

    if val =="All":
        new1 = ColumnDataSource(data.loc[(data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "January":
        new1 = ColumnDataSource(data.loc[(data.month == "January") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data) 
    
    elif val == "February":
        new1 = ColumnDataSource(data.loc[(data.month == "February") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)
    
    elif val == "March":
        new1 = ColumnDataSource(data.loc[(data.month == "March") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val =="April":
        new1 = ColumnDataSource(data.loc[(data.month == "April") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)
    
    elif val == "May": 
        new1 = ColumnDataSource(data.loc[(data.month == "May") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)
    
    elif val == "June":
        new1 = ColumnDataSource(data.loc[(data.month == "June") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "July":
        new1 = ColumnDataSource(data.loc[(data.month == "July") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "August":
        new1 = ColumnDataSource(data.loc[(data.month == "August") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "September":
        new1 = ColumnDataSource(data.loc[(data.month == "September") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "October":
        new1 = ColumnDataSource(data.loc[(data.month == "October") & (data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "November":
        new1 = ColumnDataSource(data.loc[(data.month == "November") &(data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)

    elif val == "December":
        new1 = ColumnDataSource(data.loc[(data.month == "December") &(data.depth >=N) & (data.mag >= K) & (data.year == Y)])
        columndata.data = dict(new1.data)


#Method to project longitude and latitude to mercator coordinates
def projectToPlane(longitude_df,latitude_df):
    in_wgs =Proj(init="epsg:4326")
    out_mercator = Proj(init="epsg:3857")

    result = []

    for i in range(len(longitude_df)):
        mercator_x, mercator_y=transform(in_wgs, out_mercator, longitude_df[i],latitude_df[i])
        result.append((mercator_x,mercator_y))

    long_df =[result[i][0] for i in range(len(result))] 
    lat_df = [result[i][1] for i in range(len(result))]
    
    long_df = pd.DataFrame(long_df)
    lat_df = pd.DataFrame(lat_df)
    return (long_df, lat_df)





######################### Read and process data #########################
data = pd.read_csv("/Users/rasmusvahlgreen/Desktop/python/bokeh/earthquakes/data_test.csv")
data = data.drop(["nst","gap","dmin","rms","net","id","updated","place","locationSource","magSource","horizontalError","depthError","magNst","status"], axis=1)
data["long"] = data["longitude"].copy()
data["lat"] = data["latitude"].copy()
data["time"] = data["time"].str.replace("T"," ")
data["time"] = data["time"].str.replace("Z","")
data['time'] = data['time'].str[:-4]
data["year"] = data["time"].str[:4].astype(int)
data["month"] = data["time"].str[5:7].astype(str)
data["month"].replace({"01": "January", "02": "February", "03": "March", "04": "April", "05": "May", "06": "June", "07": "July", "08": "August", "09": "September", "10": "October", "11": "November", "12": "December"}, inplace=True)

#project longitude and latitude coordinates
data["longitude"] , data["latitude"] = projectToPlane(data["longitude"],data["latitude"])

 



################################ This part creates the plot ############################



columndata = ColumnDataSource(data)


#Determines linear relationship between size of a glyph and the data points' estimated magnitude error
#size_mapper is parsed as size argument to the glyphs
size_mapper = LinearInterpolator(
    x = [data.magError.max(),data.magError.min()],
    y = [1,8])


#Provides background map
tile_provider = get_provider(Vendors.CARTODBPOSITRON_RETINA)
#tile_provider = get_provider(Vendors.STAMEN_TERRAIN_RETINA)
#OSM

#Define colors for colormapper. Pass colormapper to the colorbar object
colors = ("#deebf7","#c6dbef","#9ecae1","#6baed6","#4292c6","#084594","#002e63")
color_mapper = LinearColorMapper(palette=colors, low=min(columndata.data["mag"]), high=max(columndata.data["mag"]))
color_bar = ColorBar(color_mapper=color_mapper,title = "Mag",title_text_font_size='11px',label_standoff=12, border_line_color=None, location=(0,0))


#intantiate figure
fig = figure(plot_height=700,
      plot_width=1000,
      x_range = (-21000000, 20000000),
      y_range = (-18000000, 12000000),
      x_axis_type = "mercator",
      y_axis_type = "mercator",
      x_axis_label='Projected longitude',
      y_axis_label='Projected latitude',
      background_fill_color='#440154',
      title='World Distribution of Earthquakes',
      toolbar_location='below',
      toolbar_sticky=False,
      tools=["box_select",'box_zoom', 'reset', 'pan','wheel_zoom'])

#add colorbar and background map to figure
fig.add_tile(tile_provider)
fig.add_layout(color_bar, "right")


#circle glyphs will represent earthquakes
fig.circle(x='longitude',
      y='latitude',
      source=columndata,
      line_color = "blue",
      fill_color = linear_cmap("mag",palette=colors,low=min(columndata.data['mag']), high=max(columndata.data['mag'])),
      alpha=0.9,
      size=10,  #{'field':'magError', 'transform':size_mapper}
      selection_color='deepskyblue',
      nonselection_alpha=0.3)



#create hovertool and decide on what information to display
fig.add_tools(HoverTool(tooltips=[                                                   
            ('Date & Time','@time UTC'),                
            ('Depth', '@depth km'),
            ("Magnitude", "@mag Ml"),
      ]))

#define dropdown menu
Labels = ['January','February',"March","April","May","June","July","August","September","October","November","December","All"]
menu = Select(title="Choose month", options=Labels, value='All')

#define magnitude slider
mag_slider = Slider(start = math.ceil(min(columndata.data["mag"])), 
    end = math.floor(max(columndata.data["mag"])), 
    step = 1, 
    title = "Display magnitudes greater than or equal to (Ml)", 
    value = math.ceil(min(columndata.data["mag"])),
    width = 300,
    height=100)

#define depth slider
depth_slider = Slider(start = 0,
    end = math.floor(max(columndata.data["depth"])),
    step = 5,
    value = 0,
    title = "Display depths greater than or equal to (km)",
    width = 300,
    height=100)

#define year slider
year_slider = Slider(start = min(columndata.data["year"]),
    end = max(columndata.data["year"]),
    step = 1,
    value = 2019,
    title = "Year" ,
    width = 300,
    height = 100)

#define scatterplot
scatter = figure(x_range = (min(columndata.data["depth"]),max(columndata.data["depth"])),
    plot_height = 500, plot_width = 1000, toolbar_location='below',
    x_axis_label='Depth (km)',
    y_axis_label='Magnitude (Ml)',
    toolbar_sticky=False,
    tools=["box_select",'box_zoom', 'reset', 'pan','wheel_zoom'])

scatter.scatter(x="depth", y = "mag", source = columndata)



#the on_change method links widgets with their update methods
mag_slider.on_change("value", updateMag)
depth_slider.on_change("value",updateDepth)
year_slider.on_change("value",updateYear)
menu.on_change('value', updateMenu)

#create layout containing the plot and sliders
layout = layout(column(row(fig,widgetbox(mag_slider,depth_slider,year_slider, menu)),scatter))

#add layout to the current document
curdoc.add_root(layout)