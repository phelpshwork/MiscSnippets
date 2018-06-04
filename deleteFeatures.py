# deletes features from an ArcGIS Enterprise instance 
# requires a "credentials.py" file with username and password variables set in same directory

from credentials import username, password
from arcgis.gis import GIS
gis = GIS("https://wdcintel.maps.arcgis.com", username, password)

# find the thing to delete - examples below
#data = gis.content.search("name:Spire API Feature Service GeoEvent")[0]
# the 0 makes it the first one (if there are multiples)
data = gis.content.search("name:Spire_Add_Features")[0]

# get the feature layer of the thing to delete (this is how to access features)
fl = data.layers[0] # the 0 makes it the first one (if there are multiples)
fl # shows what query brought back - sometimes the service definition is first
#fl.delete_features(where="1=1") # gets rid of all features in the feature layer - use with care!
# or 
#fl.delete_features(where="OID<10000")
