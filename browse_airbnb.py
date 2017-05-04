# coding=utf-8
import json
from airbnb_api import Airbnb

def get_user_infos(user_id):
    api = Airbnb()

    json_result = api.get_user_infos(user_id)
    data = json.loads(json_result)
    return data['user']

def get_listings_by_gps(ne_lat, ne_lng, sw_lat, sw_lng, zoom=18, checkin=None, checkout=None):
    api = Airbnb()

    page = 1
    last_name = ""

    while page < 20:
        print(page)
        json_result = api.get_logement_by_gps(ne_lat, ne_lng, sw_lat, sw_lng, zoom, page)
        data = json.loads(json_result)

        try:
            res = data['explore_tabs'][0]['sections'][0]['listings']
        except IndexError:
            print("no more result")
            break

        current_name = res[0]['listing']['name']
        if current_name == last_name:
            break
        last_name = current_name

        for listing in res:
            yield listing

        page += 1

def get_listings_by_city(city, checkin, checkout):
    """It is a generator, to be used like :
    for appart in get_all_result_city("Bordeaux")"""

    api = Airbnb()

    offset = 0
    last_name = ""

    while offset < 1000:
        print(offset)
        json_result = api.get_logement(city, checkin, checkout, offset)
        data = json.loads(json_result)

        #check if we have same result than last request => end result
        try:
            current_name = data['search_results'][0]['listing']['name']
        except IndexError:
            break
        if current_name == last_name:
            break
        last_name = current_name

        for appart in data['search_results']:
            yield appart

        offset += 50

def get_reviews(logement_id):
    api = Airbnb()

    offset = 0
    json_result = json.loads(api.get_review(logement_id, 0))
    nb_reviews = json_result['metadata']['reviews_count']

    while offset < nb_reviews:
        json_result = api.get_review(logement_id, offset)
        data = json.loads(json_result)

        for review in data['reviews']:
            yield review

        offset += 50

def get_details(logement_id):
    """take a logement id (string or int) as a parameter and return
    a dictionnary object with all the infos wanted"""
    api = Airbnb()

    json_result = api.get_logement_details(logement_id)
    data = json.loads(json_result)
    return data['listing']

def get_available(listing_id, month, year, count=4):
    """take a logement id (string or int) as a parameter and return
    a dictionnary object with all availability for the listing"""

    airbnb = Airbnb()
    json_result = airbnb.get_available(listing_id, month, year, count)
    data = json.loads(json_result)
    return data['calendar_months']



if __name__ == '__main__':
    # for rev in get_reviews(17834617):
    #     print(rev['comments'].encode('utf-8'))
    # for appart in get_listings_by_city("picpus", "20170505", "20170506"):
    #     print(appart['listing']['name'].encode('utf8'))
    for appart in get_listings_by_gps(48.8672,2.3626,48.8658,2.3594, 18):
        with open("appart1", "wb") as f:
            f.write(str(appart))
