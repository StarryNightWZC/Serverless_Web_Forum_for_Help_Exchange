from flask import (render_template, url_for, flash, current_app,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
#from flaskblog import db
from flask_googlemaps import GoogleMaps, Map
from flask_googlemaps import get_address, get_coordinates
from geopy.distance import great_circle
import json

maps = Blueprint('maps', __name__)

@maps.route("/map/offerhelp", methods=['GET', 'POST'])
def map_offerhelp():
    locations = []  # long list of coordinates
    place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], 'M4Y0C4')
    place['infobox'] = "<b>Hello World</b>"
    locations.append(place)

    place = get_coordinates(current_app.config['GOOGLEMAPS_KEY'], 'M4Y0C4')
    place['infobox'] = "<b>Hello World from other place</b>"
    locations.append(place)

    map_offerhelp = Map(
        identifier="map_offerhelp",
        style=(
            "height:350px;"
            "width:700px;"
        ),
        lat=locations[0]['lat'],
        lng=locations[0]['lng'],
        markers=[(loc['lat'], loc['lng'], loc['infobox']) for loc in locations],
        fit_markers_to_bounds=True
    )
    place1 = [locations[0]['lat'], locations[0]['lng']]
    place2 = [locations[1]['lat'], locations[1]['lng']]
    print("Distance:{}km".format(great_circle(place1, place2).km))
    return render_template('map_offerhelp.html', map_offerhelp=map_offerhelp)