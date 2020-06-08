def scrape():
    # Import Dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    import time

    # Create a dictionary for the app

    mars_scrape = {}

    ######################
    ### MARS HEADLINES ###
    ######################

    # Set up splinter variables. Make it headless so it doesn't open a browser each time.
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    # Send it to the nasa site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Convert the browser's webpage to html and turn it into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the first title and body
    news_title = soup.find("div", class_="list_text").find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    mars_scrape["news_title"] = news_title
    mars_scrape["news_p"] = news_p

    ###################
    ### MARS IMAGES ###
    ###################

    # Do it again for the images
    url_base = "https://www.jpl.nasa.gov"
    url = url_base+"/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Turn it into soup! 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # The image is in a style tag, so let's grab that. 
    bg_img = soup.find("article", class_="carousel_item")

    # Now let's split it out of the style tag
    # Convert it to a string, and split it on the ' around the url
    image = (str(bg_img)).split("('", 1)[1].split("')")[0]

    # Get a full url by combining it with the base url
    featured_image_url = url_base+image

    mars_scrape["featured_image_url"] = featured_image_url


    ####################
    ### MARS WEATHER ###
    ####################

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    # Turn it into soup! 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    tweet_article = soup.find("article", {"role" : "article", "tabindex":0})
    spans = tweet_article.find_all("span")
    for span in spans:
        if span.text[0:7] == "InSight":
            mars_weather = span.text
        else:
            pass

    mars_scrape["mars_weather"] = mars_weather


    ##################
    ### MARS FACTS ###
    ##################

    url = "https://space-facts.com/mars/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    df = df[0]
    mars_info_table = df.to_html(index=False)

    mars_scrape["mars_info_table"] = mars_info_table


    ########################
    ### MARS HEMISPHERES ###
    ########################

    # Save the base url to add to the img url later
    url_base = "https://astrogeology.usgs.gov"

    # Create a list of urls to scrape through
    url_list = ["https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced", "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced", "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced", "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"]

    # Create an empty list to store each image url in
    hemisphere_image_urls = []

    # Go through the different urls and scrape what is needed. Add to a dictionary and append to the list. 
    for url in url_list:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Grab the title of the image
        title = soup.find("h2", class_="title").text
        # Create the full image url by combining the url base with the image url
        img = url_base + (soup.find("img", class_="wide-image")["src"])
        # Create a dictionary of the title and the url
        img_dict = {
            "title" : title,
            "image_url" : img
        }
        # Throw that dictionary into a list for parsing later. 
        hemisphere_image_urls.append(img_dict)

    mars_scrape["hemisphere_images"] = hemisphere_image_urls

    return mars_scrape