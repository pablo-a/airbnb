# coding=utf-8
import time
import json
import numpy as np
import pandas as pd
from pablo import Pablo
from browse_airbnb import get_listings_by_gps
from shapely.geometry import Polygon, mapping


def get_square():
    ville = 'cities\paris_boudaries'
    df = pd.read_json(ville + '.json')
    coord = df['geometries'][0]['coordinates']
    flattened = [val for sublist in coord for val in sublist]
    max_coord = max(flattened, key=len)
    df = pd.DataFrame(max_coord, columns=["Lon", "Lat"])

    maxLon = df['Lon'].max()
    maxLat = df['Lat'].max()
    minLon = df['Lon'].min()
    minLat = df['Lat'].min()

    dLon = .95*0.00318646430969
    dLat = .95*0.00137477186218

    shiftLon = .5 * (minLon + dLon * (int((maxLon - minLon) / dLon) + 1) - maxLon)
    shiftLat = .5 * (minLat + dLat * (int((maxLat - minLat)  /dLat) + 1) - maxLat)

    def Lon(i):
        return minLon + i * dLon - shiftLon

    def Lat(j):
        return minLat + j * dLat - shiftLat

    l = []
    city = Polygon(max_coord)

    ord = range(int((maxLat-minLat) / dLat) + 1)
    abs = range(int((maxLon-minLon) / dLon) + 1)

    for j in ord:
        for i in abs:
            SLon = Lon(i)
            NLon = SLon + dLon
            SLat = Lat(j)
            NLat = SLat + dLat
            window = Polygon([[SLon,SLat],[NLon,SLat],[NLon,NLat],[SLon,NLat]])
            if window.intersection(city):
                l.append([SLat,SLon,NLat,NLon])
    return l


def search_on_all_squares():
    bdd = Pablo()

    insert_req = """INSERT INTO airbnb (
    id_airbnb, listing_name, rate, review_nb, star_rating, bed_nb, capacity,
    room_type, instant_book, superhost, business_travel, is_new, picture_nb,
    latitude, longitude, city, date_maj)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    lst_coordinates = get_square()

    # loop on all squares
    for coo in lst_coordinates:

        for appart in get_listings_by_gps(coo[2], coo[3], coo[0], coo[1]):

            infos = appart['listing']

            id_airbnb = appart['listing']['id']
            name = infos['name']
            rate_amount = appart['pricing_quote']['rate']['amount']
            nb_reviews = infos['reviews_count']
            star_rating = infos['star_rating']
            bed_nb = infos['beds']
            capacity = infos['person_capacity']
            room_type = infos['room_type']
            instant_book = appart['pricing_quote']['can_instant_book']
            superhost = infos['is_superhost']
            business_travel_ready = infos['is_business_travel_ready']
            is_new = infos['is_new_listing']
            picture_nb = infos['picture_count']
            latitude = infos['lat']
            longitude = infos['lng']
            city = infos['localized_city']
            date_maj = time.strftime("%Y%m%d")

            print(name.encode('utf-8'))

            params = (id_airbnb, name, rate_amount, nb_reviews, star_rating,
            bed_nb, capacity, room_type, instant_book, superhost,
            business_travel_ready, is_new, picture_nb, latitude, longitude,
            city, date_maj)

            bdd.exec_req_with_args(insert_req, params)

    bdd.close()


if __name__ == '__main__':
    search_on_all_squares()
