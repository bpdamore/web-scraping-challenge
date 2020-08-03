# web-scraping-challenge

In this challenge I was tasked with gathering a bunch of information on Mars, scraping the images and information, and serving it into a variable html file. 

___

Using a combination of Beautiful Soup and Splinter, I was able to scrape the images and data from Twitter, Nasa, etc.

The [Mars Scrape](Missions_to_Mars/mars_scrape.py) python file has the scripts needed to scrape the images and data. The Scrape function returns a dictionary of the results. 

The [app.py](Missions_to_Mars/app.py) file uses a flask server to serve two pages:
* The home page that displays the scraped information
* The scrape page that starts the retrieval of information

The scrape function from the Mars Scrape file is imported into the app.py file, and the returned dictionary of data is pushed into a Mongo Database. 

The [index.html](Missions_to_Mars/templates/index.html) file is the main landing page. When the Flask server is running, it pulls the latest data from the Mongo Database and displays it. 

While all this may take some time, if you click the button on the page, it should pull all the data and load! 

---
However, if you'd rather look at the page without refreshing it, here is a screenshot of the page. 

![screenshot](Images/scraping_mars_screenshot.png)