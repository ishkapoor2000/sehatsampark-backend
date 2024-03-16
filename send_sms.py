import requests
import json

# Replace with your actual Pushbullet access token
ACCESS_TOKEN = "o.l6XCGHxqDTjpi6ngFZBpscQFovZS9sNJ"

# Replace with the target device identifier
TARGET_DEVICE_IDEN = "ujwRVzjj0lEsjwYBxQxr1E"

# Replace with the phone number (including country code) of the recipient
ReceiverNumber = "+919289708244"

# The message you want to send
TextMessage = "SMS sent from Ish via API. Disha is the best!"

# Construct the Pushbullet API endpoint URL
url = "https://api.pushbullet.com/v2/texts"

# Prepare the JSON data for the POST request
data = {
    "data": {
        "target_device_iden": TARGET_DEVICE_IDEN,
        "addresses": [ReceiverNumber],
        "message": TextMessage
    }
}

# Create the headers with your access token and content type
headers = {
    "Access-Token": ACCESS_TOKEN,
    "Content-Type": "application/json;charset=UTF-8"
}

# Send the POST request using the requests library
response = requests.post(url, headers=headers, json=data)

# Check the response status code
if response.status_code == 200:
    print("Status Code:", response.status_code)
    print("Status Text: Sent successfully")
else:
    # Parse the error message from the JSON response
    error_message = response.json().get("error", {}).get("message")
    print(f"Status Code: {response.status_code}")
    print(f"Status Text: {error_message or 'Unknown error'}")
