import numpy as np
import pandas as pd


def bold(text):
    """
    Takes a string and returns it bold.
    """
    return '\033[1m'+text+'\033[0m'


def print_string_series(series, max_rows=100):
    """
    Pretty print `series` of strings.
    """
    n = 1
    for i, v in zip(series.index, series.values):
        print('{}: {}'.format(bold(str(i)), v))
        n = n + 1
        if n > max_rows:
            break


def check_guarda_compartilhada(df, col_subordinada, col_raiz, drop_unique=True):
    """
    Return a Series whose index are the unique
    entries in `df` (DataFrame) column `col_subordinada`
    (str or list of str) and values are arrays of unique 
    entries in `col_raiz` (str) that appear in `df` 
    associated to each index.
    
    This function can be used to:
    - Double check that elements in `col_subordinada`
      are subdivisions of `col_raiz` completely contained
      in each element of `col_raiz`.
    - Find out which ramifications of `col_subordinada` there
      are listed in column `col_raiz`.
    """
    
    n_raiz_por_subordinado = df.groupby(col_subordinada)[col_raiz].unique()
    if drop_unique:
        return n_raiz_por_subordinado.loc[n_raiz_por_subordinado.str.len() > 1]
    else:
        return n_raiz_por_subordinado


def print_array_series(series):
    """
    Print a Series of arrays.
    """
    n = len(series)
        
    for i in range(n):
        print(bold(str(series.index[i]) + ': ') + ' / '.join(series.iloc[i]))


def crop_strings(series, str_range, ellipsis='…'):
    """
    Get slices of the strings, marking the removed ends 
    with ellipsis.
    
    Parameters
    ----------
    series : Pandas Series or Index object.
        The array-like containing the strings to slice.
    str_range : tuple of non-negative ints
        The positions (inclusive, exclusive) where to 
        slice the string.
    ellipsis : str
        The string representing an ellipsis, to be 
        added to cropped strings.
    
    Returns
    -------
    str_arr : array pr Series
        An array of sliced strings, with ellipsis marking
        the removal of string parts when required. Return 
        a Series with the same index as `series` if the 
        latter is a Series object.
    """
    
    if str_range[0] == 0:
        y = np.where((series.str.len() > str_range[1]), series.str.slice(*str_range) + ellipsis, series)
    else:
        y = np.where((series.str.len() > str_range[1] - str_range[0]), ellipsis + series.str.slice(*str_range) + ellipsis, ellipsis + series.str.slice(*str_range))
        
    if type(series) == pd.core.series.Series:
        return pd.Series(y, index=series.index)
    else:
        return y


def date_series_replace(series, year=None, month=None, day=None):
    """
    Replace date elements with the ones specified.
    
    Parameters
    ----------
    series : datetime Series
        The series with dates to be altered.
    year : int
        The fixed year used to replace the year in `series`.
    month : int
        The fixed month used to replace the year in `series`.
    day : int
        The fixed day used to replace the year in `series`.
    
    Returns
    -------
    date_series : datetime Series
        A new series like `series` but with the replacements
        made.
    """
    return pd.to_datetime(
        {'year':  series.dt.year if year is None else year,
         'month': series.dt.month if month is None else month,
         'day':   series.dt.day if day is None else day})
