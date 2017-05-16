# coding=utf-8
import json
import requests
import re
import sys

def get_boundaries(city_name):

    # get all results from city_name and chose one.
    response = requests.get("http://nominatim.openstreetmap.org/search.php?q=%s&polygon_geojson=1&viewbox=" % city_name)
    links = re.findall(ur'href="details.php\?place_id=(\d+)"', response.content.decode('utf-8'))
    if not links:
        return None

    for index, link in enumerate(links):

        city_id = re.sub(ur"(\d+)", ur"\1", link)

        # second request with city_id return us more detail (the city id here)
        response = requests.get(u'http://nominatim.openstreetmap.org/details.php?place_id=%s' % city_id)
        data_decoded = response.content.decode('utf-8')

        # if we dont get a polygon we go to next result.
        if not re.findall(ur"Coverage.*Polygon", data_decoded):
            continue

        print(u"\nget result number %d from openstreetmap" % (index + 1))

        # i think this try/except block is useless now since we filtered not polygons results
        city_id = re.findall(ur"OSM.*relation (\d+)", data_decoded)
        try:
            city_id = re.sub(ur'OSM.*relation (\d+)', ur"\1", city_id[0])
        except IndexError:
            sys.exit("Result doesnt look like a city")
        break

    # now get boundaries thx to the city_id
    try:
        response_json = requests.get("http://polygons.openstreetmap.fr/get_geojson.py?id=%s&params=0" % city_id)
    except requests.exceptions.ConnectionError:
        return None


    return response_json.content
