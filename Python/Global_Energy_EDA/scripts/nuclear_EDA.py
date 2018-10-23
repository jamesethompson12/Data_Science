#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:20:08 2018

@author: jamesthompson
"""


import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import pylab
import os


# ---------------------------------------------------------------------
# Data import and cleansing for EDA
# ---------------------------------------------------------------------

# import path for raw data within this project
import_path = os.getcwd() + '/Global_Energy_EDA/data/raw/'


# filenames to be imported with NaNs specific to imported files  
  
filenames = ['nuclear_generation', 'nuclear_consumption']
na_vals=['', '-', 'n/a', '^', '_']


# create the full filename(s) with path and extension
files = [import_path + file + '.csv' for file in filenames]

generation_df = pd.read_csv(files[0], na_values=na_vals, skiprows=2, skipfooter=14, engine='python', parse_dates=True)
consumption_df = pd.read_csv(files[1], na_values=na_vals, skiprows=2, skipfooter=14, engine='python')



def data_cleanse(dataframe) :
    """ Set the leftmost column as the index and filter out unwanted rows / columns
        Unwanted rows contain NaNs or in index Totals
        Unwanted last three columns are summary columns """
    
    # set index to equal the first column and drop the remaining copy
    dataframe.set_index(dataframe.iloc[:, 0], inplace=True)
    dataframe.drop(dataframe.columns[[0, -3, -2, -1]], axis=1, inplace=True)
    
    # remove null index values (blank rows) from the data frame
    data_index = ~dataframe.index.isnull()
    dataframe = dataframe[data_index]
    
     # create a 1-D index list in string format, then iterate to identify 'Total'
    data_index_tot = [False if ind.startswith('Total') else True for ind in dataframe.index.astype(str)]
    dataframe = dataframe[data_index_tot]
    
    return dataframe
    


generation_df = data_cleanse(generation_df)
consumption_df = data_cleanse(consumption_df)

# ensure the indexes for both dataframes match
if generation_df.index.values.tolist() != consumption_df.index.values.tolist() :
    generation_df.set_index(consumption_df.index)
else: print('Dataframes\' indexes match!')

# tidy data format: transpose the dataframes to make observations by year and countries as factors

def rename_cols(dataframe, col_position, new_label):
    col_vals = dataframe.columns.values.tolist()
    return col_vals

generation_df_yr = generation_df.transpose()
#generation_df_yr.columns[0] = 'Country'

consumption_df_yr = consumption_df.transpose()
#consumption_df_yr.columns[0] = 'Country'

# generate datetime index to substitute year text in indexes
coldates = pd.date_range(start='1965-01-01', end='2017-01-01', periods=53)

generation_df_yr['year'] = coldates
generation_df_yr.set_index('year', inplace=True)

consumption_df_yr['year'] = coldates
consumption_df_yr.set_index('year', inplace=True)



# ---------------------------------------------------------------------
# EDA
# ---------------------------------------------------------------------

def report_complete_countries(dataframe, start = '', end = ''):
    """ Return a list of countries with complete entries for the specified 
        time (or throughout by default)"""
    # if time period specified, 
    if len(start) > 0 and len(end) > 0 :
        dataframe = dataframe.loc[:, start : end]
        
    country_list = dataframe.dropna().index.values.tolist()
    
    return country_list
    


# check to see if the list of countries recording measured values over the last ten years is the same for the last 10 yrs.
ten_years_gen = report_complete_countries(generation_df, '2007', '2017')
ten_years_con = report_complete_countries(consumption_df, '2007', '2017')
ten_years_match = ten_years_gen == ten_years_con



# conversion of million tonnes oil equivalent (consumption) to terawatt-hours (generation)
#ter_w_hrs = 1.163 * 10**-5
ter_w_hrs = 4.4 # according to units conversion provided with data

countries_list = consumption_df.index.values.tolist()
europe_list = countries_list[14:46]

consumption_eu_std = consumption_df_yr.loc[:, europe_list] * ter_w_hrs


# filter dfs for top results
top_consumers_eu = pd.Series(consumption_eu_std.sum())
top_consumers_eu = top_consumers_eu[top_consumers_eu > 0].sort_values(ascending=False)

consumption_eu_std = consumption_eu_std.loc[:, top_consumers_eu.index]
generation_eu = generation_df_yr.loc[:, top_consumers_eu.index]


# save figures in figs directory
fig_dir = os.getcwd() + '/Global_Energy_EDA/figs/'

# plot graphs for consumption and generation within EU countries, in descending order of proportion consumed
consumption_eu_std.plot(title='European Nuclear Energy Consumption')
pylab.xlabel('Year')
pylab.ylabel('Energy consumption (twh)')
plt.legend(bbox_to_anchor=(1, 1))
# save and show 
pylab.savefig(fig_dir + 'europe_consumption.png', bbox_inches='tight')
plt.show()
plt.clf()

generation_eu.plot(title='European Nuclear Energy Production')
pylab.xlabel('Year')
pylab.ylabel('Energy generation [twh]')
plt.legend(bbox_to_anchor=(1, 1))
# save and show 
pylab.savefig(fig_dir + 'europe_production.png', bbox_inches='tight')
plt.show()
plt.clf()

# plot graph of po=roportions consumed / produced per year
prop_consumption_df = consumption_eu_std / generation_df_yr
prop_consumption_df = prop_consumption_df.loc['1975':'2017', top_consumers_eu.index]

# resample to show means over 5yr periods (showing average suprlus or defecit per 5yr period by country)
prop_consumption_df = prop_consumption_df[:].resample('5Y').mean()

prop_consumption_df.plot(title='Mean Ratio of Produced:Consumed for Nuclear Energy in Europe')
pylab.xlabel('Year')
pylab.ylabel('Proportion of produced energy consumed (mean / 5yr)')
plt.legend(bbox_to_anchor=(1, 1))
# save and show 
pylab.savefig(fig_dir + 'europe_proportion_5yr_mean.png', bbox_inches='tight')
plt.show()


