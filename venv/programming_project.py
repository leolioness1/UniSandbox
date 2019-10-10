#import packages
import matplotlib.pyplot as plt
import pandas as pd

def clean_data(df):
    
    #drop columns with more than 50 empty columns
    
    df.dropna(axis=1,thresh=50, inplace=True)

    #drop the indicator name,code variables as they aren't noisy

    df.drop(["Indicator Name", "Indicator Code"], axis=1,inplace=True)

    #drop rows with more than 12 missing years
    df.dropna(axis=0,thresh=12, inplace=True)

    # fill empty values with 0
    df = df.fillna(0)

    return df

#import international inbound tourist data from csv

tourist_df=pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

tourist_df = clean_data(tourist_df)

#import international inbound tourist data from csv
receipt_df =pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)


# import country region and income information
country_info = pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\Metadata_Country_API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", usecols=[0,1,2])

# left join the 2 dataframes
combined_df= pd.merge(country_info,tourist_df, on='Country Code', how='left')

#clear other df from memory
del tourist_df, country_info

# seperate countries and regions in 2 different dataframes
country_df = combined_df[combined_df["Region"].notna()]
region_df = combined_df[combined_df["Region"].isna()]


#create dummies for Income Group and remove Income Group
income_enc = pd.get_dummies( country_df['IncomeGroup'])
country_df = pd.concat([country_df, income_enc], axis=1)
country_df.drop("IncomeGroup",axis=1,inplace=True)

country_df.sort_values("2016",inplace=True, ascending=False)

country_df["2016"].hist(bins=20, figsize=[14,6])




