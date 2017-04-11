# coding=utf-8
import requests




def get_review(logement_id):
    url = "https://api.airbnb.com/v2/reviews"
    params = {
        "client_id" : "3092nxybyb0otqw18e8nh5nty",
        "locale" : "en-US",
        "currency" : "USD",
        "_format" : "for_mobile_client",
        "_limit" : "20",
        "_offset" : "0",
        "_order" : "language",
        "listing_id" : logement_id,
        "role" : "all"
    }

    response = requests.get(url, params=params)
    print(response.status_code)
    with open('reviews.json', 'wb') as f:
        f.write(response.content)

def get_logement(city):
    url = "https://api.airbnb.com/v2/search_results"
    key1 = "3092nxybyb0otqw18e8nh5nty"
    key2 = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

    params = {
        "client_id" : key2 + "cool",
        "locale" : "en-EN",
        "currency" : "USD",
        "_limit" : "50",
        "_format" : "for_search_results_with_minimal_pricing",
        "_offset" : "0",
        "fetch_facets" : "true",
        "guests" : "1",
        "ib" : "false",
        "ib_add_photo_flow" : "true",
        "location" : city,
        "min_bathrooms" : "0",
        "min_bedrooms" : "0",
        "min_beds" : "1",
        "min_num_pic_urls" : "0",
        "price_max" : "5000",
        "price_min" : "0",
        "checkin" : "2017-06-03",
        "checkout" : "2017-06-04",
        "sort" : "1",
        "user_lat" : "37.3398634",
        "user_lng" : "-122.0455164"
    }

    response = requests.get(url, params=params)
    print(response.status_code)
    print(response.headers)

    with open('test.json', 'wb') as f:
        f.write(response.content)

if __name__ == '__main__':
    # get_review("17834617")
    get_logement("Bordeaux")
