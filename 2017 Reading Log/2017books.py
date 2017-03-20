from pocket import Pocket, PocketException
from datetime import datetime
import json


p = Pocket(
consumer_key='my_consumer_key',
access_token='my_access_token'
)

"""
since: pocket uses unix epoch time, 1483246800 is time stamp for 2017 NYD
state: 1 indicates an article i've read
"""
lis = p.retrieve(since=1483246800, state=1)


# for data storage purposes - outputs a json file of the data i pulled
with open('output.json', 'w') as f:
    json.dump(lis, f)


words = 0 # stores number of words read 
for i in lis['list']:
	if 'word_count' in lis['list'][str(i)].keys():
		words += int(lis['list'][str(i)]['word_count'])

# average book is 55000 words
books = words / 55000
