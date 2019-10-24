#import packages
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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
region_df_test=region_df_test.tail(11)
region_cols =region_df_test.columns.values
region_df_test.iloc[2,:].plot(y=region_cols[2:11], kind="bar")

region_cols =region_df_test.columns.values
income_cols = [s for s in list(region_cols) if "income" in s]
dividend_cols =[s for s in list(region_cols) if "dividend" in s]
IDA_IBRD_cols =[s for s in list(region_cols) if ("IDA" in s or "IBRD" in s)]
UN_cols =[s for s in list(region_cols) if "UN" in s]

# Read an example csv file
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




#clear other df from memory
del tourist_df, receipt_df

