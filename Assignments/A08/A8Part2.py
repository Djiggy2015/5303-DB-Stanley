'''
This program goes through a collection of volcano data and sorts
it according to the Population Exposure Index of each volcano.
While all of the volcanoes are plotted on the world map, the 
top three volcanoes are given an extra plot that creates a circle
around them, showing that they have the highest PEI.
'''

import plotly
import plotly.graph_objects as go
import pymongo



client = pymongo.MongoClient("mongodb:localhost:27017/")
db = client["armageddon"]
token = ""

volcano = db["volcanos"]

# Create some lists in order to store volcano information that can be passed to mapbox
vlist = []
lats = []
lons = []
Names = []

# Loop through the volcanoes and sort them by their PEI
for obj in volcano.find():
  vlist.append(db["volcanoes"].find().sort([("PEI", -1)]))
  lats.append(obj["latitude"])
  lons.append(obj["longitude"])
  Names.append(obj["V_Name"])

fig = go.Figure()

# This trace will add a circle around the volcanoes with the highest PEI
# Red = 1st, Orange = 2nd, Yellow = 3rd.
fig.add_trace(go.Scattermapbox(
  lat = lats,
  lon = lons,
  mode = "markers",
  # The marker size needs to be large enough to where volcano icon does
  # not cover it
  marker = {"size":[30, 30, 30], "color":["Red", "Orange", "Yellow"]}
  ) 
)

# This trace will add all of the volcanoes into the map along with their
# PEI count
fig.add_trace(go.Scattermapbox(
  lat = lats,
  lon = lons,
  mode = "markers",
  text = Names,
  marker = dict(size = 10, symbol = "volcano")
  )
)

fig.update_layout(
  hovermode = 'closest',
  template = 'plotly_dark',
  mapbox = go.layout.Mapbox(
    accesstoken = token,
    bearing = 0,
    center = go.layout.mapbox.Center(
      lat = 10,
      lon = 10
    ),
    pitch = 0,
    zoom = 3,
  ),
  title = "Volcanoes ranked by their Population Exposure Index (PEI)"
)

fig.show()
