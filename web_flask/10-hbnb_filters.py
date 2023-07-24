#!/usr/bin/python3
"""script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
You must use storage for fetching data from the storage engine
(FileStorage or DBStorage) => from models import storage and storage.all(...)
To load all cities of a State:
If your storage engine is DBStorage, you must use cities relationship
Otherwise, use the public getter method cities
After each request you must remove the current SQLAlchemy Session:
Declare a method to handle @app.teardown_appcontext
Call in this method storage.close()
Routes:
/hbnb_filters: display a HTML page like 6-index.html, which was done during
the project 0x01. AirBnB clone - Web static
Copy files 3-footer.css, 3-header.css, 4-common.css and 6-filters.css from
web_static/styles/ to the folder web_flask/static/styles
Copy files icon.png and logo.png from web_static/images/ to the folder
web_flask/static/images
Update .popover class in 6-filters.css to allow scrolling in the popover
and a max height of 300 pixels.
Use 6-index.html content as source code for the template 10-hbnb_filters.html:
Replace the content of the H4 tag under each filter title
(H3 States and H3 Amenities) by &nbsp;
State, City and Amenity objects must be loaded from DBStorage and
sorted by name (A->Z)
You must use the option strict_slashes=False in your route definition
Import this 10-dump to have some data
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays the main HBnB filters HTML page."""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
                           states=states, amenities=amenities)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
