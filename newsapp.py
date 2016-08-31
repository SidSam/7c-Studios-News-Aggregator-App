# IMPORTS

from flask import Flask, render_template, redirect, url_for, make_response, json, jsonify
import feedparser						# Feedparser is a universal feed parser that handles RSS 0.9x, RSS 1.0, RSS 2.0, CDF, Atom 0.3,
										# and Atom 1.0 feeds 
from math import ceil
from bs4 import BeautifulSoup			# Beautiful Soup is an HTML parser. Part of the feed returned by the Google News RSS feed is a long
										# HTML string, requiring this library to parse through it and get the required contents

app = Flask(__name__)

APPLICATION_NAME = "News Aggregator"

feeds = ['https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=e&ict=ln&output=rss&num=20',   # Entertainment
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=snc&ict=ln&output=rss&num=20', # Science
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=s&ict=ln&output=rss&num=20',   # Sports
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=w&ict=ln&output=rss&num=20',   # World
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=tc&ict=ln&output=rss&num=20'  # Technology
		]

feedtypes = ['entertainment', 'science', 'sports', 'world', 'technology']

feedlist = []    # Holds the list of the freshly retrived feeds
page_no = 1

# HTML PARSING FUNCTIONS

def soupparsedesc(descriptionhtml):
	"""Takes an HTML string as an argument and parses through it to get the brief description of the news article"""

	soup = BeautifulSoup(descriptionhtml, 'html.parser')
	fontsizelist = soup.find_all('font', {'size': '-1'})
	descriptionchild = fontsizelist[1]
	description = descriptionchild.contents[0]
	descriptionstring = unicode(description)
	return descriptionstring

def soupparseimage(descriptionhtml):
	"""Takes an HTML string as an argument and parses through it to get the image URL of the news article. Sometimes the image doesn't
	   exist in the news article, thus requiring the need for the try-except block to catch the exception"""

	soup = BeautifulSoup(descriptionhtml, 'html.parser')
	try:
		imgurl = soup.find('img', {'height': '80'})['src']
		imgurlstring = unicode(imgurl)
	except:
		imgurlstring = None
	return imgurlstring

# HELPER FUNCTIONS

def listslice():
	"""Returns the portion of the list of feeds that needs to be displayed on the current page"""

	global feedlist
	global page_no
	return feedlist[(page_no-1)*5:page_no*5]

def testforlastpage():
	global feedlist
	global page_no
	length = len(feedlist)
	last_page_no = int(ceil(float(length)/float(5)))
	if page_no == last_page_no:
		return True
	return False

# FLASK VIEW FUNCTIONS

@app.route('/')
def mainpage():
	return render_template('mainpage.html')

@app.route('/freshfeeds/<int:feedno>')
def freshfeeds(feedno):
	"""Gets the latest feeds from Google News, parses through to get the title, URL and the description and image URL (with the help of
	   Beautiful Soup). Stores each feed as a dictionary into feedlist, and returns the JSON-ified version of feedlist"""

	global feedlist
	global page_no
	feedlist = []
	rssfeed = feedparser.parse(feeds[feedno])
	for entry in rssfeed.entries:
		new_entry = {'title': entry.title, 'url': entry.link, 'description': soupparsedesc(entry.description), 'imageurl': soupparseimage(entry.description)}
		feedlist.append(new_entry)
	page_no = 1
	return json.dumps(feedlist)

@app.route('/entertainment')
def entertainment():
	freshfeeds(0)
	return redirect('/display/entertainment')

@app.route('/science')
def science():
	freshfeeds(1)
	return redirect('/display/science')

@app.route('/sports')
def sports():
	freshfeeds(2)
	return redirect('/display/sports')

@app.route('/world')
def world():
	freshfeeds(3)
	return redirect('/display/world')

@app.route('/technology')
def technology():
	freshfeeds(4)
	return redirect('/display/technology')

@app.route('/previous')
def previous():
	"""Returns the JSON-ified version of the list of feeds that are to be displayed on the previous page"""

	global page_no
	page_no -= 1
	slicedlist = listslice()
	slicedlist.append(page_no)
	is_this_last = testforlastpage()
	slicedlist.append(is_this_last)
	return json.dumps(slicedlist)

@app.route('/next')
def next():
	"""Returns the JSON-ified version of the list of feeds that are to be displayed on the next page"""

	global page_no
	page_no += 1
	slicedlist = listslice()
	slicedlist.append(page_no)
	is_this_last = testforlastpage()
	slicedlist.append(is_this_last)
	return json.dumps(slicedlist)

@app.route('/display/<string:feedtype>')
def display(feedtype):
	list_to_be_displayed_here = listslice()
	is_this_last = testforlastpage()
	feedno = 0
	if feedtype == 'science':
		feedno = 1
	elif feedtype == 'sports':
		feedno = 2
	elif feedtype == 'world':
		feedno = 3
	elif feedtype == 'technology':
		feedno = 4
	return render_template('/display.html', page_no=page_no, feedlist=list_to_be_displayed_here, is_this_last=is_this_last, feedno=feedno)
	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)