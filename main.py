import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

nutri_endpoint = os.getenv("NUTRI_ENDPOINT")
app_id = os.getenv("APP_ID")
app_key = os.getenv("APP_KEY")
sheety_endpoint = os.getenv("SHEETY_ENDPOINT")
sheety_user = os.getenv("SHEETY_USER")
sheety_pass = os.getenv("SHEETY_PASS")


# data used to calculate calories
GENDER = "male"
WEIGHT_KG = 84
HEIGHT_CM = 180
AGE = 32

headers = {
    "x-app-id": app_id,
    "x-app-key": app_key,
}

exercise_text = input("Tell me which exercises you did: ")

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}
request = requests.post(url=nutri_endpoint, json=parameters, headers=headers)
response = request.json()
print(f"Call to Nutritionix API: \n {response} \n")

# Creating variables for date and time
today_date = datetime.now().strftime("%d/%m/%y")
now_time = datetime.now().strftime("%X")
SHEET_NAME = "workout"
sheet_headers = {
    "Authorization": f"Bearer {os.getenv('SHEETY_BEARER')}"
}

for exercise in response["exercises"]:
    sheet_inputs = {
        SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    print(sheet_inputs)

    sheet_request = requests.post(
        url=sheety_endpoint, json=sheet_inputs, headers=sheet_headers,
    )
    print(sheet_request.status_code)
    print(sheet_request.json())



