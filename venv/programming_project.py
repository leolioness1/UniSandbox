#import packages
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from pandas.util.testing import assert_frame_equal


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

#plot histogram?
tourist_region_df["2016"].hist(bins=20, figsize=[14,6])

#get all the values in the rows for Country Name
region_cols =tourist_region_df['Country Name'].values

#seperate them according to specific words in the name
income_cols = [s for s in list(region_cols) if "income" in s]
dividend_cols =[s for s in list(region_cols) if "dividend" in s]
IDA_IBRD_cols =[s for s in list(region_cols) if ("IDA" in s or "IBRD" in s)]
not_classified_cols =[s for s in list(region_cols) if "not classified" in s]
organization_cols =[s for s in list(region_cols) if ("OECD members" in s or "Arab World" in s)]
small_states_cols =[s for s in list(region_cols) if "small states" in s]
other_cols =[s for s in list(region_cols) if ("Fragile and conflict affected situations" in s or "Heavily indebted poor countries (HIPC)" in s or "Least developed countries: UN classification" in s or "World" in s)]
group_region_cols =[s for s in list(region_cols) if ("Central Europe and the Baltics" in s or "Caribbean small states" in s or "East Asia & Pacific (excluding high income)" in s or "East Asia & Pacific" in s or "Europe & Central Asia (excluding high income)" in s or "Europe & Central Asia" in s or "Euro area" in s or "European Union" in s or "Latin America & Caribbean (excluding high income)" in s or "Latin America & Caribbean" in s or "Middle East & North Africa (excluding high income)" in s or "Middle East & North Africa" in s or "Sub-Saharan Africa (excluding high income)" in s or "Sub-Saharan Africa" in s)]
group_region_cols


#assign a classification to each list of names
def cond(x):
    if x in dividend_cols:
        return "Dividend" 
    elif x in IDA_IBRD_cols:
        return "IDA & IBRD" 
    elif x in income_cols:
        return "Income"
    elif x in not_classified_cols:
        return "Not Classified"
    elif x in organization_cols:
        return "Organization"
    elif x in small_states_cols:
        return "Small_States"
    elif x in other_cols:
        return "Other"
    elif x in group_region_cols:
        return "Group Region"
    else:
        return "Country"
    return x

#assign classfication for every name in Country Name column
cat_col = [cond(x) for x in tourist_region_df['Country Name']] 

#position we want to insert in df (3rd column)
idx = 2
#insert in existing df
tourist_region_df.insert(loc=idx, column='Location Group', value=cat_col)
#show first 10 values to test it worked
tourist_region_df.head(10)

%matplotlib inline
#pivot dataframe and do a bar plot for last 10 years and top 10 regions

tourist_region_df.drop("Country Code", axis=1,inplace=True)
tourist_region_df.set_index("Country Name", inplace=True)
region_df_test=tourist_region_df.T
region_df_test=region_df_test.tail(11)
region_cols =region_df_test.columns.values
region_df_test.iloc[2,:].plot(y=region_cols[2:11], kind="bar")


# Encoding issue for special characters, see the next link:
# https://stackoverflow.com/questions/18171739/unicodedecodeerror-when-reading-csv-file-in-pandas-with-python
population = pd.read_csv('C:\\Users\Leonor.furtado\OneDrive - Accenture\\Uni\Programming\project\Population by country.csv', encoding="ISO-8859-1",skiprows=4)

# Showing the dataframe
population.head()
list(population.columns)

# Drop some columns from the population dataframe
population = population.drop(['Indicator Name', 'Indicator Code'], axis=1)
list(population.columns)

# Unpivot function melt from pandas
pop_unpivoted = population.melt(id_vars=['Country Name', 'Country Code'],
                                var_name='Year',
                                value_name='Population')
pop_unpivoted


# Function to unpivot a dataframe
# ----------------------------------------------------------------------------
def unpivot(df, L, cl_var_name, cl_value_name):
    """
    This function returns unpivoted dataframe. 
    L: list of the static columns name.
    var_name: new name for the new columns of unpivoted columns (first row). 
    value_name: new name for the new columns of unpivoted values (second to last rows).
    """
    
    # Check if first introduced object is a dataframe
    if not isinstance(df, pd.DataFrame):
        print("The first introduced argument should be a dataframe.")
        return None

    # Check if the second introduced object is a list
    if not isinstance(L, list):
        print("The second introduced argument should be a list.")
        return None
=======
#define a function to breakdown the GDP investment df into subcategories

def separate_inv(inv_df, ind, value_i, sub_ind, value_s):

#select indicator to be split
    split_1 = inv_df[inv_df[ind] == value_i]

#select sub-indicator to be split
    split_2 = split_1[split_1[sub_ind] == value_s]

