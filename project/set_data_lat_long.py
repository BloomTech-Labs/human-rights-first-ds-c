import os
import pandas as pd
import re

# set up various things to be loaded outside of the function
# geolocation data
locs_path = os.path.join(os.path.dirname(
    __file__), 'latest_incidents.csv')

sources_df = pd.read_csv(locs_path)

sources_df["desc"] = sources_df["desc"].replace("\\n", "  ")

sources_df = sources_df.drop(columns=["Unnamed: 0"])

for i in range(len(sources_df)):
    sources_df["desc"][i] = str(sources_df["desc"][i]).replace("\n", " ")

# print(sources_df["desc"].head(25))
# Create csv file from dataframe
sources_df.to_csv("all_sources_geoed.csv")