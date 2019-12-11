"""
This file removes lat/lon pairs that are not numbers
and removes total fatal injuries that are not numbers
allowing us to use the data in order to perform distance
queries, and create maps.
"""

import pymongo

client = pymongo.MongoClient("mongodb://192.168.99.100:27017/")
db = client["armageddon"]
crashes = db["plane_crashes"]

# Used to show how many files were deleted
badcount = 0
finalcount = 0
initialcount = crashes.count()

# loop through the document and remove bad data
for obj in crashes.find():
  mongo_id = obj["_id"]
  lat = obj["Latitude"]
  lon = obj["Longitude"]
  fatal = obj["TotalFatalInjuries"]

  # Remove files that don't have any data regarding the total number 
  # of fatalities. Note: no data for fatalities in this collection is
  # represented by two spaces surrounded by quotes.
  if (fatal == "  ") or (fatal == None):
    badcount  += 1
    crashes.delete_one({'_id':mongo_id})
    print("Deleted")


  # Remove files that don't have any data for lat lon pairs
  if(lat == None) or (lon == None) or (lat == "  ") or (lon == "  "):
    badcount += 1
    crashes.delete_one({'_id':mongo_id})
    print("Deleted")


# subtract the number of deleted files from the initial number
# of files
finalcount = initialcount - badcount

print(finalcount)
print(badcount)
