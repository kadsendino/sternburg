import folium
import json

def read_json(filename):
    """Read JSON file and return data."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

state_data = read_json("sternburg_counties.json")

def get_color(value):
    if value <= 0:
        return '#967676'  # Red for values close to 0
    elif value <= 20:
        return '#9D6161'  # Light gray for values between 0 and 25
    elif value <= 200:
        return '#964747'  # Darker gray for values between 25 and 50
    elif value <= 1000:
        return '#8E1A1A'  # Even darker gray for values between 50 and 75
    else:
        return '#920303'  # Dark gray (almost black) for values above 75

# Initialize the map
m = folium.Map(location=[51.1657, 10.4515], tiles="cartodb positron", zoom_start=6)

# Load your local GeoJSON file
geojson_path = "germany_counties.geojson"
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)
shape_names = [feature['properties']['shapeName'] for feature in geojson_data['features']]

keys = list(state_data.keys())
for i in reversed(range(len(keys))):
    entry = keys[i]
    if entry not in shape_names:
        new_entry = entry.removeprefix("Landkreis ")
        if new_entry not in shape_names:
            new_entry = entry.removeprefix("Landkreis ") + ", Kreisfreie Stadt"
            if new_entry not in shape_names:
                new_entry = entry.removeprefix("Kreis ")
                if new_entry not in shape_names:
                    new_entry = entry.removeprefix("Landkreis ") + ", Landkreis"
                    if new_entry not in shape_names:
                        print(entry)
                    else:
                        state_data[new_entry] = state_data.pop(entry)
                else:
                    state_data[new_entry] = state_data.pop(entry)
            else:
                state_data[new_entry] = state_data.pop(entry)
        else:
            state_data[new_entry] = state_data.pop(entry)


# Define the style function using the static color palette
def style_function(feature):
    state_name = feature['properties']['shapeName']  # Adjust this based on your GeoJSON structure
    value = state_data.get(state_name, 0)  # Default to 0 if the state is not in state_data
    feature['properties']['value']=f"{value} Geschäfte"
    color = get_color(value)
    return {
        'fillColor': color,
        'fillOpacity': 0.85,
        'weight': 0.5,
        'color': 'white'
    }

# Add the GeoJSON layer with popups
folium.GeoJson(
    geojson_data,
    name='geojson',
    style_function=style_function,
    # Dynamically adding popup content within the style_function
    popup=folium.GeoJsonPopup(fields=['shapeName','value'], localize=True, labels=False)
).add_to(m)

# Add custom legend
legend_html = """
    <div style="position: fixed; 
                top: 50px; right: 50px; width: 200px; height: 200px; 
                background-color: white; border:2px solid grey; z-index:9999; font-size:14px; padding: 10px;">
        <b>Anzahl der Geschäfte, in denen Sternburg gekauft werden kann</b><br>
        <i style="background: #967676; width: 18px; height: 18px; display: inline-block;"></i> 0<br>
        <i style="background: #9D6161; width: 18px; height: 18px; display: inline-block;"></i> 1 - 20<br>
        <i style="background: #964747; width: 18px; height: 18px; display: inline-block;"></i> 21 - 200<br>
        <i style="background: #8E1A1A; width: 18px; height: 18px; display: inline-block;"></i> 201 - 1000<br>
        <i style="background: #920303; width: 18px; height: 18px; display: inline-block;"></i> > 1000
    </div>
"""

# Add the legend to the map as an HTML element
m.get_root().html.add_child(folium.Element(legend_html))
# Save the map
m.save("index.html")
print("map saved as index.html")
