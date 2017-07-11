# coding=utf-8
import requests
from browse_airbnb import get_reviews
from time import strftime
from pablo import Pablo

def get_all_reviews(logement_id):
    bdd = Pablo()
    insert_query = """INSERT INTO airbnb_review_global
    (review_id, author_id, listing_id, recipient_id, content, date_creation,
    language, date_extract)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    for review in get_reviews(logement_id):
        review_id = review['id']
        author_id = review['author_id']
        listing_id = review['listing_id']
        recipient_id = review['recipient_id']
        content = review['comments']
        date_creation = review['created_at'][:10]

        language = review['language']

        params = (review_id, author_id, listing_id, recipient_id, content,
        date_creation, language, strftime("%Y%m%d"))

        bdd.exec_req_with_args(insert_query, params)

    bdd.close()

def get_some_review_paris():
    bdd = Pablo()

    i = 0
    # bdd.executerReq("SELECT distinct listing_id from airbnb_reviews_20k order by id desc")
    req = """SELECT listing_id FROM airbnb_reviews_20k WHERE listing_id NOT IN
    (SELECT DISTINCT listing_id FROM airbnb_review_global WHERE date_creation > 20170531
    AND date_creation < 20170701)"""
    bdd.executerReq(req)
    for listing in bdd.resultatReq()[::-1]:
        i += 1
        id_listing = listing[0]
        print("listing number : %s" % i)
        get_all_reviews(id_listing)

    bdd.close()


if __name__ == '__main__':
    get_some_review_paris()
