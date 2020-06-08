from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from mars_scrape import scrape

app = Flask(__name__)

# Set up the connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/scraper")
def scraper():
    mars_scrape = mongo.db.mars_scrape
    mars_data = scrape()
    mars_scrape.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

@app.route("/")
def index():
    mars_scrape = mongo.db.mars_scrape.find_one()
    return render_template("index.html", mars_scrape=mars_scrape)

if __name__ == "__main__":
    app.run(debug=True)