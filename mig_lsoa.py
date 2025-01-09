import pandas as pd

import plotly.express as px
import sys

import os


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from util import normalize_to_range

def read_csv(data_file):

    df = pd.read_csv(data_file, header=[0])
    # Flatten the multi-index columns into year-yes, year-no, year-total


    print("---- dataframe loaded:")

    print(df.head())
    
    return df

def combine_other_ethnic_groups(df):
    # Group by 'Group' and calculate the sum for non-white ethnicities
    AGGR_BY={'Percentage': 'sum','Count':'sum'}
    #AGGR_BY={'Count':'sum'}
    
    GROUP_BY=['Lower layer Super Output Areas code','Lower layer Super Output Areas label','Migration LSOA (inflow) (6 categories) code','Migration LSOA (inflow) (6 categories) label']
    others_df = df[df['Ethnic group (6 categories) label'] != 'White'].groupby(GROUP_BY, as_index=False).agg(AGGR_BY)
    #others_df = df[df['Ethnic group (6 categories) label'] != 'White'].groupby(['Lower layer Super Output Areas code','Lower layer Super Output Areas label','Migration LSOA (inflow) (6 categories) code','Migration LSOA (inflow) (6 categories) label'], as_index=False).agg({'Percentage': 'sum','Count':'sum'})
    others_df['Ethnic group (6 categories) label'] = 'others'
    others_df['Ethnic group (6 categories) code']=0
    others_df.to_csv("./temp.csv")
    print(others_df)
    # Combine the original DataFrame with the others DataFrame for whites
    combined_df = pd.concat([df[df['Ethnic group (6 categories) label'] == 'White'], others_df[['Lower layer Super Output Areas code', 'Lower layer Super Output Areas label','Migration LSOA (inflow) (6 categories) code','Migration LSOA (inflow) (6 categories) label','Ethnic group (6 categories) code','Ethnic group (6 categories) label', 'Percentage','Count']]])
    combined_df = combined_df.sort_values(by=['Lower layer Super Output Areas code', 'Ethnic group (6 categories) label']).reset_index(drop=True)

    return combined_df

def cal_pct(df):
    # Calculate total count for each group
    total_counts = df.groupby('Lower layer Super Output Areas code')['Count'].sum().reset_index()
    total_counts.rename(columns={'Count': 'Total'}, inplace=True)

    # Merge total counts back to the combined DataFrame
    df = df.merge(total_counts, on='Lower layer Super Output Areas code')

    # Calculate percentage
    df['Percentage'] = (df['Count'] / df['Total']) * 100

    # Drop the Total column for final output
    df = df.drop(columns='Total')

    # Sort the final DataFrame for better readability
    df = df.sort_values(by=['Lower layer Super Output Areas code', 'Ethnic group (6 categories) code']).reset_index(drop=True)

    return df


if __name__ == "__main__":
    MIG_LSOA='./MIG008EW_LSOA_IN.csv'

    df = read_csv(MIG_LSOA)

    df=df[df['Migration LSOA (inflow) (6 categories) code'] ==5]


    filtered_df = df[(df['Ethnic group (6 categories) code'] == -8) & (df['Count'] != 0)]
    print("----")
    print(filtered_df)
    ## looks like all "does not apply" is of 0 value so we just aggregate the other ethnic group into 1
    
    df = cal_pct(df)
    print("ethnic groups migrated to UK (pct)")
    print(df)
    df.to_csv("./migrate_to_uk.csv")

    combined= combine_other_ethnic_groups(df)
    print("combined non-white groups into 1 group")
    print(combined)

    print("normalize data")
    combined['pct_normalized'] = normalize_to_range(combined.Percentage)
    combined['pct_normalized'] = combined['pct_normalized'].round(2)

    print(combined)
    combined[combined['Ethnic group (6 categories) label'] == 'White'].to_csv("./migrate_to_uk_white.csv")
    combined[combined['Ethnic group (6 categories) label'] != 'White'].to_csv("./migrate_to_uk_other_ethnic.csv")
