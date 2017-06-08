# coding=utf-8
import requests
import time
from pablo import Pablo
from browse_airbnb import get_available

def get_availability(listing_id):
    bdd = Pablo()
    insert_query = """INSERT INTO airbnb_dispo_test_20000
    (listing_id, date_dispo, availability, price, date_extract)
    VALUES (%s, %s, %s, %s, %s)"""
    
    update_query = """UPDATE airbnb_dispo
    SET availability = %s, price = %s, date_extract = %s
    WHERE listing_id = %s AND date_dispo = %s"""

    # init parameters
    today = time.strftime("%Y%m%d")
    month = time.strftime("%m")
    year = time.strftime("%Y")
    count = 2

    calendar = get_available(listing_id, month, year, count)
    if calendar is None:
        return 0
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

    bdd.executerReq("SELECT id_airbnb FROM test")
    lenght = len(bdd.resultatReq())
    
    i = 1
    bdd.executerReq("SELECT id_airbnb FROM test")
    for listing in bdd.resultatReq():
        print("%s on %s listings" % (i, lenght))
        get_availability(listing[0])
        i += 1

if __name__ == '__main__':
    get_availability_paris()
