from wifi_deb import wifi_users
from read_csv import aps_stations

aps, stations = aps_stations()
w_users,router_MAC = wifi_users()




def test():
 stations_with_names = []
 for station in stations:
     if station[4].lower()[0:8]==router_MAC.lower()[0:8]:
        for user in w_users:
            if(station[0] is not None and user[1] is not None and (station[0].lower() == user[1].lower())):
                station += [user[0], user[2]]
                stations_with_names += [station]
 return stations_with_names

print(test())