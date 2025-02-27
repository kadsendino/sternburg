import requests
import json


url = "https://www.sternburg-bier.de/storefinder/api//search/loc"
data = {"latitude":"51.330976","longitude":"12.401430","radius":"10000","brand":"650"}

response = requests.post(url, json=data)  # Sends JSON data

print(response.status_code)  # Print HTTP status code
#print(response.json())       # Print response JSON (if any)

if response.status_code == 200:
    json_data = response.json()  # Convert response to JSON

    # Define the output JSON file
    json_filename = "sternburg_stores.json"

    # Write to JSON file
    with open(json_filename, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)  # Pretty format

    print(f"JSON file '{json_filename}' created with {len(json_data)} entries.")

else:
    print("Error fetching data:", response.status_code)
