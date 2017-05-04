# coding=utf-8
import requests
import time
from pablo import Pablo
from browse_airbnb import get_available

def get_availability(listing_id):
    bdd = Pablo()
    insert_query = """INSERT INTO airbnb_dispo
    (listing_id, date_dispo, availability, price, date_extract)
    VALUES (%s, %s, %s, %s, %s)"""

    # init parameters
    today = time.strftime("%Y%m%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    count = 4

    calendar = get_available(listing_id, month, year, count)

    for month in calendar:
        for day in month['days']:
            date_dispo = day['date']
            availability = 1 if day['available'] else 0
            price = day['price']['local_price']

            params = (listing_id, date_dispo, availability, price, today)

            bdd.exec_req_with_args(insert_query, params)

    bdd.close()

def get_availability_paris():
    bdd = Pablo()

    bdd.executerReq("SELECT id_airbnb, listing_name FROM airbnb LIMIT 5")
    for listing in bdd.resultatReq():
        print("getting availability for %s" % listing[1])
        get_availability(listing[0])

if __name__ == '__main__':
    get_availability_paris()
