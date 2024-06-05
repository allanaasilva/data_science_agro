"""
    Modules with various auxiliary functions that will be used in the analyses
"""

import pandas as pd
import numpy as np
from typing import Union


def ranking_numeric(df: pd.DataFrame,
                    col_num: str,
                    sort: bool = False):
    """
    Function responsible for receiving a numeric column and returning the
    rankings (integers) according to the desired way (descending by default)

    Parameters:
    - df: Pandas dataframe containing the data.
    - col_num: Name of the numeric column containing the numerical values that
    will be used as the basis for the ranking
    - sort: Variable responsible for defining the ranking order
    (descending by default)

    Returns:
    A new column called 'Rank' with the numerical value of the current ranking
    of each row based on the chosen numerical column.
    """

    df['RANK'] = df[col_num].rank(
        method='min', ascending=sort
    ).astype(int)
    return df


def std_medians(data: pd.DataFrame,
                col_cat: str,
                col_num: str) -> float:
    """
    Function responsible for calculating the standard deviation of the medians
    of a categorical variable (group).

    Parameters:
    - data: Pandas dataframe containing the data.
    - col_cat: Name of the categorical column containing the groups.
    - col_num: Name of the numeric column containing the values of each group.

    Returns:
    - std_dev: Standard deviation of the medians.
    """

    # Calcula as medianas de cada grupo
    medians = data.groupby(col_cat)[col_num].median()

    # Calcula o desvio padrão das medianas
    std_dev = np.std(medians)

    return std_dev


def obter_estacao(data: pd.Timestamp) -> Union[str, None]:
    """
    Function responsible for returning the season of the year in Brazil
    based on the date provided.

    Parameters:
    - data: Column name of type 'pandas timestamp'.

    Returns:
    A string indicating the season of the year: 'Verão' (Summer),
    'Outono' (Autumn), 'Inverno' (Winter),'Primavera' (Spring),
    or None if the date is invalid.
    """

    if ((data.month == 12 and data.day >= 21) or
        (data.month == 1) or
        (data.month == 2) or
            (data.month == 3 and data.day < 21)):
        return 'Verão'
    if ((data.month == 3 and data.day >= 21) or
        (data.month == 4) or
        (data.month == 5) or
            (data.month == 6 and data.day < 21)):
        return 'Outono'
    if ((data.month == 6 and data.day >= 21) or
        (data.month == 7) or
        (data.month == 8) or
            (data.month == 9 and data.day < 23)):
        return 'Inverno'
    if ((data.month == 9 and data.day >= 23) or
        (data.month == 10) or
        (data.month == 11) or
            (data.month == 12 and data.day < 21)):
        return 'Primavera'
    return None
