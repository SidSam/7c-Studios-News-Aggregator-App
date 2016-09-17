# 7c-Studios-News-Aggregator-App

Built using Flask, SQLAlchemy and jQuery

Gets RSS feeds from Google News, parses through them using BeautifulSoup and displays them

The landing page has 5 categories to choose from. Clicking on a category takes you to a display page, where 
20 RSS feeds are divided up into 4 chunks of 5 each, which are served using AJAX

Once on the display page, if the user stays for 10 minutes, the page refreshes itself with fresh RSS feeds (Personally don't 
like this feature)

Going to `/newsjson` gives you the JSON structure of the database with the most current feeds

Had initially made this for an interview with a startup, later turned out to be a great learning experience
