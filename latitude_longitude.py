#this file is used to create the latitude and longitude coordinates from the addresses
import pandas as pd
import requests
import math
df = pd.read_csv('coldstorage.csv') 

df['Address'] = df['Address'].astype(str).fillna('') #handling missing values 

addlistnew = [address.split(',')[-1].strip() for address in df['Address']]#stripping the addressses to get smaller address sizes for more accuracy by extracting last part of the address

lat_long = {
    'Location Name': [],
    'Longitude': [],
    'Latitude': []
}

def get_lat_lon(address, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"

    params = {
        'address': address,
        'key': api_key
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()

        if data['status'] == 'OK':
            # Extract latitude and longitude from the response
            location = data['results'][0]['geometry']['location']
            lat = location['lat']
            lon = location['lng']

            # Append the results to the dictionary
            lat_long['Location Name'].append(address)
            lat_long['Longitude'].append(lon)
            lat_long['Latitude'].append(lat)
        else:
            print(f"Error: {data['status']} for address: {address}")
            lat_long['Location Name'].append(address)
            lat_long['Longitude'].append(None)
            lat_long['Latitude'].append(None)
    else:
        print(f"HTTP Error: {response.status_code} for address: {address}")
        lat_long['Location Name'].append(address)
        lat_long['Longitude'].append(None)
        lat_long['Latitude'].append(None)

api_key = "AIzaSyCDdtIvDFj124yemPqpcClIrmQPGMWlZpQ"   # here google maps geocoding api key is used

for address in addlistnew: #each address is run through the function to generate latitude and longitude 
    get_lat_lon(address, api_key)


f = open('lat_long.csv' , 'ab+')

df_latlong = pd.DataFrame(lat_long) #the lat_long dictionary is converted into the data frame

df_latlong.to_csv(f) #the data from is added to a csv file

df['Longitude'] = df_latlong['Longitude']
df['Latitude'] = df_latlong['Latitude']

df.to_csv('coldstorage.csv') #then the latitude and longitude columns are merged with the original coldstorage.csv file





