"""
Plots ufos, airports, and earthquakes on the same graph, but with different
colors and sizes.   
"""

import numpy as np 
import pandas as pd
import plotly
import plotly.graph_objects as go
import pymongo

# Connect to the Mongo Database
client = pymongo.MongoClient("mongodb:localhost")
db = client["armageddon"]
collections = [db["earthquakes"], db["ufos"], db["airports"]]

# Obtain Mapbox token
# Empty because Github repository is local
token = ""

# Create empty lists for the lons and lats of each collection
# in the database
EQlat = []
EQlon = []
Ufolat = []
Ufolon = []
Aplat = []
Aplon = []


# Find the lats and lons for earthquakes
for obj in db["earthquakes"].find():
    EQlat.append(obj["latitude"],)
    EQlon.append(obj["longitude"])

# Find the lats and lons for ufos
for obj in db["ufos"].find():
    Ufolat.append(obj["latitude"],)
    Ufolon.append(obj["longitude"])

# Find the lats and lons for airports
for obj in db["airports"].find():
    Aplat.append(obj["latitude"],)
    Aplon.append(obj["longitude"])

fig = go.Figure()

# Update Mapbox with the earthquake data
fig.add_trace(
    go.Scattermapbox(
        lat = EQlat,
        lon = EQlon,
        mode = 'markers',
        marker= go.scattermapbox.Marker(size=7, color = "orange"), name = "Earthquake"
))

# Update Mapbox with the ufo data
fig.add_trace(
    go.Scattermapbox(
        lat = Ufolat,
        lon = Ufolon,
        mode = 'markers',
        marker=go.scattermapbox.Marker(size=5, color = "blue"), name = "Ufos"
))

# Update Mapbox with the Airport data
fig.add_trace(
    go.Scattermapbox(
        lat = Aplat,
        lon = Aplon,
        mode = 'markers',
        marker = go.scattermapbox.Marker(size = 4, color = "green"), name = "Airport"
    )
)

# This will update mapbox with how we want it to look.
fig.update_layout(
    hovermode = 'closest',
    template = "plotly_dark",
    mapbox=go.layout.Mapbox(
        accesstoken=token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=10,
            lon=10
        ),
        pitch=0,
        zoom=3
    ),
)

fig.show()
#plotly.offline.plot(fig, filename='Airports_Ufos_and_Earthquakes')
