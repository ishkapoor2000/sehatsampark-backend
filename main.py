from flask import Flask, render_template, request, redirect, session, url_for
from flask import jsonify
import pymongo, json
from datetime import datetime

app = Flask(__name__)
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

# 404 Error Handler
@app.errorhandler(404)
def not_found_error(error):
	return render_template('404.html'), 404

# Define the custom error handler for 503 errors
@app.errorhandler(503)
def handle_503_error(e):
	return render_template('503.html'), 503

# Define the custom error handler for 500 errors
@app.errorhandler(500)
def handle_500_error(e):
	return render_template('500.html'), 500

"""
CAMP FUNCTIONS
"""


"""
The function `create_camps` in this Python code snippet handles the creation of new camp entries in
a MongoDB collection based on the data received through a POST request, and also retrieves all
existing camp entries for display in a template for a GET request.
:return: The code snippet provided is a Flask route function named `create_camps` that handles both
GET and POST requests.
"""
@app.route('/create_camps', methods=['GET', 'POST'])
def create_camps():
    if request.method == "POST":
        data = request.json
        camp_name = data.get('camp_name')
        camp_theme = data.get('camp_theme')
        camp_category = data.get('camp_category')
        disease_focus = data.get('disease_focus')
        venue = data.get('venue')
        date = data.get('date')
        time_period = data.get('time_period')
        awareness_creation = data.get('awareness_creation')
        age_group = data.get('age_group')
        expertise = data.get('expertise')
        assigned_doctors = data.get('assigned_doctors')
        assigned_nurses = data.get('assigned_nurses')
        prerequisites = data.get('prerequisites')
        camp_capacity = data.get('camp_capacity')
        created_at = datetime.now()

        # Create a new Camps object
        new_camp = Camps(
            camp_name=camp_name,
            camp_theme=camp_theme,
            camp_category=camp_category,
            disease_focus=disease_focus,
            venue=venue,
            date=date,
            time_period=time_period,
            awareness_creation=awareness_creation,
            age_group=age_group,
            expertise=expertise,
            assigned_doctors=assigned_doctors,
            assigned_nurses=assigned_nurses,
            prerequisites=prerequisites,
            camp_capacity=camp_capacity,
            created_at=created_at
        )

        # Generate a document from the Camps object
        camp_document = new_camp.generate_document_JSON()

        # Insert the new camp into the MongoDB collection
        inserted_id = camps_collection.insert_one(camp_document).inserted_id

        print(f">>> Camp created for id: {inserted_id} | {created_at}")

        # Return a success message or redirect
        return jsonify({"status": 200, "camp_id": str(inserted_id), "message": "Camp created succesfully", "created_at": created_at}), 200

    allCamps = list(camps_collection.find({}, {'_id': False}))	
    # If it's a GET request, just render a template or return a message
    return render_template('camps.html', camps=allCamps)  # Assuming you have a template for creating a camp


@app.route('/get_all_camps', methods=['GET'])
def get_all_camps():
    if request.method == "GET":
        allCamps = list(camps_collection.find({}, {'_id': False}))
        return jsonify({"status": 200, "camp_data": allCamps}), 200


@app.route('/create_doctors', methods=['GET', 'POST'])
def create_doctors():
    if request.method == "POST":
        data = request.json
        full_name = data.get('full_name')
        expertise_category = data.get('expertise_category')
        years_of_experience = data.get('years_of_experience')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        meet_link = data.get('meet_link')
        age = data.get('age')
        phone_number = data.get('phone_number')
        email = data.get('email')
        unavailable_days = data.get('unavailable_days')
        created_at = datetime.now()

        # Create a new Camps object
        new_doctor = Doctors(
            full_name=full_name,
            expertise_category=expertise_category,
            years_of_experience=years_of_experience,
            start_time=start_time,
            end_time=end_time,
            meet_link=meet_link,
            age=age,
            phone_number=phone_number,
            email=email,
            unavailable_days=unavailable_days,
            created_at=created_at
        )

        # Generate a document from the Camps object
        doctor_document = new_doctor.generate_document_JSON()

        # Insert the new camp into the MongoDB collection
        inserted_id = doctors_collection.insert_one(doctor_document).inserted_id

        print(f">>> Doctor Profile created for id: {inserted_id} | {created_at}")

        # Return a success message or redirect
        return jsonify({"status": 200, "doctor_id": str(inserted_id), "message": "Doctor created succesfully", "created_at": created_at}), 200
		
    allDoctors = list(doctors_collection.find({}, {'_id': False}))
    # If it's a GET request, just render a template or return a message
    return render_template('camps.html', camps=allDoctors)  # Assuming you have a template for creating a camp


