# coding=utf-8
import requests


class Airbnb(object):
    """Interface to get data from airbnb api. You can use :
    api_instance = Airbnb()
    api_instance.get_logement("Paris")
    api_instance.get_review(logement_id)
    api_instance.get_logement_details(logement_id)"""

    def get_logement_details(self, logement_id):

        try:
            url = "https://api.airbnb.com/v2/listings/" + logement_id
        except TypeError: #in case logement_id input is an integer.
            url = "https://api.airbnb.com/v2/listings/" + str(logement_id)

        params = {
            "client_id" : "3092nxybyb0otqw18e8nh5nty", # compulsory : API KEY
            "_format" : "v1_legacy_for_p3", # compulsory
            "locale" : "en-US", # optionnal from here.
            "currency" : "USD",
            "_source" : "mobile_p3",
            "number_of_guests" : "1"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return response.status_code

        return response.content

    def get_review(self, logement_id, offset):
        url = "https://api.airbnb.com/v2/reviews"
        params = {
            "client_id" : "3092nxybyb0otqw18e8nh5nty",
            "locale" : "en-US",
            "currency" : "USD",
            "_format" : "for_mobile_client",
            "_limit" : "50",
            "_offset" : offset,
            "_order" : "language",
            "listing_id" : logement_id,
            "role" : "all"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return response.status_code
        return response.content


    def get_logement(self, city, checkin, checkout, offset):
        """With this function you can get lots of infos (especially the housing
        ID), then get data about reviews or details of it.
        The method take a city name (string) as input and return a
        utf-8 encoded json string you can easily parse with json.loads() or
        a HTTP status code if an error occured."""

        url = "https://api.airbnb.com/v2/search_results"
        key1 = "3092nxybyb0otqw18e8nh5nty"
        key2 = "d306zoyjsyarp7ifhu67rjxn52tv0t20"

        params = {
            "client_id" : key1,
            "locale" : "en-US",
            "currency" : "USD",
            "_limit" : "50",
            "_format" : "for_search_results_with_minimal_pricing",
            "_offset" : offset,
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
            "checkin" : checkin,
            "checkout" : checkout,
            "sort" : "1",
            "user_lat" : "37.3398634",
            "user_lng" : "-122.0455164"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return response.status_code

        return response.content

    def get_available(self, logement_id, month, year, count):
        """Endpoint to get all availability for a precise listing.
        We neede as input the listting id, month and year to begin from
        and count as number of months to get result from.
        It returns utf-8 encoded json string to parse with json.loads() or
        an HTTP status code if the request failed."""

        url = "https://www.airbnb.fr/api/v2/calendar_months"
        params = {
            "key" : "d306zoyjsyarp7ifhu67rjxn52tv0t20",
            "currency" : "EUR",
            "locale" : "fr",
            "listing_id" : logement_id,
            "month" : month,
            "year" : year,
            "count" : count,
            "_format" : "with_conditions"
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return response.status_code
        return response.content

    def get_logement_by_gps(self, ne_lat, ne_lng, sw_lat, sw_lng, zoom, page_number, checkin=None, checkout=None):

        url = "https://www.airbnb.fr/api/v2/explore_tabs"
        params = {
            "items_per_grid" : "18",
            "key" : "d306zoyjsyarp7ifhu67rjxn52tv0t20",
            "ne_lat" : ne_lat,
            "ne_lng" : ne_lng,
            "sw_lat" : sw_lat,
            "sw_lng" : sw_lng,
            "zoom" : zoom,
            "location" : "paris",
            "search_by_map" : "true",
            "_format" : "for_explore_search_web",
            "experiences_per_grid" : "20",
            "guidebooks_per_gri" : "=20",
            "fetch_filters" : "true",
            "supports_for_you_v3" : "true",
            "screen_size" : "large",
            "timezone_offset" : "120",
            "auto_ib" : "true",
            "tab_id" : "home_tab",
            "federated_search_session_id" : "87339300-cc93-4d01-b366-dc3896f7788b",
            "_intents" : "p1",
            "currency" : "EUR",
            "locale" : "fr",
            "section_offset" : page_number - 1
        }
        if checkin and checkout:
            params['checkin'] = checkin
            params['checkout'] = checkout

        response = requests.get(url, params=params)
        if response.status_code != 200:
            return response.status_code
        return response.content

if __name__ == '__main__':
    # get_review("17834617")
    airbnb = Airbnb()
    print(airbnb.get_logement_by_gps(48.8632953507299, 2.3455012817150873, 48.86068875819463, 2.3429478187329096, 18, 2))
    # print(airbnb.get_available(17834617, 5, 2017, 4))
    # print(airbnb.get_logement_details(17834617))
    # airbnb.get_logement("Bordeaux", 1, 2)
