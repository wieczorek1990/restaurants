import flask


app = flask.Flask(__name__)


@app.route("/restaurants/near/<float:lat>/<float:long>")
def near_lat_long(lat, long):
    return "Hello World!"


@app.route("/restaurants/near/<string:address>")
def near_address(address):
    return "Hello World!"


@app.route("/restaurants/combo/<string:cusine_a><string:cusine_b>")
def combo(cusine_a, cusine_b):
    return "Hello World!"