@app.route('/get_available_doctors_staff/<day>', methods=['GET'])
def get_available_doctors(day):
    if request.method == "GET":
        # allDoctors = list(doctors_collection.find({}, {'_id': False}))
        available_doctors = [
            doctor for doctor in doctors_collection.find({}, {'_id': False})
            if day not in doctor.get('unavailable_days', [])
        ]
        available_staff = [
            staff for staff in staff_collection.find({}, {'_id': False})
            if day not in staff.get('unavailable_days', [])
        ]

        return jsonify({"status": 200, "doctor_data": available_doctors, "staff_data": available_staff}), 200


@app.route('/get_all_doctors', methods=['GET'])
def get_all_doctors():
    if request.method == "GET":
        allDoctors = list(doctors_collection.find({}, {'_id': False}))
        return jsonify({"status": 200, "doctor_data": allDoctors}), 200


@app.route('/create_staff', methods=['GET', 'POST'])
def create_staff():
    if request.method == "POST":
        data = request.json
        full_name = data.get('full_name')
        expertise_category = data.get('expertise_category')
        years_of_experience = data.get('years_of_experience')
        age = data.get('age')
        phone_number = data.get('phone_number')
        email = data.get('email')
        unavailable_days = data.get('unavailable_days')
        designation = data.get('designation')
        created_at = datetime.now()

        # Create a new Camps object
        new_staff = Staff(
            full_name=full_name,
            expertise_category=expertise_category,
            years_of_experience=years_of_experience,
            age=age,
            phone_number=phone_number,
            email=email,
            unavailable_days=unavailable_days,
            designation=designation,
            created_at=created_at
        )

        # Generate a document from the Camps object
        staff_document = new_staff.generate_document_JSON()

        # Insert the new camp into the MongoDB collection
        inserted_id = staff_collection.insert_one(staff_document).inserted_id

        print(f">>> Staff Profile created for id: {inserted_id} | {created_at}")

        # Return a success message or redirect
        return jsonify({"status": 200, "staff_id": str(inserted_id), "message": "Staff created succesfully", "created_at": created_at}), 200

    allStaff = list(saff_collection.find({}, {'_id': False}))
    # If it's a GET request, just render a template or return a message
    return render_template('camps.html', camps=allStaff)  # Assuming you have a template for creating a camp


@app.route('/get_all_staff', methods=['GET'])
def get_all_staff():
    if request.method == "GET":
        allStaff = list(staff_collection.find({}, {'_id': False}))
        return jsonify({"status": 200, "staff_data": allStaff}), 200


class Camps:

	def __init__(self, camp_name, camp_theme, camp_category, disease_focus,
	             venue, date, time_period, awareness_creation, age_group,
	             expertise, assigned_doctors, assigned_nurses, prerequisites,
	             camp_capacity, created_at):
		self.camp_name = camp_name
		self.camp_theme = camp_theme
		self.camp_category = camp_category
		self.disease_focus = disease_focus
		self.venue = venue
		self.date = date
		self.time_period = time_period
		self.awareness_creation = awareness_creation
		self.age_group = age_group
		self.expertise = expertise
		self.assigned_doctors = assigned_doctors
		self.assigned_nurses = assigned_nurses
		self.prerequisites = prerequisites
		self.camp_capacity = camp_capacity
		self.created_at = created_at

	def generate_document_JSON(self):
		return {
		    "camp_name": self.camp_name,
		    "camp_theme": self.camp_theme,
		    "camp_category": self.camp_category,
		    "disease_focus": self.disease_focus,
		    "venue": self.venue,
		    "date": self.date,
		    "time_period": self.time_period,
		    "awareness_creation": self.awareness_creation,
		    "age_group": self.age_group,
		    "expertise": self.expertise,
		    "assigned_doctors": self.assigned_doctors,
		    "assigned_nurses": self.assigned_nurses,
		    "prerequisites": self.prerequisites,
		    "camp_capacity": self.camp_capacity,
		    "created_at": self.created_at
		}

