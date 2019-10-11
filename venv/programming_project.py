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


# function to left join df with the income/region metadata and separate them into 2 different dfs country and region


def separate_df(data_df, metadata_df):
    # left join the 2 dataframes

    combined_df = pd.merge(data_df, metadata_df, on='Country Code', how='left')

    # seperate countries and regions in 2 different dataframes

    country_df = combined_df[combined_df["Region"].notna()]
    region_df = combined_df[combined_df["Region"].isna()]

    region_df.drop(["Region", "IncomeGroup"], axis=1, inplace=True)

    return country_df, region_df


def create_dummies(df, col_name):
    # turn column into dummies

    enc = pd.get_dummies(df[col_name])

    # join dummies at the end of df

    df = pd.concat([df, enc], axis=1)

    # drop original column from df

    df.drop(col_name, axis=1, inplace=True)

    return df


#import international inbound tourist data from csv

tourist_df=pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

tourist_df = clean_data(tourist_df)

# import expenditure data from csv and clean data

receipt_df = pd.read_csv("C:\\Users\Leonor.furtado\\OneDrive - Accenture\\Uni\Programming\project\API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

receipt_df = clean_data(receipt_df)

# import country region and income information
country_info = pd.read_csv("C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\Metadata_Country_API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", usecols=[0,1,2])

#seperate tourist df into region and country
tourist_country_df, tourist_region_df = separate_df (tourist_df, country_info)


#seperate receipt df into region and country
receipt_country_df, receipt_region_df = separate_df (receipt_df, country_info)


#create dummies for Income Group and remove Income Group

tourist_country_df = create_dummies(tourist_country_df,col_name ='IncomeGroup')

#sort region data from highest to lowest values in 2016

tourist_region_df.sort_values("2016",inplace=True, ascending=False)
receipt_region_df.sort_values("2016",inplace=True, ascending=False)


#pivot dataframe and do a bar plot for last 10 years and top 10 regions

tourist_region_df.drop("Country Code", axis=1,inplace=True)
tourist_region_df.set_index("Country Name", inplace=True)
region_df_test=tourist_region_df.T
region_df_test.reset_index(inplace=True)
region_df_test=region_df_test.tail(11)
region_cols =region_df_test.columns.values
region_df_test.plot(x="index", y=region_cols[2:11], kind="bar")


#clear other df from memory

del tourist_df, receipt_df



