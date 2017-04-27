# coding=utf-8
from browse_airbnb import get_listings_by_gps
from pablo import Pablo
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, mapping


def get_square():
    df = pd.read_json('paris_boudaries.json')
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
    print(l)
    return l



def search_on_all_squares():
    bdd = Pablo()

    insert_req = """INSERT INTO airbnb_test
    (name_logement, id_airbnb, nb_reviews)
    VALUES (%s, %s, %s)"""

    lst_coordinates = get_square()

    # loop on all squares
    for coo in lst_coordinates:

        for appart in get_listings_by_gps(coo[2], coo[3], coo[0], coo[1]):
            nb_reviews = appart['listing']['reviews_count']
            name = appart['listing']['name']
            id_airbnb = appart['listing']['id']

            print(name.encode('utf-8'))

            params = (name, id_airbnb, nb_reviews)
            bdd.exec_req_with_args(insert_req, params)

    bdd.close()

if __name__ == '__main__':
    search_on_all_squares()
