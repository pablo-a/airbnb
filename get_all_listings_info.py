# coding=utf-8
import requests
import dateparser
import json
from pablo import Pablo
from browse_airbnb import get_details

def update_listing_info(listing_id, lat, lng):
    bdd = Pablo()
    update_query = """UPDATE airbnb
    SET id_owner = %s, min_night = %s, max_night = %s, property_type = %s,
    calendar_update = %s, bed_type = %s, H24checking = %s, self_checking = %s
    WHERE id_airbnb = %s"""

    # appel à l'interface API
    # en cas d'erreur on ne fait rien.
    infos = get_details(listing_id)
    if not infos:
        return

    # ctrl + maj + /
    # gps coordinates => exact address.
    # thx to government API
    url_req = "http://api-adresse.data.gouv.fr/reverse/?lon=%s&lat=%s" % (lng, lat)
    response = requests.get(url_req)
    address_json = json.loads(response.content)
    try:
        street = address_json['features'][0]['properties']['name']
        postcode = address_json['features'][0]['properties']['postcode']
        city = address_json['features'][0]['properties']['city']
    except IndexError:
        pass
    else:
        bdd.exec_req_with_args("""UPDATE airbnb SET street = %s, city = %s,
        postcode = %s WHERE id_airbnb = %s""", (street, city, postcode, listing_id))

    # récupération des champs interessants
    owner_id = infos['user_id']
    min_night = infos['min_nights']
    max_night = infos['max_nights']
    property_type = infos['property_type']
    try:
        calendar_updated = infos["calendar_updated_at"]
        calendar_updated = dateparser.parse(calendar_updated).date()
    except AttributeError:
        calendar_updated = None
    bed_type = infos['bed_type']
    H24_checking = 1 if 43 in infos['amenities_ids'] else 0
    self_checking = 1 if "Self Check-In" in infos['amenities'] else 0


    # execution requête
    params = (owner_id, min_night, max_night, property_type, calendar_updated,
    bed_type, H24_checking, self_checking, listing_id)
    bdd.exec_req_with_args(update_query, params)
    bdd.close()

def update_paris_listings():
    bdd = Pablo()
    bdd.executerReq("SELECT id_airbnb, listing_name, latitude, longitude from airbnb")
    for listing in bdd.resultatReq():
        print("updating %s" % listing[1])
        update_listing_info(listing[0], listing[2], listing[3])

    bdd.close()


if __name__ == '__main__':
    update_paris_listings()
