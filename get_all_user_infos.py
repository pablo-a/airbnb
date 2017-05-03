# coding=utf-8
import requests
from browse_airbnb import get_user_infos
from pablo import Pablo

def get_user(user_id):
    bdd = Pablo()
    insert_query = """INSERT INTO airbnb_user
    (user_id, name, creation_date, response_rate, response_time, listing_nb,
    description)
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    user = get_user_infos(user_id)

    user_id = user['id']
    name = user['smart_name']
    creation_date = user['created_at'][:10]
    response_rate = user['response_rate']
    response_time = user['response_time']
    listing_nb = user['listings_count']
    description = user['about']

    params = (user_id, name, creation_date, response_rate, response_time,
    listing_nb, description)

    bdd.exec_req_with_args(insert_query, params)
    bdd.close()

def get_users_paris():
    bdd = Pablo()

    bdd.executerReq("SELECT DISTINCT author_id FROM airbnb_review")
    for user in bdd.resultatReq():
        get_user(user)

    bdd.executerReq("SELECT DISTINCT recipient_id FROM airbnb_review")
        for user in bdd.resultatReq():
            get_user(user)

    bdd.close()
