import locale
import pandas as pd

locale.setlocale( locale.LC_ALL, 'english_USA' )
def get_int(x):
    """
    parse int from strings, e.g. '1,200'
    """
    # x=NaN
    if pd.isnull(x):
        return x
    # try whether string x can be directed cast as int
    try:
        return int(x)
    # if can't, use the package locale to parse it
    except:
        return locale.atoi(x)
        
        
def save_dict_of_list(data, fn):
    with open(fn, 'wb') as f:
        for k, l in data.items():
            line = '{}\t{}\n'.format(k, ' '.join([str(x) for x in l]))
            f.write(line)