#drop indicator/subindicator columns
    split_2.drop(ind,axis=1,inplace=True)
    split_2.drop(sub_ind,axis=1,inplace=True)

#drop years 2020 and onwards
    split_2.drop(split_2.iloc[:,-9:], axis=1,inplace=True)

    return split_2

GDP_pct = separate_inv(investment_GDP_df,"Indicator",'Travel and Tourism total contribution to GDP','Subindicator Type','Percentage share of total GDP')

GDP_govt = separate_inv(investment_GDP_df,"Indicator",'Government spending on travel and Tourism service','Subindicator Type',"US$ in bn (Real prices)")

GDP_govt_pct = separate_inv(investment_GDP_df,"Indicator",'Government spending on travel and Tourism service','Subindicator Type',"% share of total tourism expenditure")

GDP_cap = separate_inv(investment_GDP_df,"Indicator",'Capital investment in Travel and Tourism','Subindicator Type',"US$ in bn (Real prices)")

    # Check if the third introduced object is a string value
    if not isinstance(cl_var_name, str):
        print("The third introduced argument should be a string value.")
        return None

    # Check if the fourth introduced object is a string value
    if not isinstance(cl_var_name, str):
        print("The fourth introduced argument should be a string value.")
        return None

    # Unpivot dataframe
    unpivoted_df = df.melt(id_vars=L,
                           var_name=cl_var_name,
                           value_name=cl_value_name)
    return unpivoted_df


# ----------------------------------------------------------------------------    

# Get the documentation of the unpivot function
unpivot.__doc__

# Using the wrong argument instead of a dataframe
unpivot([1, 2, 3], ['Country Name', 'Country Code'], 'Year', 'Population')

# Using the wrong argument instead of a list on the second argument
unpivot(population, 'Country Name', 'Year', 'Population')

# Using the wrong argument instead of a list on the third argument
unpivot(population, ['Country Name', 'Country Code'], 2, 'Population')

# Using unpivot function
unpivot_pop = unpivot(population, ['Country Name', 'Country Code'], 'Year', 'Population')
unpivot_pop.head()
list(unpivot_pop.columns)

# define a function to fill in missing values in each column using kmean regressor
def kmeans_fillna(df, X, y, y_pred):
    # select the variable to be predicted
    dependent = df[y]

    # select the other variables to be used in the regressor for prediction and fill in their missing values with respective averages
    # (avg fillna applied because kmeans regressor doesn't work with variables that have missing values)
    tempavg = df[X].fillna(df.mean())

    # merge the two tables together for analysis
    reg = pd.concat([dependent, tempavg], axis=1).apply(pd.to_numeric)

    # splitting the reg dataframe to incomplete table
    # contains the rows of each Nan value of the dependent variable in reg df
    incomplete = reg[reg[y].isna()]

    # splitting the reg dataframe to complete table
    # contains the rows of each valid value of the dependent variable in reg df
    complete = reg[~reg.index.isin(incomplete.index)]

    # setting the kmeans regressor using euclidean distances
    regressor = KNeighborsRegressor(10, weights='distance', metric='euclidean')

    # applying the regressor to the dataframe
    fitting = regressor.fit(complete.loc[:, X], complete.loc[:, [y]])

    # predicting the values in the incomplete table
    incomplete[y_pred] = fitting.predict(incomplete.drop(columns=[y]))

    # cleaning the incomplete df and getting ready to merge back to the original dataframe
    incomplete.drop(X, axis=1, inplace=True)
    incomplete.drop(y, axis=1, inplace=True)

    # applying concatenate to the original df
    df = pd.concat([df, incomplete], axis=1)

    # fillna of dependent and predicted columns with 0, to be able to add back to the original df
    df[[y, y_pred]] = df[[y, y_pred]].fillna(0)

    # add the new values to the original column in the original df
    df[y] = df[y] + df[y_pred]

    # drop the predicted column from the original df
    df.drop(columns=[y_pred], inplace=True)

    # return the original df
    return df

data_url = "https://goo.gl/ioc2Td"
gapminder = pd.read_csv(data_url)
gapminder_numeric =gapminder.iloc[0:50,2:4]
gapminder_NaN = gapminder_numeric.mask(np.random.random(gapminder_numeric.shape)<0.3)
merged_df=pd.concat([gapminder.iloc[0:50,0:2],gapminder_NaN],axis=1)
merged_df.columns
filled_df=kmeans_fillna(merged_df,['gdpPercap_1952'],'gdpPercap_1957','gdpPercap_1957_2')
assert_frame_equal(merged_df,filled_df)
df = pd.concat([filled_df,merged_df], axis=1)
df.to_csv('compare_result.csv')


#clear other df from memory
del tourist_df, receipt_df

