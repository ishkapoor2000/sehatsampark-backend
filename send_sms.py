import requests
import json

# Replace with your actual Pushbullet access token
ACCESS_TOKEN = "o.l6XCGHxqDTjpi6ngFZBpscQFovZS9sNJ"

# Replace with the target device identifier
TARGET_DEVICE_IDEN = "ujwRVzjj0lEsjwYBxQxr1E"

# Replace with the phone number (including country code) of the recipient
ReceiverNumber = "+919289708244"

# The message you want to send
TextMessage = f"Hi {user_name}. Sehat Sampark is hosting a {camp_name} at your nearest location {camp_complete_address}. Visit the location between {camp_start_time} to {end_start_time}."

# Construct the Pushbullet API endpoint URL
url = "https://api.pushbullet.com/v2/texts"

# Prepare the JSON data for the POST request
# data = {
#     "data": {
#         "target_device_iden": TARGET_DEVICE_IDEN,
#         "addresses": [ReceiverNumber],
#         "message": TextMessage
#     }
# }

# Create the headers with your access token and content type
headers = {
    "Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json;charset=UTF-8"
}

# Send the POST request using the requests library
# response = requests.post(url, headers=headers, json=data)

# Check the response status code
# if response.status_code == 200:
#     print("Status Code:", response.status_code)
#     print("Status Text: Sent successfully")
# else:
#     # Parse the error message from the JSON response
#     error_message = response.json().get("error", {}).get("message")
#     print(f"Status Code: {response.status_code}")
#     print(f"Status Text: {error_message or 'Unknown error'}")

def send_greeting_sms(receiver_number, user_name, camp_name, camp_complete_address, camp_start_time, camp_end_time):
    """Sends a personalized greeting SMS using a hypothetical SMS sending library
    (replace 'send_sms' with your actual library call).

    Args:
        receiver_number (str): The user's phone number in international format (including country code).
        user_name (str): The user's name.

    Returns:
        str: A message indicating success or failure (replace with actual return value from your library).
    """

    # Hypothetical greeting message (replace with your desired content)
    greeting_message = f"Hi {user_name}. Sehat Sampark is hosting a {camp_name} at your nearest location {camp_complete_address}. Visit the location between {camp_start_time} to {camp_end_time}."

    data = {
        "data": {
            "target_device_iden": TARGET_DEVICE_IDEN,
            "addresses": [receiver_number],
            "message": greeting_message
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:  # Replace with actual success condition
            return "SMS sent successfully!", 200
        else:
            return f"Error sending SMS: {response.text}"  # Replace with actual error handling
    except Exception as e:
        return f"An unexpected error occurred: {e}", 403  # Generic error handling


users=[
    {
    "name": "Himanshu",
    "number": "+919870538621"
},
    {
    "name": "Shivam Saini",
    "number": "+919555625605"
},
    {
    "name": "Rohan",
    "number": "+917374091655"
}]

for i in users:
    user_name = i["name"]
    user_phone_number = i["number"]
    response_message = send_greeting_sms(user_phone_number, user_name)
    print(response_message)

