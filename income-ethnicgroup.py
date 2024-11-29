import pandas as pd

import plotly.express as px
import sys


# Load the dataset
ASIAN=['Indian','Pakistani','Bangladeshi','Chinese','Any other Asian background']

def read_csv(data_file, is_AHC):

    df = pd.read_csv(data_file, header=[0, 1], index_col=0)
    # Flatten the multi-index columns into year-yes, year-no, year-total
    new_columns = []
    year_list=[]
    current_year = ''
    for col in df.columns:
        #print(col)
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
    print("---- dataframe loaded:")

    print(df.head())
    

    # convert to numbers
    df = df.apply(pd.to_numeric, errors='coerce')

    return df, year_list


def cal_pct(df, year_list):
    pct_cols=[]
    # Iterate over the years in the columns, calcuate the pct of those in low income group over the total in group
    df_copy=df.copy()
    for year in year_list:
        yes_col = f"{year}-Yes"
        no_col = f"{year}-No"
        total_col = f"{year}-Total"
        
        # Calculate the percentage of 'no' for each year
        pct_cols.append(f"{year}")
        df_copy[f"{year}"] = round(df_copy[yes_col] / df_copy[total_col] * 100,2)

    return df_copy, pct_cols

def melt(df, pct_col):
    print(df)
    # keep the pct columns only
    df=df[pct_cols]
    #df_ma=pd.DataFrame(index=df.index)

    # transpose the dataframe 
    df_transposed = df.T
    # Reset index to make ethnic groups a column
    df_transposed.reset_index(inplace=True)
    print("---- after transpose:")

    print(df_transposed)


    # Melt the DataFrame to long format for Plotly
    df_melted = df_transposed.melt(id_vars='index', var_name='Ethnic Group', value_name='Value')
    df_melted.rename(columns={'index': 'Year'}, inplace=True)
    print("---- melted dataframe:")

    print(df_melted)

    return df_melted


    return df_melted

def plot(df_melted, is_AHC):
    print("---- plotting chart:")
    # Create the line plot
    chart_title='Change in % of Low income group by ethnic group '+ ("- after housing cost" if is_AHC else "- before housing cost")
    fig = px.line(df_melted, x='Year', y='MA', color='Ethnic Group', color_discrete_sequence=px.colors.qualitative.Dark24,
#                title=chart_title,
#                labels={'Value': '% of Low income', 'Year': 'Year'}
    )
    fig.update_layout(
        title=dict(text=chart_title, font=dict(size=24, family='Arial, Bold')),
        xaxis=dict(
            title='Year', 
            titlefont=dict(size=18, family='Arial, Bold'), 
            showgrid=True, gridcolor='Lightgray', zeroline=True),
        yaxis=dict(title='Low income %', 
            titlefont=dict(size=18, family='Arial, Bold'), 
            gridcolor='Lightgray', showgrid=True, zeroline=True),
        font=dict(size=16, family='Arial, Bold'),
        plot_bgcolor='rgba(255, 255, 255, 1)',  # white background
        #paper_bgcolor='rgba(255, 255, 255, 1)',  # white paper
    )
    # Show the plot
    fig.show()


def aggreg_asia(df):
    """
        group and sum asian group
    """
    print(df.index)
    filtered_df = df[df.index.isin(ASIAN)]
    print("---- filtered updated dataframe:")
    print(filtered_df)
    # Group by Year and Ethnic Group, then sum the values
    yearly_sums = filtered_df.sum(axis=0)
    print(yearly_sums)
    new_df = df[~df.index.isin(ASIAN)]
    df_copy = new_df.copy()
    df_copy.loc['Asian']=yearly_sums
    #result_df = pd.concat([df, new_df], ignore_index=True)
    print("---- updated dataframe:")
    print(df_copy)
    return df_copy



if __name__ == "__main__":
    BHC_file='./BHC-cleanedup.csv'
    AHC_file='./AHC-cleanedup.csv'
    is_AHC = ('AHC' in sys.argv)

    data_file = AHC_file if is_AHC else BHC_file
    all_df, year_list = read_csv(data_file, is_AHC)
    df=aggreg_asia(all_df)


    df, pct_cols = cal_pct(df, year_list)
    df_melted=melt(df,pct_cols)
    df_melted['MA'] = df_melted.groupby('Ethnic Group')['Value'].transform(lambda x: x.rolling(3, 1).mean())
    #df_melted.to_csv("./income vs ethnicity.csv")
    plot(df_melted, is_AHC)

    asain_df = all_df[all_df.index.isin(ASIAN)]
    asain_df, pct_cols = cal_pct(asain_df, year_list)
    df_melted=melt(asain_df,pct_cols)
    df_melted['MA'] = df_melted.groupby('Ethnic Group')['Value'].transform(lambda x: x.rolling(3, 1).mean())
    plot(df_melted, is_AHC)

