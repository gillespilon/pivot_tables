#! /usr/bin/env python3
"""
Example of pivot tables
"""

import datasense as ds
import pandas as pd
import numpy as np


def main():
    pd.options.display.width = 220
    pd.options.display.max_columns = 220
    pd.options.display.max_rows = 220
    output_url = 'pivot_table.html'
    header_title = 'Pivot tables'
    header_id = 'pivot-tables'
    original_stdout = ds.html_begin(
        output_url=output_url,
        header_title=header_title,
        header_id=header_id
    )
    df = pd.read_excel('sales-funnel.xlsx')
    ds.dataframe_info(
        df=df,
        file_in='sales-funnel.xlsx'
    )
    print(df.head())
    print()
    print('Pivot table, implicit parameters')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager']
        ).round(2)
    )
    print()
    print('Pivot table, explicit parameters')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager'],
            aggfunc='mean'
        ).round(2)
    )
    print()
    print('Pivot table, multiple-level index')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager', 'Rep'],
            aggfunc='mean'
        ).round(2)
    )
    print()
    print('Pivot table, multi-parameter aggfunc')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager', 'Rep'],
            aggfunc={'Price': [np.mean, np.sum, len]}
        ).round(2)
    )
    print()
    print('Pivot table, columns parameter is optional')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager', 'Rep'],
            columns=['Product'],
            aggfunc=[np.sum]
        ).round(2)
    )
    print()
    print('Pivot table, replace NaN with 0')
    print(
        pd.pivot_table(
            data=df,
            values=['Price'],
            index=['Manager', 'Rep'],
            columns=['Product'],
            aggfunc=[np.sum],
            fill_value=0
        ).round(2)
    )
    print()
    print('Pivot table, add second colume to values parameter')
    print(
        pd.pivot_table(
            data=df,
            values=['Price', 'Quantity'],
            index=['Manager', 'Rep'],
            columns=['Product'],
            aggfunc=[np.sum],
            fill_value=0
        ).round(2)
    )
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
    table = pd.pivot_table(
        df,
        values=['Price', 'Quantity'],
        index=['Manager', 'Status'],
        columns=['Product'],
        aggfunc={'Quantity': len, 'Price': [np.sum, np.mean]},
        fill_value=0
    ).round(2)
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
    ds.html_end(
        original_stdout=original_stdout,
        output_url=output_url
    )


def byte_size(num, suffix='B'):
    '''
    Convert bytes to appropriate multiple.
    '''
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


if __name__ == '__main__':
    main()
