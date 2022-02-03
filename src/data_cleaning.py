import pandas as pd
from yelpapi import YelpAPI
import sqlite3 as db

df = pd.read_csv("C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data/stockholm_housing_df_RAW.csv")
def clean_housing_data(df):
    df['fee'] = df['fee'].str.rstrip(' kr/mån')

    # Drop 'location' column, as it is redundant
    df = df.drop(columns=["location"])

    # Split size of apartment and number of rooms into separate columns
    df[['size', 'rooms']] = df['size:rooms'].str.split("  ", 1, expand=True)
    df = df.drop(columns=["size:rooms"])
    # Clean up the columns size and room, removing m2 and "rum"
    df['size'] = df['size'].str.rstrip('m²')
    df["rooms"] = df["rooms"].str.rstrip(' rum')

    # Split adress and floor of apt into separate columns
    df[['adress', 'floor']] = df['adress'].str.split(",", 1, expand=True)

    # Bug where value_dev ends up in wrong columns, due to old postings
    bad_index = df[df["ppsqm"].str.find("%") != -1].index
    df = df.drop(bad_index, axis=0)
    column_list = ["ppsqm", "size", "rooms", "sale_price", "fee"]

    # Clean up sold_date, sale_price, value_dev, ppsqm
    df["sold_date"] = df["sold_date"].str.lstrip('såld')
    df["sale_price"] = df["sale_price"].str.lstrip('slutpris ')
    df["sale_price"] = df["sale_price"].str.rstrip(' kr')
    df["ppsqm"] = df["ppsqm"].str.rstrip(" kr/m²")
    df['value_dev'] = df['value_dev'].str.extract('(\d+)', expand=False)
    df["value_dev"].astype(float)

    # Introduce dummy variables in the following way: Balkong = 1, Hiss = 2, Balkong&Hiss = 3, Uteplats = 4
    df["features"] = df.features.map({'balkong': 1, 'hiss': 2, 'balkong&hiss': 3, 'uteplats': 4, 'NaN': 5})

    # Remove everything except numerical values from floor
    df['floor'] = df['floor'].str.extract('(\d+)', expand=False)

    df = fix_numeric(column_list, df.copy())

    # Reset index after removing rows
    cleaned_housing_df = df.reset_index(drop=True)
    return cleaned_housing_df


def fix_numeric(column_list, df):
    new_df = df.copy()
    for i in column_list:
        new_df[i] = new_df[i].str.replace(" ", "")
        new_df[i] = pd.to_numeric(new_df[i], errors='coerce')
        new_df = new_df.dropna(subset=[i])
        new_df[i] = new_df[i].astype('int')
    return new_df


cleaned_housing_df = clean_housing_data(df)
cleaned_housing_df.to_csv("stockholm_housing_df_CLEANED.csv", index=False)


###############################################################################

yelp_df = pd.read_csv("C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data/stockholm_housing_df_CLEANED.csv")
yelp_api = YelpAPI("KulP_1xAbhj4PcwcltixYR5hz4qMJ2aarTp4uNP_bBED4CsgP1nqY0bZrDxRMMSsZYwqvirOQ1Dy--6v3Y2yS4lBVPmfebDVdXGukr74OZEKRNoivTBiORBJ0v_iYXYx")

# A 'suggested search area' of 500 is used, although, the docs tell us the following:
# This field is used as a suggestion to the search. The actual search radius may be lower
# than the suggested radius in dense urban areas, and higher in regions of less business density
# hopefully, it does give some quantifiable value as to the 'closeness' to points of interest a apartment has

# k is set to 0 initially, but as there can only be 5000 yelp calls on one api key per day, this has to be changed continuosly
k = 0
def get_POI(adress):
    input_adress = adress
    response = yelp_api.search_query(location=input_adress, radius=500, limit=1)
    return response
def get_yelp_values(df, k):
    try:
        for i in range(k, len(df)):
            response = get_POI(df["adress"][i])
            print("Getting values from adress:", df["adress"][i], "from row: ", i)

            lat = (response['region']['center']['latitude'])
            long = (response['region']['center']['longitude'])
            POI = (response['total'])
            df.at[i, 'Latitude'] = lat
            df.at[i, 'Longitude'] = long
            df.at[i, 'NearbyPOIs'] = POI

        return df
    except Exception as e:
        print(e)
        print("\n", "error")
        k = i + 1

        error_handler(df, k)
def error_handler(df, k):
    get_yelp_values(df, k)
    return
get_yelp_values(yelp_df, k)

yelp_df.to_csv("hemnet_housing_yelp.csv", index=False)

df = pd.read_csv("C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data/hemnet_housing_yelp.csv")
true_columns = df.columns[1:]
df = df[true_columns]

non_duplicate_index = df[["fee","features","sale_price","adress","Longitude", "Latitude", "NearbyPOIs"]].drop_duplicates().index
df_final = df.iloc[non_duplicate_index]
df_final.reset_index(drop=True)

path = "C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data"
def insert_into_db(df, path):
    try:
        conn = db.connect(f"{path}/hemnet_database.db")
        c = conn.cursor()
    except Exception as e:
        print(e)
    try:
        df.to_sql("housing_objects", conn, if_exists="fail")
    except Exception as e:
        print(e)
insert_into_db(df_final, path)