# The Users class in Python defines attributes and methods to store and generate JSON documents
# containing user information.
class Users:

    # user_id, full_name, age, pincode, lat, long, gender, disease_category, payment_status, prescriptions, created_at
    def __init__(self, user_id, full_name, age, pincode, lat, long, gender, disease_category, payment_status, prescriptions, created_at):
        self.user_id = user_id
        self.full_name = full_name
        self.age = age
        self.pincode = pincode
        self.lat = lat
        self.long = long
        self.gender = gender
        self.disease_category = disease_category
        self.payment_status = payment_status
        self.prescriptions = prescriptions
        self.created_at = created_at
    
    def generate_document_JSON(self):
    	return {
    	    "user_id": user_id,
            "full_name": full_name,
            "age": age,
            "pincode": pincode,
            "lat": lat,
            "long": long,
            "gender": gender,
            "disease_category": disease_category,
            "payment_status": payment_status,
            "prescriptions": prescriptions,
            "created_at": created_at
    	}


# This Python class defines a template for storing information about doctors, including their personal
# details and availability.
class Doctors:
    '''
    full_name, expertise_category, years_of_experience, start_time, end_time, age, phone_number, email, unavailable_days, created_at
    '''
    def __init__(self, full_name, expertise_category, years_of_experience, start_time, end_time, meet_link,
                 age, phone_number, email, unavailable_days, created_at):
        self.full_name = full_name
        self.expertise_category = expertise_category
        self.years_of_experience = years_of_experience
        self.start_time = start_time
        self.end_time = end_time
        self. meet_link =  meet_link
        self.age = age
        self.phone_number = phone_number
        self.email = email
        self.unavailable_days = unavailable_days
        self.created_at = created_at

    def generate_document_JSON(self):
        """
        The function `generate_document_JSON` returns a dictionary containing various attributes of a
        document.
        :return: A JSON object containing various attributes such as full_name, expertise_category,
        years_of_experience, start_time, end_time, meet_link, age, phone_number, email,
        unavailable_days, and created_at.
        """
        return {
            "full_name": self.full_name,
            "expertise_category": self.expertise_category,
            "years_of_experience": self.years_of_experience,
            "start_time": self.start_time,
            "end_time": self.end_time,
            " meet_link": self. meet_link,
            "age": self.age,
            "phone_number": self.phone_number,
            "email": self.email,
            "unavailable_days": self.unavailable_days,
            "created_at": self.created_at
        }


# This Python class defines a Staff object with attributes such as full name, age, expertise category,
# years of experience, contact information, and availability schedule.
class Staff:
    def __init__(self, full_name, age, expertise_category, years_of_experience,
                 phone_number, email, unavailable_days, designation, created_at):
        self.full_name = full_name
        self.expertise_category = expertise_category
        self.years_of_experience = years_of_experience
        self.age = age
        self.phone_number = phone_number
        self.email = email
        self.unavailable_days = unavailable_days
        self.designation = designation
        self.created_at = created_at

    def generate_document_JSON(self):

        return {
            "full_name": self.full_name,
            "expertise_category": self.expertise_category,
            "years_of_experience": self.years_of_experience,
            "age": self.age,
            "phone_number": self.phone_number,
            "email": self.email,
            "unavailable_days": self.unavailable_days,
            "designation": self.designation,
            "created_at": self.created_at
        }



"""
The above function defines a route in a Python Flask application that returns the string
'SehatSampark Backend' when the route is accessed.
:return: 'SehatSampark Backend'
"""
@app.route('/')
def index():
	return 'SehatSampark Backend'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)
