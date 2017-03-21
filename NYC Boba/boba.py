import pandas as pd 
import geocoder 
import googlemaps
import geopandas
import geojson
from shapely.geometry import Point
from geopandas import GeoDataFrame
from geojson import Feature, FeatureCollection
from geojsonio import display

# authentication initialized
gmaps = googlemaps.Client(key='my_key')

# open csv with list of bubble tea places in new york city
boba = pd.read_csv('./boba.csv')

# gets latitutde and longitudes of each place
boba['Lat'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lat)
boba['Longitude'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lng)

# converts lat and long points to coordinate point data type
boba['Coordinates'] = [Point(xy) for xy in zip(boba.Longitude, boba.Lat)]

# writes to a csv and opens
boba.to_csv('boba_final.csv')
boba = pd.read_csv('./boba_final.csv')

# list of coordinates
geo = [Point(xy) for xy in zip(boba.Longitude, boba.Lat)]

# series for boba names
bname = boba['Name']

# coordinate system parameter
crs = {'init': 'epsg:4326'}

# converts to geodataframe
geo_df = GeoDataFrame(bname, crs=crs, geometry=geo) 

# displays to geojsonio
display(geo_df.to_json())




