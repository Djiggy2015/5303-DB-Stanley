'''
This program loops through a collection of plane crashes and
sorts them by their number of fatalities. The crashes are then
plotted using mapbox, with different colors representing how 
many fatalities occured.
'''

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as pg
import pymongo

client = pymongo.MongoClient("mongodb:localhost/27017/")
db = client["armageddon"]
token = ""

crashes = db["plane_crashes"]

# Create lists to hold the locations of crashes with most fatalities
crashes300lat = []
crashes300lon = []
crashes200lat = []
crashes200lon = []
crashes100lat = []
crashes100lon = []
crashesrestlon = []
crashesrestlat = []

# These arrays will help show how many deaths occured at each crash site
crashes300count = []
crashes200count = []
crashes100count = []
crashesrestcount = []

# Loop through the data and sort it by how many fatalities occured
for obj in crashes.find():

  if(int(obj["TotalFatalInjuries"]) > 300):
    crashes300lat.append(obj["Latitude"])
    crashes300lat.append(obj["Longitude"])
    crashes300count.append(obj["TotalFatalInjuries"])
  
  elif(int(obj["TotalFatalInjuries"]) > 200):
    crashes200lat.append(obj["Latitude"])
    crashes200lon.append(obj["Longitude"])
    crashes200count.append(obj["TotalFatalInjuries"])

  elif(int(obj["TotalFatalInjuries"]) > 100):
    crashes100lat.append(obj["Latitude"])
    crashes100lon.append(obj["Longitude"])
    crashes100count.append(obj["TotalFatalInjuries"])

  else:
    crashesrestlat.append(obj["Latitude"])
    crashesrestlon.append(obj["Longitude"])
    crashesrestcount.append(obj["TotalFatalInjuries"])

fig = pg.Figure()

# Add the 300+ deaths to the map. None actually show up on the
# map (Hopefully because there are none.)
fig.add_trace(pg.Scattermapbox(
  lat = crashes300lat,
  lon = crashes300lon,
  text = crashes300count,
  mode = "markers",
  marker = {"size": 10, "color": "red"}
  )
)

# Add the 200+ deaths to the map
fig.add_trace(pg.Scattermapbox(
  lat = crashes200lat,
  lon = crashes200lon,
  text = crashes200count,
  mode = "markers",
  marker = {"size": 10, "color": "orange"}
  )
)

# Add the 100+ deaths to the map
fig.add_trace(pg.Scattermapbox(
  lat = crashes100lat,
  lon = crashes100lon,
  text = crashes100count,
  mode = "markers",
  marker = {"size": 10, "color": "yellow"}
  )
)

# Add the rest of the deaths to the map
fig.add_trace(pg.Scattermapbox(
  lat = crashesrestlat,
  lon = crashesrestlon,
  text = crashesrestcount,
  mode = "markers",
  marker = {"size": 10, "color": "blue"}
  )
)

fig.update_layout(
  hovermode = 'closest',
  template = 'plotly_dark',
  mapbox = pg.layout.Mapbox(
    accesstoken = token,
    bearing = 0,
    center = pg.layout.mapbox.Center(
      lat = 10,
      lon = 10
    ),
    pitch = 0,
    zoom = 3,
  ),
 title = "Plane crashes and their fatalities"
)

fig.show()
