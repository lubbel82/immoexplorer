# read csv file with properties
import pandas as pd
import requests
import time

df = pd.read_csv('properties.csv', encoding="utf-8")

# Loop through rows where the column 'GPS' is empty
for row in df[df["gps"].isnull()].iterrows():
    # Get the address of the property
    
    params={'street':row[1][['street']],'city':row[1]['city'],'country':row[1]['country'],'postalcode':row[1]['zip_code']}

    print(params)
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&zoom=18"

    response = requests.get(url, params=params)
    
    # Get the latitude and longitude coordinates from the response
    print(response.status_code)
    if response.status_code == 200:
       results = response.json()
       if results:
           # Get the latitude and longitude coordinates from the geocoding API response
           # Update the GPS column in the DataFrame
           gps = f"{results[0]['lat']}, {results[0]['lon']}"
           print(gps)
           df.loc[row[0], "gps"] = gps
           df.loc[row[0], "lat"] = float(results[0]['lat'])
           df.loc[row[0], "lon"] = float(results[0]['lon'])
    time.sleep(2)

# Loop through rows where the column 'GPS' is not empty but lat and lon are empty


for row in df[(df["gps"].notnull()) & (df["lat"].isnull())].iterrows():
    # Get the address of the property
    gps = row[1]["gps"]
    lat, lon = gps.split(",")
    df.loc[row[0], "lat"] = float(lat)
    df.loc[row[0], "lon"] = float(lon)

# Save the updated DataFrame to a CSV file
df.to_csv('updated_properties.csv', index=False)

# %%
import folium
import webbrowser

# Create a map
map = folium.Map(location=[52.0971107, 7.6114373], zoom_start=8)


for row in df.iterrows():
    # Get the property information
    value = str(row[1]["value"])
    type = row[1]["type"]
    name = row[1]["name"]
    lat = row[1]["lat"]
    lon = row[1]["lon"]

    # Create a Folium marker
    #marker = folium.Marker(location= [row[1]['lat'], row[1]['lon']], popup=f"Objektname {name} Nutzung: {type} Marktwert €: {value}")
    marker = folium.Marker(location= [row[1]['lat'], row[1]['lon']], popup=f"Objektname {name} Nutzung: {type} Marktwert €: {value}"+ '<br>' + '<a href="https://www.google.com/maps?layer=c&cbll=' + str(lat) + ',' + str(lon) + '" target="blank">GOOGLE STREET VIEW</a>')

    # Add the marker to the map
    marker.add_to(map)

#Display the map
map.save("map.html")
webbrowser.open("map.html")



