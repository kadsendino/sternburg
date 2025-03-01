import folium
import json

# Your data (for demonstration purposes)
state_data = {
    "Sachsen": 1515,
    "Brandenburg": 822,
    "Sachsen-Anhalt": 784,
    "Berlin": 769,
    "Thüringen": 757,
    "Mecklenburg-Vorpommern": 544,
    "Hessen": 102,
    "Bayern": 66,
    "Niedersachsen": 45,
    "Schleswig-Holstein": 18,
    "Baden-Württemberg": 6,
    "Rheinland-Pfalz": 2,
    "Hamburg": 2,
    "Nordrhein-Westfalen": 1,
    "Saarland": 0,
    "Bremen": 0
}

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
geojson_path = "germany_states.geojson"
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

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


legend_html = """
    <style>
        #legend, #map-selector {{
            position: fixed;
            background-color: white;
            border: 2px solid grey;
            z-index: 9999;
            font-size: 14px;
            padding: 10px;
        }}

        #legend {{
            top: 150px; right: 50px; width: 200px; height: 200px;
        }}

        #legend i {{
            width: 18px; height: 18px; display: inline-block;
        }}

        #map-selector {{
            top: 10px; right: 50px; width: 200px; height: auto;
            text-align: center;
        }}

        #map-selector button {{
            width: 90%;
            padding: 5px;
            margin: 5px;
            color: white;
            border: none;
            cursor: pointer;
        }}

        @media (max-width: 600px) {{
            #legend, #map-selector {{
                width: 100px;
                font-size: 7px;
                padding: 5px;
            }}

            #legend {{
                top: 100px;
                height: 100px;
            }}

            #legend i {{
                width: 9px;
                height: auto;
            }}

            #map-selector button {{
                width: 90%;
                padding: 3px;
                font-size: 7px;
            }}
        }}
    </style>
    
    <div id="legend">
        <b>Anzahl der Geschäfte, in denen Sternburg gekauft werden kann</b><br>
        <i style="background: #967676;"></i> 0<br>
        <i style="background: #9D6161;"></i> 1 - 20<br>
        <i style="background: #964747;"></i> 21 - 200<br>
        <i style="background: #8E1A1A;"></i> 201 - 1000<br>
        <i style="background: #920303;"></i> > 1000
    </div>

    <div id="map-selector">
        <b>Karten-Auswahl</b><br><br>
        <button onclick="window.location.href='index.html'" 
                style="background-color: {index_color};">
            Bundesländer
        </button>
        <button onclick="window.location.href='map_counties.html'" 
                style="background-color: {other_color};">
            Landkreise
        </button>
    </div>
"""


current_map = "index.html"  # Change this logic dynamically if needed
index_color = "#8E1A1A" if current_map == "map_counties.html" else "#967676"
other_color = "#8E1A1A" if current_map == "index.html" else "#967676"

m.get_root().html.add_child(folium.Element(legend_html.format(index_color=index_color, other_color=other_color)))

m.save("index.html")
print("map saved as index.html")
