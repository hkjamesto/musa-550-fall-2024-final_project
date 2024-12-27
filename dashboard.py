
## folium
import folium
from folium import plugins
from folium.plugins import DualMap
# import ipywidgets as widgets
from ipywidgets import interact, widgets, HBox
from IPython.display import display, HTML
import panel as pn
pn.extension()

# Function to update the map based on selected year and month
def update_map(year, month):
    temp = LAcrime[(LAcrime["Month"] == month) & (LAcrime["Year"] == year)]
    
    # Separate data for violent and property crimes
    violent_crimes = temp[temp["Crime Type"] == "violent"]
    property_crimes = temp[temp["Crime Type"] == "property"]
    
    # Initialize DualMap: one for violent crimes (left) and one for property crimes (right)
    m = DualMap(location=[34.0522, -118.2437], zoom_start=9)
    
    # Add LAPD reporting districts (optional)
    folium.GeoJson(
        LAPD_rd,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["PREC"], aliases=["Precinct:"], localize=True),
        name="LAPD Reporting Districts"
    ).add_to(m.m1)
    
    folium.GeoJson(
        LAPD_rd,
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(fields=["PREC"], aliases=["Precinct:"], localize=True),
        name="LAPD Reporting Districts"
    ).add_to(m.m2)
    
    # Add violent crimes to the left map
    for _, row in violent_crimes.iterrows():
        folium.CircleMarker(
            [row["LAT"], row["LON"]],
            radius=5,
            color="red",
            fill=True,
            fill_color="red",
            tooltip=f'Violent Crime: {row["Crime_Description"]} ({row["LAT"]}, {row["LON"]})'
        ).add_to(m.m1)
    
    # Add property crimes to the right map
    for _, row in property_crimes.iterrows():
        folium.CircleMarker(
            [row["LAT"], row["LON"]],
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue",
            tooltip=f'Property Crime: {row["Crime_Description"]} ({row["LAT"]}, {row["LON"]})'
        ).add_to(m.m2)
    
    # Return the map as an HTML pane to Panel
    return pn.panel(m, height=500, width=800)

# Create the sliders for year and month
year_selector = pn.widgets.IntSlider(name='Year', start=2010, end=2024, value=2010)
month_selector = pn.widgets.IntSlider(name='Month', start=1, end=12, value=1)

# Bind the function to the widgets
interactive_map = pn.bind(update_map, year=year_selector, month=month_selector)

# Layout the widgets and map together
layout = pn.Column(year_selector, month_selector, interactive_map)

# Display in a Quarto-friendly format (return layout for Quarto/Notebook)
layout.servable()
