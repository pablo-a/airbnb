# coding=utf-8
import requests
from pablo import Pablo
from browse_airbnb import get_details

def get_listing_info(listing_id):
    bdd = Pablo()
    update_query = """UPDATE airbnb
    SET id_owner = %s, min_night = %s, max_night = %s, property_type = %s,
    calendar_updated = %s, bed_type = %s, H24_checking = %s
    WHERE id_airbnb = %s"""

    infos = get_details(listing_id)
    owner_id = infos['user_id']
    min_night = infos['min_nights']
    max_night = infos['max_nights']
    property_type = infos['property_type']
    calendar_updated = infos["calendar_updated_at"]
    bed_type = infos['bed_type']
    H24_checking = 1 if 43 in infos['amenities'].values() else 0

    params = (owner_id, min_night, max_night, property_type, calendar_updated,
    bed_type, H24_checking, listing_id)

    bdd.exec_req_with_args(update_query, params)


if __name__ == '__main__':
    get_listing_info(629248)
