from pocket import Pocket, PocketException
from datetime import datetime
import json
import os
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import random

p = Pocket(
consumer_key='my_key',
access_token='my_token'
)

# this retrieves all my readings since jan 1, 2017
lis = p.retrieve(since=1483246800, state=1)

# i save this to a json file
with open('output.json', 'w') as f:
    json.dump(lis, f)

# this is for the word couunt
words = 0 
words2 = ""
for i in lis['list']: # iterate through IDs
	if 'word_count' in lis['list'][str(i)].keys(): # make sure there's a wordcount
		words += int(lis['list'][str(i)]['word_count']) # adds the word count to total count
	elif 'given_title' in lis['list'][str(i)].keys():
		words2 += " " + lis['list'][str(i)]['given_title']

# write words to text file
text_file = open("words2.txt", "w")
text_file.write(words2)
text_file.close()

# average book is 55000 words, so divide the total to get the number of books ive read this year so far
books = words / 55000
 
# This is the function to generate colors for the words, specifically purple shades
def color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return ("hsl(%d, %d%%, %d%%)" % (random.randint(250, 280), random.randint(30, 100), random.randint(30, 50)))

stopwords = set(STOPWORDS) # get rid of these words from wordcloud

# article sources
nsw = ["medium", "new", "york", "times", "stop"] 
for i in nsw:
	stopwords.add(i)

# amaticSC is the font I chose
wordcloud = WordCloud(stopwords=stopwords, font_path='./AmaticSC-Regular.ttf', background_color="white")

# actually generates the words
wordcloud.generate(words)

# this selects the colors and displays
plt.imshow(wordcloud.recolor(color_func=color_func, random_state=3))
plt.axis("off")
plt.show()

# lis retrieves the json for all my favorite articles
lis = p.retrieve(favorites=1)

# write the json to a file for safe keeping
with open('favorites.json', 'w') as f:
    json.dump(lis, f)
    f.close()

# attaches the words to the a string
words = ""
for i in lis['list']:
	if 'given_title' in lis['list'][str(i)].keys():
		words += " " + lis['list'][str(i)]['given_title']

# write words to text file
text_file = open("words.txt", "w")
text_file.write(words)
text_file.close()


wordcloud = WordCloud(stopwords=stopwords, font_path='./AmaticSC-Regular.ttf.ttf', background_color="white")
wordcloud.generate(words)

plt.imshow(wordcloud.recolor(color_func=color_func, random_state=3))
plt.axis("off")
plt.show()

