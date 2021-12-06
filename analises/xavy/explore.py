#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Tue Oct  5 17:37:29 2021

@author: skems
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl

from xavy.dataframes import crop_strings

#############################
### From old utils module ###
#############################

def bold(text):
    """
    Takes a string and returns it bold.
    """
    return '\033[1m'+text+'\033[0m'


def unique(series):
    """
    Takes a pandas series as input and print all unique values, separated by 
    a blue bar.
    """
    u = series.unique()
    try:
        print(bold(str(len(u)))+': '+'\033[1;34m | \033[0m'.join(sorted(u.astype(str))))
    except:
        print(bold(str(len(u)))+': '+'\033[1;34m | \033[0m'.join(sorted(u)))


def columns(df):
    """
    Print the number of columns and their names, separated by a blue bar.
    """
    unique(df.columns)

    
def mapUnique(df):
    """
    Takes a pandas dataframe and prints the unique values of all columns and 
    their numbers. If the number of unique values is greater than maxItems, 
    only print out a sample.  
    """
    python_version = int(sys.version.split('.')[0])
    maxItems = 20
    
    for c in df.columns.values:
        try:
            u = df[c].unique()
            n = len(u)
        except TypeError:
            u = np.array(['ERROR (probably unhashable type)'])
            n = 'Unknown'
        if python_version == 2:
            isStr = all([isinstance(ui, basestring) for ui in u])
        else:
            isStr = all([isinstance(ui, str) for ui in u])
        print('')
        print(bold(c+': ')+str(n)+' unique values.')
        
        if n == 'Unknown':
            n = 1
        if n <= maxItems:
            if isStr:
                try:
                    print(',  '.join(np.sort(u)))
                except:
                    print(',  '.join(np.sort(u.astype('unicode'))))
            else:
                try:
                    print(',  '.join(np.sort(u).astype('unicode')))
                except:
                    print(',  '.join(np.sort(u.astype('unicode'))))
        else:
            if isStr:
                try:
                    print(bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False))))
                except:
                    print(bold('(sample) ')+',  '.join(np.sort(np.random.choice(u.astype('unicode'),size=maxItems,replace=False))))
            else:
                try:
                    print(bold('(sample) ')+',  '.join(np.sort(np.random.choice(u,size=maxItems,replace=False)).astype('unicode')))
                except:
                    print(bold('(sample) ')+',  '.join(np.sort(np.random.choice(u.astype('unicode'),size=maxItems,replace=False))))


def checkMissing(df):
    """
    Takes a pandas dataframe and prints out the columns that have 
    missing values.
    """
    colNames = df.columns.values
    print(bold('Colunas com valores faltantes:'))
    Ntotal = len(df)
    Nmiss  = np.array([float(len(df.loc[df[c].isnull()])) for c in colNames])
    df2    = pd.DataFrame(np.transpose([colNames,[df[c].isnull().any() for c in colNames], Nmiss, np.round(Nmiss/Ntotal*100,2)]),
                     columns=['coluna','missing','N','%'])
    print(df2.loc[df2['missing']==True][['coluna','N','%']])


def one2oneQ(df, col1, col2):
    """
    Check if there is a one-to-one correspondence between two columns in a 
    dataframe.
    """
    n2in1 = df.groupby(col1)[col2].nunique()
    n1in2 = df.groupby(col2)[col1].nunique()
    if len(n2in1)==np.sum(n2in1) and len(n1in2)==np.sum(n1in2):
        return True
    else:
        return False


def one2oneViolations(df, colIndex, colMultiples):
    """
    Returns the unique values in colMultiples for a fixed value in colIndex 
    (only for when the number of unique values is >1).
    """
    return df.groupby(colIndex)[colMultiples].unique().loc[df.groupby(colIndex)[colMultiples].nunique()>1]


##########################
### Plotting functions ###
##########################


