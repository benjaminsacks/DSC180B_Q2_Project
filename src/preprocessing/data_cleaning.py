import pandas as pd


def filter_metadata(df):
    """
    Filters the metadata of outliers for days to death and strange values for analyte_A260A280Ratio
    and aliquot_concentration.

    Input: pandas Dataframe of metadata feature table
    Output: pandas Dataframe of filtered metadata feature table

    """
    df = df[df['days_to_death'] < 10_000]  # Drop NaN's & outliers
    df = df[
        (df['analyte_A260A280Ratio'] > 0) | (df['analyte_A260A280Ratio'].isna())]  # Drop strange values / Keep NaN's
    df = df[
        (df['aliquot_concentration'] < 2) | (df['aliquot_concentration'].isna())]  # Drop strange values / Keep NaN's

    return df


def reduce_stages(col):
    """
    Takes substages and coverts them into their primary stage ex. Stage IA to Stage I.

    Input: pandas Series or Dataframe column
    Output: pandas Series or Dataframe column after transformation
    """
    stage_dict = {'Stage IA': 'Stage I',
                  'Stage IB': 'Stage I',
                  'Stage IS': 'Stage I',
                  'I or II NOS': 'Stage I',

                  'Stage IIA': 'Stage II',
                  'Stage IIB': 'Stage II',
                  'Stage IIC': 'Stage II',

                  'Stage IIIA': 'Stage III',
                  'Stage IIIB': 'Stage III',
                  'Stage IIIC': 'Stage III',

                  'Stage IVA': 'Stage IV',
                  'Stage IVB': 'Stage IV',
                  'Stage IVC': 'Stage IV',
                  }

    if col.name == 'pathologic_stage_label':
        col = col.replace(stage_dict)

    if col.name == 'pathologic_t_label':
        for i in range(5):
            col = col.replace(f'T{i}.*', f'T{i}', regex=True)  # Consolidate T Labels

    if col.name == 'pathologic_n_label':
        for i in range(5):
            col = col.replace(f'N{i}.*', f'N{i}', regex=True)  # Consolidate N Labels

    return col
