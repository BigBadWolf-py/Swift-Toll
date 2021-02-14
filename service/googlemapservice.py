import polyline
from googleplaces import GooglePlaces, types, lang
from common import constants
import googlemaps


gmaps = googlemaps.Client(key=constants.GOOGLE_SERVER_KEY)
google_places = GooglePlaces(constants.GOOGLE_SERVER_KEY)
RADIUS = 500 # Unit in meters


def search_nearby_gates(location):
    """
    Searches the nearby tolls based on the provided location
    :param location:
    :return: toll names
    """
    query_result = google_places.nearby_search(lat_lng=location, keyword='other', radius=RADIUS)
    if query_result.has_attributions:
        print query_result.html_attributions
    return [place.name for place in query_result.places]


def get_directions():
    directions_result = gmaps.directions("Alwar",
                                         "Faridabad")
    lat_lngs = polyline.decode(directions_result[0]['overview_polyline']['points'])
