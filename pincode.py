# import requests

# pincode = "110089"
# distance = "5"
# print("pincode[0:2]", pincode[0:3])

# url = f"https://india-pincode-with-latitude-and-longitude.p.rapidapi.com/api/v1/pincode/{pincode}/nearby"

# headers = {
#     "X-RapidAPI-Key": "03a4975f59mshfcc9b734480a538p1354ecjsn0bf5001701d3",
#     "X-RapidAPI-Host":
#     "india-pincode-with-latitude-and-longitude.p.rapidapi.com"
# }

# response = requests.post(url, headers=headers)
# areas = response.json()

# for code in areas["areas"]:
# 	distance_km = round(float(code["distance"]) * 1.609344, 2)
# 	if str(code["pincode"]).startswith(pincode[0:2]) and distance_km <= int(distance):
# 		print(f'{code["pincode"]} - {code["area"]}, {code["state"]} {distance_km}KM [{code["lat"]}, {code["lng"]}]')

import requests

def get_nearby_areas(pincode, distance=5):
    """Retrieves nearby areas within a specified distance from a given pincode.

    Args:
        pincode (str): The pincode for which to find nearby areas.
        distance (int): The maximum distance in kilometers for nearby areas.
        api_key (str): Your RapidAPI key for the API.
        host (str): The RapidAPI host for the API.

    Returns:
        list: A list of dictionaries, each containing details of a nearby area:
            - pincode (str)
            - area (str)
            - state (str)
            - distance_km (float): Distance in kilometers from the input pincode
            - lat (float): Latitude
            - lng (float): Longitude
    """
    api_key =  "03a4975f59mshfcc9b734480a538p1354ecjsn0bf5001701d3"
    host = "india-pincode-with-latitude-and-longitude.p.rapidapi.com"  # Replace if different


    url = f"https://{host}/api/v1/pincode/{pincode}/nearby"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }

    response = requests.post(url, headers=headers)
    areas = response.json()

    nearby_areas = []
    for code in areas["areas"]:
        distance_km = round(float(code["distance"]) * 1.609344, 2)
        if str(code["pincode"]).startswith(pincode[0:2]) and distance_km <= distance:
            nearby_areas.append(code["pincode"])

    print("nearby_areas", nearby_areas)
    return nearby_areas

# # Example usage
# pincode = "201301"
# distance = 5

# nearby_areas = get_nearby_areas(pincode, distance)
# print("Nearby areas:")
# for area in nearby_areas:
#     print(area)
