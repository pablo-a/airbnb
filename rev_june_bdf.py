# -*- coding: utf-8 -*-
from pablo import Pablo

def main():
    bdd = Pablo()
    insert_listing = """INSERT INTO airbnb_rev_june (listing_id, city) VALUES (%s, %s)"""

    # insertion des listings 20K
    bdd.executerReq("SELECT DISTINCT listing_id, city FROM airbnb_reviews_20k")
    listings = bdd.resultatReq()
    # print(listings)
    # bdd.cursor.executemany(insert_listing, listings)

    nb_rev = bdd.executerReq("""SELECT COUNT(id) as nb_rev, listing_id FROM airbnb_review_global
    WHERE date_creation > 20170531 and date_creation < 20170701 group by listing_id""")
    for elem in bdd.resultatReq():
        bdd.exec_req_with_args("""UPDATE airbnb_rev_june SET nb_reviews = %s
                                   WHERE listing_id = %s""", (elem[0], elem[1]))


if __name__ == '__main__':
    main()
