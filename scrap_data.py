import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []

url = "https://www.napanta.com/cold-storage" #the url to scrap data from

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

rows = soup.find_all('tr')
sname = []
sconverted = []
ulink = []

def convertstring(s):
    return s.lower().replace(' ', '-')

#extracting the name of the states
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        state_name = cells[2].find('h5').text.strip()
        sname.append(state_name)

for s in sname:
    s1 = convertstring(s)
    sconverted.append(s1)

#creating link for each state and accessing district names
for s2 in sconverted:
    hrefl = f"https://www.napanta.com/cold-storage/{s2}"
    response2 = requests.get(hrefl)
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    rows2 = soup2.find_all('tr')

    for ro2 in rows2:
        cells2 = ro2.find_all('td')
        if len(cells2) > 3:
            state_name = cells2[2].text.strip()
            district_name = cells2[3].find('h5').text.strip()
            d = convertstring(district_name)
            u_detaillink = f"https://www.napanta.com/cold-storage/{s2}/{d}"
            ulink.append((state_name, u_detaillink))  # Store state name with the link

#accessing each district link and then extracting data from it
for state_name, u in ulink:
    response3 = requests.get(u)
    soup3 = BeautifulSoup(response3.text, 'html.parser')
    rows3 = soup3.find_all('tr')

    for ro3 in rows3:
        cells3 = ro3.find_all('td')
        if len(cells3) > 3:
            d_name = cells3[2].text.strip()
            s_name = cells3[3].text.strip()
            addre = cells3[4].text.strip()
            manager_name = cells3[5].text.strip()
            capacity = cells3[6].text.strip()

            #adding the details in the dictionary
            data.append({
                'State Name': state_name,
                'District Name': d_name,
                'Storage Name': s_name,
                'Address': addre,
                'Manager Name': manager_name,
                'Capacity': capacity
            })

df = pd.DataFrame(data) #converting the dictionary to dataframe 

filename = "coldstorage.csv"
#converting the dataframe to a csv file
df.to_csv(filename, mode='a', header=['STATE', 'DISTRICT', 'Storage name', 'Address', 'Manager Name', 'capacity'], index=False)
