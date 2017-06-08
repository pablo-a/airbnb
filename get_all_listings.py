# coding=utf-8
import time
import json
import numpy as np
import pandas as pd
from MySQLdb import IntegrityError
from get_boundaries import get_boundaries
from pablo import Pablo
from browse_airbnb import get_listings_by_gps
from shapely.geometry import Polygon, mapping


def get_squares(city_name):

    json_file = get_boundaries(city_name)
    try:
        df = pd.read_json(json_file)
    except (ValueError, TypeError):
        return []

    coord = df['geometries'][0]['coordinates']
    flattened = [val for sublist in coord for val in sublist]
    max_coord = max(flattened, key=len)
    df = pd.DataFrame(max_coord, columns=["Lon", "Lat"])

    maxLon = df['Lon'].max()
    maxLat = df['Lat'].max()
    minLon = df['Lon'].min()
    minLat = df['Lat'].min()

    coeff_agrandissement = 1

    dLon = .95 * 0.00318646430969 * coeff_agrandissement
    dLat = .95 * 0.00137477186218 * coeff_agrandissement

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


def get_listings_from_city_name(city_name):
    bdd = Pablo()

    insert_req = """INSERT INTO airbnb (
    id_airbnb, listing_name, rate, review_nb, star_rating, bed_nb, capacity,
    room_type, instant_book, superhost, business_travel, is_new, picture_nb,
    latitude, longitude, city, date_maj)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    update_req = """UPDATE airbnb
    SET rate = %s, review_nb = %s, star_rating = %s, instant_book = %s,
    superhost = %s, business_travel = %s, is_new = %s, picture_nb = %s,
    date_maj = %s
    WHERE id_airbnb = %s"""

    lst_coordinates = get_squares(city_name)

    i = 1
    nb_squares_to_check = len(lst_coordinates)
    # loop on all squares
    for coo in lst_coordinates:
        print("\n%s/%s squares on %s" % (i, nb_squares_to_check, city_name))
        i += 1

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

            try:
                bdd.exec_req_with_args(insert_req, params)
            except IntegrityError:
                params = (rate_amount, nb_reviews, star_rating, instant_book,
                superhost, business_travel_ready, is_new, picture_nb, date_maj)
                bdd.exec_req_with_args(update_req, params)

    bdd.close()


if __name__ == '__main__':
    big_cities = ["Marseille", "Lyon", "Nice", "Montpellier",
    "Toulouse", "Nantes", "Bordeaux", "Lille", "Rennes", "Dijon", "Orleans",
    "Rouen", "Ajaccio", "Paris", "Cannes"]

    small_cities = ["Dunkerque", "Boulogne-sur-Mer", "Douai", "Lens",
    "Valenciennes", "Arras", "Amiens", "Creil", "Saint-Quentin", "Compiegne",
    "Beauvais", "Charleville-Mezieres", "Reims", "Metz", "Nancy", "Strasbourg",
    "Mulhouse", "Troyes", "Colmar", "Chalons-en-Champagne", "Auxerre",
    "Nevers", "Chalon-sur-Saone", "Mâcon", "Besançon", "Montbeliard", "Belfort",
    "Boulogne-Billancourt", "Saint-Denis", "Versailles", "Nanterre", "Creteil",
    "Meaux", "Evry", "Argenteuil", "Chartres", "Blois","Tours", "Châteauroux",
    "Bourges", "Le Havre", "Evreux", "Caen","Cherbourg-Octeville", "Alençon", "Brest",
    "Lorient", "Saint-Brieuc", "Vannes","Quimper", "Laval", "Le Mans", "Angers",
    "Saint-Nazaire", "La Roche-sur-Yon", "Cholet", "Les-Sables-d'Olonne",
    "Poitiers", "Niort","La Rochelle", "Angoulême", "Perigueux", "Agen",
    "Bayonne","Pau", "Limoges", "Brive-la-Gaillarde", "Dax", "Arcachon",
    "Mont-de-Marsan","Montauban", "Tarbes", "Albi", "Carcassonne", "Perpignan",
    "Narbonne", "Beziers", "Nîmes", "Ales", "Auch", "Sete", "Bourg-en-Bresse",
    "Roanne", "Clermont-Ferrand", "Saint-Etienne","Annecy", "Thonon-les-Bains",
    "Aix-en-Provence","Arles", "Avignon", "Cannes", "Toulon", "Gap", "Bastia",
    "Chambery", "Grenoble", "Valence france", "Chamonix","Avignon", "Toulon", "Frejus",
    "Lourdes", "Saint-Malo", "Antibes", "Biarritz", "Saint-Bon-Tarentaise",
    "Morzine", "Saintes-Maries-de-la-Mer", "Beaune", "Porto-Vecchio",
    "Aix-les-Bains", "Saint-Tropez", 'Saint-Nazaire 44600', 'Douai', 'Lens',
    'Chalon-sur-Sa\xc3\xb4ne']

    # missing = ['Douai', 'Lens', 'Chalon-sur-Sa\xc3\xb4ne', 'Saint-Nazaire']
    missing = ['Chamonix-Mont-Blanc', 'Cherbourg-Octeville', 'Saint-Bon-Tarentaise', "valence france"]

    for city in missing:
        get_listings_from_city_name(city)

    # for city in small_cities:
    #     get_listings_from_city_name(city)
    #
    # for city in big_cities:
    #     get_listings_from_city_name(city)