def plot_categorical_dist(series, max_cat=30, cat_slice=(0, 30), normalize=False, horizontal='auto', **kwargs):        
    """
    Plot a histogram (actually a bar plot) for instaces 
    of a categorical variable. 
    
    Parameters
    ----------
    series : Pandas Series
        The instances of a categorical variable. They can 
        be strings or numbers.
    max_cat : int
        Maximum number of categories to plot. Only the 
        most frequent categories will appear.
    cat_slice : tuple of ints
        Cropping range (inclusive, exclusive) for string 
        instances. Parts beyond these limits are removed
        when labeling the plot bars.
    normalize : bool
        Whether to plot should be normalized to the total
        number of instances.
    horizontal : bool or 'auto'
        Whether the bars should be horizontal or vertical.
        If 'auto', guess based on the length the the string
        categories, otherwise use vertical.
    kwargs : other
        Arguments for the plot.
    """
    
    counts = series.value_counts(ascending=False, normalize=normalize)
    
    # If categories are strings:
    try:
        counts.index = crop_strings(counts.index, cat_slice)
        # Decide bar direction:
        if horizontal == 'auto':
            if counts.index.str.len().max() > 10:
                horizontal = True
            else:
                horizontal = False
    # If categories are not strings:
    except AttributeError:
        if horizontal == 'auto':
            horizontal = False
    
    # Limit the number of bars by removing least frequent categories:
    counts = counts.iloc[:max_cat]
    
    # Plot:
    if horizontal == True:
        counts.iloc[::-1].plot(kind='barh', **kwargs)
    else:
        counts.plot(kind='bar', **kwargs)
        

def multiple_dist_plots(df, dtypes, n_cols=5, new_fig=True, fig_width=25, subplot_height=5, normalize=False, max_cat=30, cat_slice=(0, 30), n_bins='auto', **kwargs):
    """
    Create one plot of the distribution of values for each column 
    in a DataFrame.
    
    Parameters
    ----------
    df : DataFrame
        Data for which to plot the distribution.
    dtypes : list of str or of None
        Types of the data for each column in `df`. It can be
        'cat' (for categorical distribution), 'num' (for numerical
        distribution, a.k.a a histogram), 'log'(same as 'num' but 
        for the base-10 log of the values) or None (no plot for this 
        column).
    n_cols : int
        Number of columns in the grid of subplots.
    fig_width : float
        Width of the figure containing all subplots.
    subplot_height : float
        Approximate height of each subplot.
    normalize : bool
        Whether to normalize the plots by the number of instances 
        in `df`. For histograms (i.e. columns with 'num' or 'log'
        dtypes), plot the density.
    max_cat : int
        Maximum number of categories to include in the categorical
        plots (the most frequent ones are shown).
    cat_slice : tuple of ints
        Crop window applied to the categories' labels when drawing 
        a categorical plot. The categories names are cropped to this
        range.
    n_bins : int, array-like of floats or 'auto'
        Number of bins to use in histograms (plots for 'num' or 'log'
        columns), or edges of the bins (if array). If 'auto', decide
        the binning internally in an independent way for each plot.
    kwargs : other
        Parameters passed to the plots.
    """
    # Security checks:
    assert len(dtypes) == len(df.columns), '`dtypes` must contain one entry per `df` column.'
    assert set(dtypes) - {'cat', 'num', 'log', None} == set(), "`dtypes` can only contain the elements: 'cat', 'num', 'log' and None."
    
    # Count plots:
    n_plots = len(list(filter(lambda x: x != None, dtypes)))
    n_rows  = int(n_plots / n_cols) + 1

    if new_fig == True:
        pl.figure(figsize=(fig_width, subplot_height * n_rows))
    panel = 0
    for i in range(len(dtypes)): 
        # One column:
        dtype  = dtypes[i]
        col    = df.columns[i]
        series = df[col]
        
        if dtype != None:
            # One plot:
            panel += 1
            pl.subplot(n_rows, n_cols, panel)
            pl.title(col)
            
            # Categorical:
            if dtype == 'cat':
                plot_categorical_dist(series, max_cat, cat_slice, normalize, **kwargs)
            # Numerical:
            if dtype in ('num', 'log'):
                if n_bins == 'auto':
                    bins = min(min(200, series.nunique()), int(np.round(len(series) / 10)))
                else:
                    bins = n_bins
                if dtype == 'log':
                    np.log10(series).hist(bins=bins, density=normalize, **kwargs)
                else:
                    series.hist(bins=bins, density=normalize, **kwargs)
            
    pl.tight_layout()
