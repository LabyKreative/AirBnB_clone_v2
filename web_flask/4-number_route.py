#!/usr/bin/python3
"""script that starts a Flask web application:
web application must be listening on 0.0.0.0, port 5000
Routes:
/: display “Hello HBNB!”
/hbnb: display “HBNB”
/c/<text>: display “C ”, followed by the value of the text variable
(replace underscore _ symbols with a space )
/python/(<text>): display “Python ”, followed by the value of the text
variable (replace underscore _ symbols with a space )
The default value of text is “is cool”
/number/<n>: display “n is a number” only if n is an integer
You must use the option strict_slashes=False in your route definition
"""
from flask import Flask
from flask import abort

app = Flask(__name__)
app.debug = False


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Displays "Hello HBNB!"."""
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Displays "HBNB"."""
    return ("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Displays "C" followed by the value of <text>."""
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text="is cool"):
    """Displays "Python" followed by the value of <text>."""
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Displays "n is a number" only if n is an integer."""
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
