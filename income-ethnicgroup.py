import pandas as pd

import plotly.express as px
import sys

BHC_file='./BHC-cleanedup.csv'

AHC_file='./AHC-cleanedup.csv'

is_AHC = ('AHC' in sys.argv)


# Load the dataset

data_file = AHC_file if is_AHC else BHC_file
df = pd.read_csv(data_file, header=[0, 1], index_col=0)

# Flatten the multi-index columns into year-yes, year-no, year-total
new_columns = []
year_list=[]
current_year = ''
for col in df.columns:
    print(col)
    if 'Unnamed' not in col[0]:
        current_year = col[0].split("-")[0].strip()  #keep only the start year.. 1994-95 becomes 1994
        current_year=int(current_year)+1  # add 1 to year so we get 1995 as the year
        year_list.append(current_year )

    if "Not in low income" in col[1]: # shorten the in low income group, not in low income group
        category="No"
    elif "In low income" in col[1]:
        category="Yes"
    else:
        category=col[1]
    new_columns.append(f'{current_year}-{category}')

df.columns = new_columns

df = df.reset_index()

# Rename the 'index' column to 'Ethnic Group'
df = df.rename(columns={'index': 'Ethnic Group'})

df=df.set_index('Ethnic Group')
# Display the first few rows of the DataFrame
print(df.head())

# convert to numbers
df = df.apply(pd.to_numeric, errors='coerce')

pct_cols=[]
# Iterate over the years in the columns, calcuate the pct of those in low income group over the total in group
for year in year_list:
    yes_col = f"{year}-Yes"
    no_col = f"{year}-No"
    total_col = f"{year}-Total"
    
    # Calculate the percentage of 'no' for each year
    pct_cols.append(f"{year}")
    df[f"{year}"] = round(df[yes_col] / df[total_col] * 100,2)


print(df)
# keep the pct columns only
df=df[pct_cols]
df_ma=pd.DataFrame(index=df.index)
    

# transpose the dataframe 
df_transposed = df.T
print(df)
# Reset index to make ethnic groups a column
df_transposed.reset_index(inplace=True)

print(df_transposed)


# Melt the DataFrame to long format for Plotly
df_melted = df_transposed.melt(id_vars='index', var_name='Ethnic Group', value_name='Value')
df_melted.rename(columns={'index': 'Year'}, inplace=True)
print(df_melted)

df_melted['MA'] = df_melted.groupby('Ethnic Group')['Value'].transform(lambda x: x.rolling(3, 1).mean())
print(df_melted)
# Create the line plot
chart_title='Change in % of Low income group by ethnic group '+ ("- after housing cost" if is_AHC else "- before housing cost")
fig = px.line(df_melted, x='Year', y='MA', color='Ethnic Group', 
              title=chart_title,
              labels={'Value': '% of Low income', 'Year': 'Year'})

# Show the plot
fig.show()

