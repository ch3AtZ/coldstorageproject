import pandas as pd
import folium

file_path = 'lat_long.csv'
data = pd.read_csv(file_path)

# Drop rows with missing longitude or latitude values
valid_data = data.dropna(subset=['Longitude', 'Latitude'])

# Calculate the center of the map (mean of the valid latitudes and longitudes)
center_lat = valid_data['Latitude'].mean()
center_long = valid_data['Longitude'].mean()


# Create a map centered on the calculated mean
map_= folium.Map(location=[center_lat, center_long], zoom_start=5)

print(map_)

# Add markers to the map
for _, row in valid_data.iterrows():
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=row['Location Name']
    ).add_to(map_)

output_path = 'lat_long_map.html'
map_.save(output_path)

print(f'Map saved to {output_path}')
