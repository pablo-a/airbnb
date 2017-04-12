# coding=utf-8
import json
from airbnb_api import Airbnb

def get_all_result_city(city):
    api = Airbnb()

    offset = 0

    while offset < 1000:
        json_result = api.get_logement(city, 1, 2, offset)
        data = json.loads(json_result)

        for i, appart in enumerate(data['search_results']):
            print(i, appart['listing']['name'].encode('utf-8'))

        next_offset = data['metadata']['pagination']['next_offset']
        
        # in case we reach the end of results.
        if next_offset = offset:
            break
        offset = next_offset

if __name__ == '__main__':
    get_all_result_city("Bordeaux")
