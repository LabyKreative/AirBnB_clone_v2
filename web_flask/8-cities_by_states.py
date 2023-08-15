#!/usr/bin/python3
"""script that starts a Flask web application
web application must be listening on 0.0.0.0, port 5000
You must use storage for fetching data from the storage engine
(FileStorage or DBStorage) => from models import storage and storage.all(...)
After each request you must remove the current SQLAlchemy Session:
Declare a method to handle @app.teardown_appcontext
Call in this method storage.close()
Routes:
/states_list: display a HTML page: (inside the tag BODY)
H1 tag: “States”
UL tag: with the list of all State objects present in DBStorage sorted
by name (A->Z) tip
LI tag: description of one State: <state.id>: <B><state.name></B>
Import this 7-dump to have some data
You must use the option strict_slashes=False in your route definition

IMPORTANT:
Make sure you have a running and valid setup_mysql_dev.sql in your
AirBnB_clone_v2 repository (Task)
Make sure all tables are created when you run:
echo "quit" | HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db HBNB_TYPE_STORAGE=db
./console.py
"""
from models import storage
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = False


@app.route("/cities_by_states", strict_slashes=False)
def cities_by_states():
    """HTML page with a list of all states and related cities"""
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
