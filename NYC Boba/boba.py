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
	gmaps = googlemaps.Client(key='your_api_key_here')

	# filename: file with list of bubble tea places and addresses
	def __init__(self, filename):
		# initalizes csv with list of bubble tea places to dataframe
		self.boba = pd.read_csv(filename)

	# calc_coordinates: pulls coordinates from google maps and adds to dataframe
	def calc_coords(self): 
		# gets latitude and longitudes of each place
		self.boba['Lat'] = self.boba['Address'].apply(geocoder.google).apply(lambda x: x.lat)
		self.boba['Longitude'] = self.boba['Address'].apply(geocoder.google).apply(lambda x: x.lng)
		# converts lat and long points to coordinate point data type
		self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Longitude, self.boba.Lat)]

	# get_geo: returns all coordinates as a list
	def get_geo(self):
		return(list(self.boba['Coordinates']))

	# get_names: get method for names column
	def get_names(self):
		return(self.boba['Name'])

	# get_gdf: returns geoDataFrame of needed data
	def get_gdf(self):
		# coordinate system parameters
		crs = {'init': 'epsg:4326'}
		return(GeoDataFrame(self.get_names(), crs=crs, geometry=self.get_geo()))

	# get method for the entire boba dataframe
	def get_boba(self):
		return(self.boba)
	
	# provides boba recommendations based on correct location
	def boba_recs(self, lat, lng):
		user_loc = Point(lng, lat) # converts user lat/long to point object
		# makes dataframe of distances between each boba place and the user loc
		self.boba['Distance'] = [user_loc.distance(Point(xy)) for xy in zip(self.boba.Longitude, self.boba.Lat)]
	    	# grabs the three smallest distances
		boba_list = self.boba.nsmallest(3, 'Distance').set_index('Name') # sets index to name
		temp = (": " + boba_list['Address']).rename_axis(None).__repr__()
		return(temp.rsplit('\n', 1)[0]) # formatted to string

	# Adds a boba place for when you find a new one and dont want to redo it 
	def add(self, name, addr, rest):
		obj = geocoder.google(addr)
		df2 = pd.DataFrame({'Name': [name],
			'Address': [addr],
			'Restaurant': [rest],
			'Lat': [obj.lat],
			'Longitude': [obj.lng],
			'Coordinates': [Point(obj.lng, obj.lat)]}, index=[len(self.boba)])
		self.boba = pd.concat([self.boba, df2])
		return(self.boba)

	# visualizes the geojson using geojsonio
	def visualize(self):
		self.boba['Coordinates'] = [Point(xy) for xy in zip(self.boba.Longitude, self.boba.Lat)]
		updated = self.get_gdf()
		display(updated.to_json())
 

if __name__ == "__main__":
	buff = True
	b1 = BubbleTea("./boba_final.csv")

	while buff:
		bname = input("Boba Place Name:")
		baddress = input("Boba Place Address:")
		brestaurant = input("Is this place a restaurant? Y/N")
		update_df = b1.add(bname, baddress, brestaurant)
		update_df.to_csv("./boba_final.csv")
		ask = input("Want to add a place? Y/N ")
		if ask == "N":
			buff = False
			b1.visualize()
