#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 14:20:08 2018

@author: jamesthompson
"""


import pandas as pd
import os

# import path for raw data within this project
import_path = os.getcwd() + '/Global_Energy/data/raw/'


# filenames to be imported with NaNs specific to imported files  
  
filenames = ['nuclear_generation', 'nuclear_consumption']
na_vals=['', '-', 'n/a', '^', '_']


# create the full filename(s) with path and extension
files = [import_path + file + '.csv' for file in filenames]

generation_df = pd.read_csv(files[0], na_values=na_vals, skiprows=2, skipfooter=14, engine='python')
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



def report_complete_countries(dataframe, start = '', end = ''):
    """ Return a list of countries with complete entries for the specified 
        time (or throughout by default)"""
    #if time period specified, 
    if len(start) > 0 and len(end) > 0 :
        dataframe = dataframe.loc[:, start : end]
        
    country_list = dataframe.dropna().index.values.tolist()
    
    return country_list
    



ten_years_gen = report_complete_countries(generation_df, '2007', '2017')
ten_years_con = report_complete_countries(consumption_df, '2007', '2017')

print(ten_years_gen == ten_years_con)

# 
