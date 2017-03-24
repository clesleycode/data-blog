### Objective 

The purpose of this project was to build an interactive map data visualization of all the bubble tea places in New York City. The final product will consist of a map of New York City with data points of each place with labels containing the title.

### Data Collection

My first approach was to use the Yelp API to retrieve the bubble tea places in the New York City area. This output a clearly inaccurate number of places, 37 (based on personal experience). I tried the following approaches to see if a more accurate number could be retrieved, but unfortunately was unsuccessful. This includes:

- I expanded the `radius_filter` to include a wider mileage range.
- I changed the `category_filter` to include other similar categories, such as boba, bubble tea, and coffee & tea.

As I said, this proved unsuccessful. Not only were all the bubble tea places not retrieved, but places that don't qualify as bubble tea places were output. It was at this point that I decided to just create the data myself on a csv file. I compiled 49 places, with the following format:

``` 
Name Address Restaurant
````

### Google Maps API

Now that I had the addresses of the compiled bubble tea list, I used the google maps API to retrieve the coordinates for each place. I accomplished this through a column manipulation that added `Latitude` and `Longitude` columns to the dataframe. Google maps allows us to input an address to the `geocoder` function and output a converted geometric object. From there, the `x.lat` and `x.lng` give us the actual coordinates.

### Shapely 

At this point, we have two new columns with the latitudes and longitudes. Using shapely, we can then convert these columns to `Point` objects. This will eventually become our geojson.

### Geojson

We have all the geometric objects needed for visualization. Before converting all of this to geojson, we create a GeoDataFrame with the `name` and `coordinate` columns. As a final step of data preparation, we convert it to geojson with the `to_json()` function. The geojson should look as follows:

```
{"type":"FeatureCollection",
  "features":[{
     "id":"0",
     "type":"Feature",
  "geometry":{
      "type": "Point",
      "coordinates":[-73.9940771,40.7301485]},
      "properties":
          {"Name":"Boba Guys"}
  }
```


### Geojsonio

And lastly, we visualize it with `geojson`! 

### Future Work

My geojson currently doesn't include the address in the label - eventually I'd like to add these along with links to the website, menu, and more. I'll also be updating with new bubble tea places as I find more. 
