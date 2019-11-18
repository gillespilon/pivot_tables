#! /usr/bin/env python3


'''
Example of pivot tables
'''


import pandas as pd
import numpy as np


def byte_size(num, suffix='B'):
    '''
    Convert bytes to appropriate multiple.
    '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


def dataframe_info(df):
    print(f'Dataframe information',
          f'\nColumn names   : ', list(df),
          f'\nRows         : ', df.shape[0],
          f'\nColumns      : ', df.shape[1],
          f'\nMemory usage :', byte_size(df.memory_usage(index=True).sum()))


df = pd.read_excel('sales-funnel.xlsx')
dataframe_info(df)
print('\n', df.head())


# Pivot table using index and values parameters.
# By default the aggfunc is the average.
pd.pivot_table(df, values=['Price'], index=['Manager']).round(2)
# To be explicit.
pd.pivot_table(df,
               values=['Price'],
               index=['Manager'],
               aggfunc='mean').round(2)
# The index can have multiple levels.
pd.pivot_table(df,
               values=['Price'],
               index=['Manager', 'Rep'],
               aggfunc='mean').round(2)
# The aggfunc can have several parameters.
pd.pivot_table(df,
               values=['Price'],
               index=['Manager', 'Rep'],
               aggfunc=[np.mean, np.sum, len]).round(2)
# The columns parameter is optional.
# It provides an additional way to segment values.
# The index can have multiple levels.
pd.pivot_table(df,
               values=['Price'],
               index=['Manager', 'Rep'],
               columns=['Product'],
               aggfunc=[np.sum]).round(2)
# Replace the NaN with 0.
pd.pivot_table(df,
               values=['Price'],
               index=['Manager', 'Rep'],
               columns=['Product'],
               aggfunc=[np.sum],
               fill_value=0).round(2)
# Add another column to the values parameter.
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Rep'],
               columns=['Product'],
               aggfunc=[np.sum],
               fill_value=0).round(2)
# Move the product column to the index.
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Rep', 'Product'],
               aggfunc=[np.sum],
               fill_value=0).round(2)
# Show totals.
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Rep', 'Product'],
               aggfunc=[np.sum],
               fill_value=0,
               margins=True).round(2)
# Change the categories to look at the Manager level,
# add Status, remove Quantity.
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Status'],
               aggfunc=[np.sum],
               fill_value=0,
               margins=True).round(2)
# Pass a dictionary to the aggfunc to perform different functions.
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Status'],
               columns=['Product'],
               aggfunc={'Quantity': len, 'Price': np.sum},
               fill_value=0,
               margins=True).round(2)
# Pass a dictionary to the aggfunc to perform different functions.
# Each value can have a dictionary. Need to remove totals (why?).
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Status'],
               columns=['Product'],
               aggfunc={'Quantity': len, 'Price': [np.sum, np.mean]},
               fill_value=0).round(2)
# Do this again and save to a variable.
table = pd.pivot_table(df,
                       values=['Price', 'Quantity'],
                       index=['Manager', 'Status'],
                       columns=['Product'],
                       aggfunc={'Quantity': len, 'Price': [np.sum, np.mean]},
                       fill_value=0).round(2)
# Sort on one column, price.
table.sort_values(by=('Price', 'mean', 'CPU'), ascending=False)
# Filter for one manager.
table.query('Manager == ["Debra Henley"]')
# Or just string the query method to the previous code.
# Pass a dictionary to the aggfunc to perform different functions.
# Each value can have a dictionary. Need to remove totals (why?).
pd.pivot_table(df,
               values=['Price', 'Quantity'],
               index=['Manager', 'Status'],
               columns=['Product'],
               aggfunc={'Quantity': len, 'Price': [np.sum, np.mean]},
               fill_value=0).round(2).query('Manager == ["Debra Henley"]')
# Another query.
table.query('Status == ["pending", "won"]')
# And another query.
table.query('Status == ["pending", "won"]')\
     .query('Manager == ["Debra Henley"]')
# Or this way.
table.query('Status == ["pending", "won"] & Manager == ["Debra Henley"]')
