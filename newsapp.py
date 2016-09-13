# IMPORTS

from flask import Flask, render_template, redirect, url_for, make_response, json, jsonify, request
import feedparser
from bs4 import BeautifulSoup			
from newsdb import Base, News           
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

APPLICATION_NAME = "News Aggregator"

# Connect to Database and create database session
engine = create_engine('sqlite:///news.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

feeds = ['https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=e&ict=ln&output=rss&num=20',   # Entertainment
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=snc&ict=ln&output=rss&num=20', # Science
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=s&ict=ln&output=rss&num=20',   # Sports
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=w&ict=ln&output=rss&num=20',   # World
		 'https://news.google.co.in/news/section?cf=all&pz=1&ned=in&topic=tc&ict=ln&output=rss&num=20'  # Technology
		]

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

def testforlastpage(curr_page):
	if curr_page == 4:
		return True
	return False

# FLASK VIEW FUNCTIONS

@app.route('/newsjson')
def newsjson():
	""" Gives the JSON of the database objects """

	newsfeeds = session.query(News).all()
	return jsonify(newsfeeds = [n.serialize for n in newsfeeds])

@app.route('/')
def mainpage():
	return render_template('mainpage.html')
	
@app.route('/freshfeeds/<int:feedno>')
def freshfeeds(feedno):
	"""Gets the latest feeds from Google News, parses through to get the title, URL and the description and image URL (with the help of
	   Beautiful Soup). Stores each feed as a dictionary into feedlist, and returns the JSON-ified version of feedlist"""

	rssfeed = feedparser.parse(feeds[feedno])
	session.query(News).delete()
	session.commit()
	for entry in rssfeed.entries:
		new_entry = News(title = entry.title, url = entry.link, description = soupparsedesc(entry.description), imageurl = soupparseimage(entry.description))
		session.add(new_entry)
		session.commit()
	# return json.dumps(feedlist)

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

	curr_page = request.args.get('page')
	curr_page = int(curr_page) - 1
	newsfeeds = session.query(News).slice((curr_page-1)*5, curr_page*5).all()
	newsfeeds = [n.serialize for n in newsfeeds]
	newsfeeds.append(str(curr_page))
	is_this_last = testforlastpage(curr_page)
	newsfeeds.append(is_this_last)
	return json.dumps(newsfeeds)

@app.route('/next')
def next():
	"""Returns the JSON-ified version of the list of feeds that are to be displayed on the next page"""
	curr_page = request.args.get('page')
	curr_page = int(curr_page) + 1
	newsfeeds = session.query(News).slice((curr_page-1)*5, curr_page*5).all()
	newsfeeds = [n.serialize for n in newsfeeds]
	newsfeeds.append(str(curr_page))
	is_this_last = testforlastpage(curr_page)
	newsfeeds.append(is_this_last)
	return json.dumps(newsfeeds)

@app.route('/display/<string:feedtype>')
def display(feedtype):
	newsfeeds = session.query(News).slice(0,5).all()
	return render_template('/display.html', feedlist=newsfeeds, t=t)
	
if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)