import pandas as pd 
import geocoder 
import googlemaps
import geopandas
import geojson
from shapely.geometry import Point
from geopandas import GeoDataFrame
from geojson import Feature, FeatureCollection
from geojsonio import display


class BubbleTea(object):

	# authentication initialized
	gmaps = googlemaps.Client(key='my_key')

	def __init__(self, filename):
		# initalizes csv with list of bubble tea places to dataframe
		boba = pd.read_csv(filename)

	def get_coords(self): 
		# gets latitude and longitudes of each place
		boba['Lat'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lat)
		boba['Longitude'] = boba['Address'].apply(geocoder.google).apply(lambda x: x.lng)
		# converts lat and long points to coordinate point data type
		boba['Coordinates'] = [Point(xy) for xy in zip(boba.Longitude, boba.Lat)]

	def get_geo(self):
		return(list(boba['Coordinates']))

	def get_names(self):
		return(boba['Name'])

	def get_gdf(self):
		# coordinate system parameters
		crs = {'init': 'epsg:4326'}
		return(GeoDataFrame(get_names(), crs=crs, geometry=get_geo()))

	#def update(self):


if __name__ == "__main__":
	display(geo_df.to_json())




