This repo contains code and data for studying relationship between ethnicity and income level.

We download data from [stat-xplore](https://stat-xplore.dwp.gov.uk/)  to download  60 per cent of median net household income before and after housing costs, ethnicity with values above and below the median income levels. 
We clean up the data and read them into pandas dataframe and plot using plotly.   The original data is a weighted sum of income distribution, not no. of households.  So we need to compare this to the total to get the % of ethnic group having lower income. 
Also, as suggested by DWP, we calculate 3 year average and plot the trend as shown in the following.


![image](https://github.com/user-attachments/assets/17ad563b-7048-4e4c-b1ab-8654011f6b38)



![image](https://github.com/user-attachments/assets/95f86f54-fc8d-4494-8915-deac432b16de)


mig_lsoa.py

This file uses data from  [census 2021] (https://www.nomisweb.co.uk/sources/census_2021_mig) and sum up all the migrant numbers in each LSOA for asian, black, multiple ethnicity groups.  This is basically all non-white migrants in each area.  We calculate the percentage of this population in the total migrant population.  Then we normalize the pct to range of 0 to 10.  
