# coding=utf-8
import requests
import dateparser
from pablo import Pablo
from browse_airbnb import get_details

def update_listing_info(listing_id):
    bdd = Pablo()
    update_query = """UPDATE airbnb
    SET id_owner = %s, min_night = %s, max_night = %s, property_type = %s,
    calendar_update = %s, bed_type = %s, H24checking = %s
    WHERE id_airbnb = %s"""

    # appel à l'interface API
    infos = get_details(listing_id)

    # récupération des champs interessants
    owner_id = infos['user_id']
    min_night = infos['min_nights']
    max_night = infos['max_nights']
    property_type = infos['property_type']
    calendar_updated = infos["calendar_updated_at"]
    calendar_updated = dateparser.parse(calendar_updated).date()
    bed_type = infos['bed_type']
    H24_checking = 1 if 43 in infos['amenities'] else 0

    # execution requête
    params = (owner_id, min_night, max_night, property_type, calendar_updated,
    bed_type, H24_checking, listing_id)
    bdd.exec_req_with_args(update_query, params)
    bdd.close()

def update_paris_listings():
    bdd = Pablo()
    bdd.executerReq("SELECT id_airbnb, listing_name from airbnb limit 10")
    for listing in bdd.resultatReq():
        print("updating %s" % listing[1])
        update_listing_info(listing[0])

    bdd.close()


if __name__ == '__main__':
    update_paris_listings()
