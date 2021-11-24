# Import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
## Tells Flask what to display when looking at homepage
@app.route("/")
## Accomplishes the following:
def index():
    ## uses PyMongo to find Mars collection in the DB, assign mars variable
   mars = mongo.db.mars.find_one()
    ## Tells Flask to return an HTML template using an index. html , mars=mars tells Python to use the mars collection in MongoDB
   return render_template("index.html", mars=mars)

# The following code sets up the scrapping route. Route is the "button" of the web application. It will scrape updated data
## Defines the route for Flask
@app.route("/scrape")
def scrape():
    ## Assign a new variable
   mars = mongo.db.mars
    ## Assign variable to hold scraped data, refrences the scraping.py file
   mars_data = scraping.scrape_all()
    ## Adding an empty JSON object if not already there (True) new data saved
   mars.update({}, mars_data, upsert=True)
    ## Navigate the page back to see the updated content
   return redirect('/', code=302)

# Code to run Flask
if __name__ == "__main__":
   app.run()
