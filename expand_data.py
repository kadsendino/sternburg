from geopy.geocoders import Nominatim
import json
from collections import defaultdict

def read_json(filename):
    """Read JSON file and return data."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json(data, filename):
    """Writes a dictionary to a JSON file."""
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Dictionary successfully written to {filename}")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")

def determ_location(entry):
    lat = entry.get("coordinates", {}).get("lat")
    lng = entry.get("coordinates", {}).get("lng")
    
    while True:
        try:
            geolocator = Nominatim(user_agent="geo_locator")
            location = geolocator.reverse((lat, lng), language="de")
            break  # Exit the loop if the try block is successful
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")

    return location.raw

def main(filename):
    """Main function to process JSON data and count occurrences per state."""
    data = read_json(filename)
    state_counts = defaultdict(int)
    count = 0
    
    for entry in data:
        location = determ_state(entry)
        entry["location"]=location
        count+=1
        
        print(location)
        print(f"{count}/5432")
    write_json(data,"sternburg_stores_expanded.json")
    return data

if __name__ == "__main__":
    filename = "sternburg_stores.json"  
    result = main(filename)
    print("finished")
