#!/usr/bin/env python
# coding: utf-8

# In[2]:


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

tourist_df=pd.read_csv("API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

tourist_df = clean_data(tourist_df)

# import expenditure data from csv and clean data

receipt_df = pd.read_csv("API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", skiprows=4)

receipt_df = clean_data(receipt_df)

# import country region and income information
country_info = pd.read_csv("Metadata_Country_API_ST.INT.ARVL_DS2_en_csv_v2_103871.csv", usecols=[0,1,2])

# import GDP and investment information
investment_GDP_df = pd.read_csv("Public_Private Spending on travel and Tourism service.csv")

investment_GDP_df.dropna(axis=1,thresh=50, inplace=True)

investment_GDP_df.drop(["Country Name", "Indicator Id"], axis=1,inplace=True)

investment_GDP_df.dropna(axis=0,thresh=12, inplace=True)

investment_GDP_df = investment_GDP_df.fillna(0)

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
region_df_test=region_df_test.tail(11)
region_cols =region_df_test.columns.values
region_df_test.iloc[2,:].plot(y=region_cols[2:11], kind="bar")

region_cols =region_df_test.columns.values
income_cols = [s for s in list(region_cols) if "income" in s]
dividend_cols =[s for s in list(region_cols) if "dividend" in s]
not_classified_cols =[s for s in list(region_cols) if "not classified" in s]
organization_cols =[s for s in list(region_cols) if ("OECD members" in s or "Arab World" in s)]
small_states_cols =[s for s in list(region_cols) if "small states" in s]
other_cols =[s for s in list(region_cols) if ("Fragile and conflict affected situations" in s or "Heavily indebted poor countries (HIPC)" in s or "Least developed countries: UN classification" in s or "World" in s)]
group_region_cols =[s for s in list(region_cols) if ("Central Europe and the Baltics" in s or "Caribbean small states" in s or "East Asia & Pacific (excluding high income)" in s or "East Asia & Pacific" in s or "Europe & Central Asia (excluding high income)" in s or "Europe & Central Asia" in s or "Euro area" in s or "European Union" in s or "Latin America & Caribbean (excluding high income)" in s or "Latin America & Caribbean" in s or "Middle East & North Africa (excluding high income)" in s or "Middle East & North Africa" in s or "Sub-Saharan Africa (excluding high income)" in s or "Sub-Saharan Africa" in s)]
IDA_IBRD_cols =[s for s in list(region_cols) if ("IDA" in s or "IBRD" in s)]
UN_cols =[s for s in list(region_cols) if "UN" in s]

dividend_region_df=region_df_test[dividend_cols]



#clear other df from memory

del tourist_df, receipt_df


# In[ ]:




