def month_name_to_num(month_name):
    """
    Translate a `month_name` (str) to a number (int) from 
    1 to 12. Works with portuguese and english, and with 
    full name and 3-letter abbreviation.
    """
    
    translate_dict = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6, 
                      'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12, 
                      'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6, 
                      'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12, 
                      'marco': 3, 'feb': 2, 'apr': 4, 'may': 5, 'aug': 8, 'sep': 9, 'oct': 10, 'dec': 12, 
                      'january': 1, 'february': 2, 'march': 3, 'april': 4, 'june': 6, 
                      'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
    
    return translate_dict[month_name.lower().strip()]


def parse_ptbr_number(string):
    """
    Input: a string representing a float number in Brazilian currency format, e.g.: 1.573.345,98
    
    Returns the corresponding float number.
    """
    number = string
    number = number.replace('.', '').replace(',', '.')
    return float(number)


def parse_ptbr_series(string_series):
    """
    Input: a Series of strings representing a float number in Brazilian currency format, e.g.: 1.573.345,98
    
    Returns a Series with the corresponding float number.
    """
    
    number_series = string_series.str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    return number_series
