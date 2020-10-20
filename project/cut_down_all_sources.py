import os
import pandas as pd
import re

# set up various things to be loaded outside of the function
# geolocation data
locs_path = os.path.join(os.path.dirname(
    __file__), 'all_sources_geoed.csv')

sources_df = pd.read_csv(locs_path)

print(sources_df.sort_values(by="date", ascending=False))