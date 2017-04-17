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
	
	def boba_recs(self, lat, lng):
		user_loc = Point(lng, lat) # converts user lat/long to point object
		# makes dataframe of distances between each boba place and the user loc
		self.boba['Distance'] = [user_loc.distance(Point(xy)) for xy in zip(self.boba.Longitude, self.boba.Lat)]
	    	# grabs the three smallest distances
		boba_list = self.boba.nsmallest(3, 'Distance').set_index('Name') # sets index to name
	    	temp = (": " + boba_list['Address']).rename_axis(None).__repr__() 
	    	return(temp.rsplit('\n', 1)[0]) # formatted to string

	# still not written
	def update(self):
		self.boba = self.boba['Name'].where(self.boba['Lat'] == float('nan'))

if __name__ == "__main__":
	boba1 = BubbleTea("./sample.csv")
