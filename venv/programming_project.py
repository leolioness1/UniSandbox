#import packages
import pandas as pd

#import international inbound tourist data from csv

api_df=pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

#drop columns with more than 50 empty columns

api_df.dropna(axis=1,thresh=50, inplace=True)


#drop the indicator name,code variables as they aren't noisy

api_df.drop(["Indicator Name", "Indicator Code"], axis=1,inplace=True)

# import country region and income information
country_info = pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\Metadata_Country_API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", usecols=[0,1,2])

# left join the 2 dataframes
combined_df= pd.merge(country_info,api_df, on='Country Code', how='left')

#clear other df from memory
del api_df, country_info

# seperate countries and regions in 2 different dataframes
country_df = combined_df[combined_df["Region"].notna()]
region_df = combined_df[combined_df["Region"].isna()]

#drop rows with more than
country_df.dropna(axis=0,thresh=12, inplace=True)
country_df= country_df.fillna(0)
income_enc = pd.get_dummies( country_df['IncomeGroup'])
country_df = pd.concat([country_df, income_enc], axis=1)
country_df.drop("IncomeGroup",axis=1,inplace=True)

