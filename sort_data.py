import json

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


def stores_per_state(filename):
    data = read_json(filename)
    state_counts = {}

    for entry in data:
        state = entry.get("location", {}).get("address",{}).get("state")
        
        if entry.get("city") == "BERLIN":
            state = "Berlin"
        
        if entry.get("city") == "HAMBURG":
            state = "Hamburg"

        if state == None:
            print(entry)

        if state not in state_counts:
            state_counts[state]=0
        state_counts[state] += 1

    state_counts["Bremen"]=0
    state_counts["Saarland"]=0
    state_counts = dict(reversed(sorted(state_counts.items(), key=lambda item: item[1])))
    print(state_counts)
    write_json(state_counts, "sternburg_states.json")

def stores_per_county(filename):
    data = read_json(filename)
    county_counts = {}

    for entry in data:
        county = entry.get("location", {}).get("address",{}).get("county")
        if county == "Wartburgkreis" and entry.get("location", {}).get("address",{}).get("town") == "Eisenach":
            county = "Eisenach, Kreisfreie Stadt"

        if county == None:
            county = entry.get("location", {}).get("address",{}).get("city")
        
        if county == None:
            county = entry.get("location", {}).get("address",{}).get("town")
            if county != None:
                county+=", Kreisfreie Stadt"
                #print(county)
        
        if county == "Leipzig":
            county = "Leipzig, Kreisfreie Stadt"

        if county == None:
            print(entry)

        if county not in county_counts:

            county_counts[county]=0
        county_counts[county] += 1

    county_counts = dict(reversed(sorted(county_counts.items(), key=lambda item: item[1])))
    write_json(county_counts, "sternburg_counties.json")

if __name__ == "__main__":
    stores_per_county("sternburg_stores_expanded.json")
