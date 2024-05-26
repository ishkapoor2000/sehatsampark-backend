from flask import Flask, render_template, request, redirect, session, url_for
from flask import jsonify
from flask_cors import CORS, cross_origin
import pymongo, json
import requests

from send_sms import send_greeting_sms
from pincode import get_nearby_areas

from datetime import datetime

app = Flask(__name__)

#CORS(app,resources={r"/api/*":{"origins":"*"}})
CORS(app)
#app.config['CORS_HEADERS']='Content-Type'

app.secret_key = "Telebuddy@123"

Private_Repl_URL = "https://21a533fb-0d65-40cf-846d-319618e7f791-00-2oe2r5586vwp8.sisko.replit.dev/"  # Found this Private URL in "Toggle Developers Tool" in "Webview" section inside "Resources" tab. Scroll a bit to find it with "https://*.id.repl.co/" or "...repl.co".

MONGO_URI = "mongodb+srv://telebuddy:telebuddy123@cluster0.sqnxktc.mongodb.net/"

# Connect to the MongoDB cluster
client = pymongo.MongoClient(MONGO_URI, connect=False)

MONGO_DATABASE = "Production"
CAMPS_MONGO_COLLECTION = "Camps"
USERS_MONGO_COLLECTION = "Users"
DOCTORS_MONGO_COLLECTION = "Doctors"
STAFF_MONGO_COLLECTION = "Staff"

# Get the database
dbs = client[MONGO_DATABASE]

camps_collection = dbs[CAMPS_MONGO_COLLECTION]
users_collection = dbs[USERS_MONGO_COLLECTION]
doctors_collection = dbs[DOCTORS_MONGO_COLLECTION]
staff_collection = dbs[STAFF_MONGO_COLLECTION]

@app.route('/')
def index():

    nearby_areas = get_nearby_areas("110089", distance=5)
    nearby_areas.append("110089")
    m_users = []
    for area in nearby_areas:
        print(area)
        matching_users = list(users_collection.find({'pincode': str(area)}))
        # matching_users = list(users_collection.find({'pincode': {'$in': list(nearby_areas)}}))
        if matching_users:
            m_users.append(matching_users[0])
            print(matching_users)

    print("\n\n>>>m_users", m_users)
    for user in m_users:
        print(user['phone_number'], user['full_name'])

    return 'SehatSampark Backend'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
