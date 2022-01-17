import pandas as pd

df = pd.read_csv("C:/Users/Anton/Documents/Anton_Gollbo/Skolarbete/projects/Hemnet_Housing/data/stockholm_housing_df_RAW.csv")

df['fee'] = df['fee'].str.rstrip(' kr/mån')

#Drop 'location' column, as it is redundant
df = df.drop(columns=["location"])

#Split size of apartment and number of rooms into separate columns
df[['size', 'rooms']] = df['size:rooms'].str.split("  ", 1, expand=True)
df = df.drop(columns=["size:rooms"])
#Clean up the columns size and room, removing m2 and "rum"
df['size'] = df['size'].str.rstrip('m²')
df["rooms"] = df["rooms"].str.rstrip(' rum')

#Split adress and floor of apt into separate columns
df[['adress', 'floor']] = df['adress'].str.split(",", 1, expand=True)

#Clean up sold_date, sale_price, value_dev, ppsqm
df["sold_date"] = df["sold_date"].str.lstrip('såld')
df["sale_price"] = df["sale_price"].str.lstrip('slutpris ')
df["sale_price"] = df["sale_price"].str.rstrip(' kr')
df["ppsqm"] = df["ppsqm"].str.rstrip(" kr/m²")
df["value_dev"] = df["value_dev"].str.rstrip(" %")
df["value_dev"] = df["value_dev"].str.lstrip("+")

# Introduce dummy variables in the following way: Balkong = 1, Hiss = 2, Balkong&Hiss = 3, Uteplats = 4
df["features"] = df.features.map( {'balkong':1 , 'hiss':2, 'balkong&hiss':3, 'uteplats': 4, 'NaN':5} )

#Remove everything except numerical values from floor
df['floor'] = df['floor'].str.extract('(\d+)', expand=False)

#Bug where value_dev ends up in wrong columns, due to old posting
bad_index = df[df["ppsqm"].str.find("%") != -1].index
df = df.drop(bad_index, axis=0)

column_list = ["ppsqm", "size", "rooms", "sale_price","fee"]

def fix_numeric(column_list, df):
    new_df = df.copy()
    for i in column_list:
        new_df[i] = new_df[i].str.replace(" ", "")
        new_df[i] = pd.to_numeric(new_df[i] , errors='coerce')
        new_df = new_df.dropna(subset=[i])
        new_df[i] = new_df[i].astype('int')
    return new_df

cleaned_housing_df = fix_numeric(column_list,df.copy() )
#Reset index after removing rows
cleaned_housing_df = cleaned_housing_df.reset_index(drop=True)
cleaned_housing_df.to_csv("stockholm_housing_df_CLEANED.csv",index=False)
