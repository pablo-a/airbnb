# Airbnb API usage

There are a lot of endpoints available, here only 2 are explained as examples
but you can find all wrapper function on airbnb_api.py file.

## availability of a listing

HTTP Method : ``GET``  
Endpoint : https://www.airbnb.fr/api/v2/calendar_months  
#### Required Parameters :
- key : API Key (ex : `key=3092nxybyb0otqw18e8nh5nty`)
- listing_id : listing to get availability from (ex : `listing_id=432044`)
- count : number of months (`count=3`)
- month : month to start from (`month=7`)
- year : year to start from (`year=2017`)

#### Optionnal Parameters :
- currency => EUR, ...
- locale => fr, ...
- _format => _format=with_conditions_

#### example full request :  
`GET https://www.airbnb.fr/api/v2/calendar_months?key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=EUR&locale=fr&listing_id=432044&month=7&year=2017&count=3&_format=with_conditions`


## Search Listings by GPS coordinates
It is based on 2 points (North-East and South-West) and a zoom.

HTTP Method : `GET`  
Endpoint : `https://www.airbnb.fr/api/v2/explore_tabs`

#### Required Parameters :
- key = API key
- search_by_map = true
- ne_lat = 48.88204456969935
- ne_lng = 2.3759465821207186
- sw_lat = 48.84033871460492
- sw_lng = 2.335091174405875
- zoom = 14

#### Optionnal Parameter or Parameter i dont understand :
- items_per_grid= 18
- experiences_per_grid = 20
- guidebooks_per_grid = 20
- fetch_filters = true
- supports_for_you_v3 = true
- screen_size = large
- timezone_offset = 120
- auto_ib = true
- tab_id = home_tab
- location = paris
- federated_search_session_id=87339300-cc93-4d01-b366-dc3896f7788b
- _intents = _p1_
- currency=EUR
- locale=fr



#### example full request :  
`https://www.airbnb.fr/api/v2/explore_tabs?version=1.1.0
&_format=for_explore_search_web&
items_per_grid=18&
experiences_per_grid=20&
guidebooks_per_grid=20&
fetch_filters=true&
supports_for_you_v3=true&
screen_size=large&
timezone_offset=120&
auto_ib=true&
tab_id=home_tab&
location=paris&
ne_lat=48.88204456969935&
ne_lng=2.3759465821207186&
search_by_map=true&
sw_lat=48.84033871460492&
sw_lng=2.335091174405875&
zoom=14&
federated_search_session_id=87339300-cc93-4d01-b366-dc3896f7788b&
_intents=p1&
key=d306zoyjsyarp7ifhu67rjxn52tv0t20&currency=EUR&locale=fr`
