# coding=utf-8
import json
from airbnb_api import Airbnb

def get_all_result_city(city):
    """kind of a generator, to be used like :
    for appart in get_all_result_city("Bordeaux")"""
    api = Airbnb()

    offset = 0
    last_name = ""

    while offset < 1000:
        json_result = api.get_logement(city, 1, 2, offset)
        data = json.loads(json_result)

        #check if we have same result than last request => end result
        current_name = data['search_results'][0]['listing']['name']
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




if __name__ == '__main__':
    for rev in get_reviews(17834617):
        print(rev['comments'].encode('utf-8'))
    # for appart in get_all_result_city("Bordeaux"):
    #     print(appart['listing']['name'].encode('utf8'))
