# coding=utf-8
from browse_airbnb import get_listings_by_gps
from pablo import Pablo
import time
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, mapping


def get_square():
    df = pd.read_json('paris_boudaries.json')

    nb_polygon = len(df['geometries'][0]['coordinates'])
    lens = [len(df['geometries'][0]['coordinates'][i][0]) for i in range(nb_polygon)]

    biggest_poly_index = lens.index(max(lens))
    biggest_poly = df['geometries'][0]['coordinates'][biggest_poly_index][0]


    coord = df['geometries'][0]['coordinates'][0][0]
    df = pd.DataFrame(coord, columns=["Lon", "Lat"])
    # df.describe()

    maxLon = df['Lon'].max()
    maxLat = df['Lat'].max()
    minLon = df['Lon'].min()
    minLat = df['Lat'].min()

    dLon = 0.00318646430969
    dLat = 0.00137477186218

    shiftLon = .5 * (minLon + dLon * (int((maxLon - minLon) / dLon) + 1) - maxLon)
    shiftLat = .5 * (minLat + dLat * (int((maxLat - minLat)  /dLat) + 1) - maxLat)

    def Lon(i):
        return minLon + i * dLon - shiftLon

    def Lat(j):
        return minLat + j * dLat - shiftLat

    l = []
    city = Polygon(coord)

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

    insert_req = """INSERT INTO airbnb (id_airbnb, listing_name, rate,
    review_nb, star_rating, city, superhost, bed_nb, picture_nb,
    latitude, longitude, business_travel, is_new, date_maj,
    instant_book)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    lst_coordinates = get_square()

    # loop on all squares
    for coo in lst_coordinates:

        for appart in get_listings_by_gps(coo[2], coo[3], coo[0], coo[1]):

            date_maj = time.strftime("%Y%m%d")
            instant_book = appart['pricing_quote']['can_instant_book']
            rate_amount = appart['pricing_quote']['rate']['amount']
            infos = appart['listing']
            is_new = infos['is_new_listing']
            nb_reviews = infos['reviews_count']
            star_rating = infos['star_rating']
            name = infos['name']
            capacity = infos['person_capacity']
            city = infos['localized_city']
            superhost = infos['is_superhost']
            room_type = infos['room_type']
            bed_nb = infos['beds']
            picture_nb = infos['picture_count']
            latitude = infos['lat']
            longitude = infos['lng']
            business_travel_ready = infos['is_business_travel_ready']
            id_airbnb = appart['listing']['id']

            # gps coordiantes => exact address.
            # thx to government API
            url_req = "http://api-adresse.data.gouv.fr/reverse/?lon=%s&lat=%s" % (longitude, latitude)
            address_json = json.loads(requests.get(url_req))
            street = address_json['features'][0]['properties']['name']
            city = address_json['features'][0]['properties']['city']
            postcode = address_json['features'][0]['properties']['postcode']
            http://api-adresse.data.gouv.fr/reverse/?lon=2.37&lat=48.357

            print(name.encode('utf-8'))

            params = (id_airbnb, name, rate_amount, nb_reviews, star_rating,
            city, superhost, bed_nb, picture_nb, latitude, longitude,
            business_travel_ready, is_new, date_maj, instant_book)

            bdd.exec_req_with_args(insert_req, params)

    bdd.close()

if __name__ == '__main__':
    search_on_all_squares()
