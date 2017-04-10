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
	gmaps = googlemaps.Client(key='your_key')

	def __init__(self, filename):
		# initalizes csv with list of bubble tea places to dataframe
		self.boba = pd.read_csv(filename)

	def calc_coords(self): 
		# gets latitude and longitudes of each place
		self.boba['Lat'] = self.boba['Address'].apply(geocoder.google).apply(lambda x: x.lat)
		self.boba['Longitude'] = self.boba['Address'].apply(geocoder.google).apply(lambda x: x.lng)
		# converts lat and long points to coordinate point data type
		self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Longitude, self.boba.Lat)]

	def get_geo(self):
		return(list(self.boba['Coordinates']))

	def get_names(self):
		return(self.boba['Name'])

	def get_gdf(self):
		# coordinate system parameters
		crs = {'init': 'epsg:4326'}
		return(GeoDataFrame(self.get_names(), crs=crs, geometry=self.get_geo()))

	def get_boba(self):
		return(self.boba)
	
	# still not written
	def update(self):
		self.boba = self.boba['Name'].where(self.boba['Lat'] == float('nan'))

if __name__ == "__main__":
	boba1 = BubbleTea("./sample.csv")
