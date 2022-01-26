from yelpapi import YelpAPI
import pandas as pd

yelp_df = pd.read_csv("C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data/stockholm_housing_df_CLEANED.csv")

yelp_api = YelpAPI(
    "KulP_1xAbhj4PcwcltixYR5hz4qMJ2aarTp4uNP_bBED4CsgP1nqY0bZrDxRMMSsZYwqvirOQ1Dy--6v3Y2yS4lBVPmfebDVdXGukr74OZEKRNoivTBiORBJ0v_iYXYx")


# A 'suggested search area' of 500 is used, although, the docs tell us the following:
# This field is used as a suggestion to the search. The actual search radius may be lower
# than the suggested radius in dense urban areas, and higher in regions of less business density
# hopefully, it does give some quantifiable value as to the 'closeness' to points of interest a apartment has

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

#yelp_df.to_csv("UNFINISHED_yelp_df_CLEANED.csv", index=False)
