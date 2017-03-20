import pandas as pd 
import geocoder 
import googlemaps
import geopandas
import geojson
from shapely.geometry import Point
from geopandas import GeoDataFrame
from geojson import Feature, FeatureCollection
from geojsonio import display

gmaps = googlemaps.Client(key='my_key')

# open csv with list of bubble tea places in new york city
boba = pd.read_csv('./boba.csv')

# gets latitutde and longitudes of each place
boba['Lat'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lat)
boba['Longitude'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lng)

# writes to a csv and opens
boba.to_csv('boba_final.csv')
boba = pd.read_csv('./boba_final.csv')

# converts lat and long points to coordinate point data type
geo = [Point(xy) for xy in zip(boba.Longitude, boba.Lat)]

# sets to geodataframe
crs = {'init': 'epsg:4326'}
geo_df = GeoDataFrame(geo, crs=crs, geometry=geo) 

# fixes json formatting and puts it back into geodataframe
l1 = [geojson.dumps(i, sort_keys=True) for i in geo]
geo_df = GeoDataFrame(l1, crs=crs, geometry=geo) 

# displays to geojsonio
display(geo_df.to_json())