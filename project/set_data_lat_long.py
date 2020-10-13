import os
import pandas as pd

# set up various things to be loaded outside of the function
# geolocation data
locs_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'cities_states.csv')
locs_df = pd.read_csv(locs_path)


def lowerify(text):
    # fix up geolocation dataframe a little
    return text.lower()


locs_df = locs_df.drop(columns=['Unnamed: 0', 'country'])
locs_df['city_ascii'] = locs_df['city_ascii'].apply(lowerify)
locs_df['admin_name'] = locs_df['admin_name'].apply(lowerify)

states_map = {}
# for each state, map their respective cities
for state in list(locs_df.admin_name.unique()):
    states_map[state] = locs_df[locs_df['admin_name']
                                == state]['city_ascii'].to_list()

# Create geo_coder dictionary to map states to their cities and their lat and long
geo_coder = {}
for state in list(locs_df.admin_name.unique()):
    
    geo_coder[state] = {}

# Iterate through each row in the locs_df dataframe and create the connections between our state/city and their lat/long
for _, row in locs_df.iterrows():
    temp_dict = {row["city_ascii"]: [row["lat"], row["lng"]]}
    geo_coder[row["admin_name"]].update(temp_dict)

# Read in our all_sources csv file
sources_path = os.path.join(os.path.dirname(
    __file__), '..', '..', 'all_sources.csv')
sources_df = pd.read_csv(sources_path)
# Drop lat and long columns
sources_df = sources_df.drop(columns=["lat", "long"])
sources_df = sources_df.dropna()


# Set all of the city and state values to lowercase
sources_df["city"] = sources_df["city"].apply(lowerify)
sources_df["state"] = sources_df["state"].apply(lowerify)

# Create list to hold latitude values
lat_list = []
# Create list to hold longitude values
long_list = []

# Iterate through each row in sources_df dataframe
for _, row in sources_df.iterrows():

    # Washington DC is formatted differently in all_sources.csv compared to cities_states
    # The following if statement considers that
    if row["state"] == "washington dc":
        # Set lat and long values using the geo_coder graph
        lat_list.append(geo_coder["district of columbia"]["washington"][0])
        long_list.append(geo_coder["district of columbia"]["washington"][1])
    # hollywood, california is formatted differented in all_sources.csv compared to cities_states
    # the following elif statement considers that
    elif row["city"] == "hollywood":
        lat_list.append(geo_coder[row["state"]]["west hollywood"][0])
        long_list.append(geo_coder[row["state"]]["west hollywood"][1])
    # Bethel, Ohio is not in the cities_states.csv
    # Performing my own research I found the lat and long values
    # for Bethel, Ohio and will input them manually in the
    # following elif code
    elif row["city"] == "bethel":
        lat_list.append(38.963677) 
        long_list.append(-84.080766)
    # Discovered an instance of incorrect state in all_sources.csv
    # Claims incident occurred in Everett, Oregon but after
    # doing some research and following the link the state is actually
    # Washington. The following elif code creates lat and long values
    # with that considered
    elif row["city"] == "everett":
        lat_list.append(geo_coder["washington"]["everett"][0])
        long_list.append(geo_coder["washington"]["everett"][1])
    # Keystone, South Dakota is not in the cities_states.csv
    # Performing my own research I found the lat and long values
    # for Keystone, South Dakota and will input them manually in the
    # following elif code
    elif row["city"] == "keystone":
        lat_list.append(43.895544) 
        long_list.append(-103.418246)
    # New York City, New York is formatted differented in the two csv files
    # The following code creates lat and long values with that considered
    elif row["city"] == "new york city":
        lat_list.append(geo_coder[row["state"]]["new york"][0])
        long_list.append(geo_coder[row["state"]]["new york"][1])
    else:
        lat_list.append(geo_coder[row["state"]][row["city"]][0])
        long_list.append(geo_coder[row["state"]][row["city"]][1])

# Create latitude column using lat_list
sources_df["lat"] = lat_list
# Create longitude column using long_list
sources_df["long"] = long_list

# Create csv file from dataframe
sources_df.to_csv("all_sources_geoed.csv")