# coding=utf-8
import json
from airbnb_api import Airbnb

def get_all_result_city(city, checkin, checkout):
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

    json_result = json.loads(api.get_logement_details(logement_id))
    data = json.loads(json_result)
    return data['listing']



if __name__ == '__main__':
    # for rev in get_reviews(17834617):
    #     print(rev['comments'].encode('utf-8'))
    for appart in get_all_result_city("picpus", "20170505", "20170506"):
        print(appart['listing']['name'].encode('utf8'))
