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

if __name__ == "__main__":
    stores_per_state("sternburg_stores_expanded.json")
