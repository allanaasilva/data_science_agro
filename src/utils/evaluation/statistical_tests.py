"""
    Module with statistical functions that will be used
    throughout the analysis.
"""

from typing import Union, Tuple
import pandas as pd
from scipy.stats import kruskal
import scikit_posthocs as sp


def kruskal_nemenyi(data: pd.DataFrame,
                    col_cat: str,
                    col_num: Union[float, int],
                    verbose: bool = True) -> Tuple[float, float,
                                                   pd.DataFrame]:
    """
    Function responsible for applying the Kruskall-Wallis and Nemelyin tests
    to check whether there are statistically significant differences
    between the numerical values of several different groups (>2).

    Parameters:
    - data: Pandas dataframe containing the data.
    - col_cat: Categorical column containing the groups to be tested.
    - col_num: Numeric column containing the values of each group to be tested
    - verbose: If True, print the results; otherwise, do not print.

    Returns:
    - est_kruskal: Kruskal-Wallis test statistic.
    - p_value_kruskal: p-value of the Kruskal-Wallis test.
    - results_nemenyi: DataFrame with p-values of multiple comparisons
    (Nemenyi).
    """

    # Teste de Kruskal-Wallis
    est_kruskal, p_value_kruskal = kruskal(
        *[group[col_num] for _, group in data.groupby(col_cat)]
    )
    # Teste de comparações múltiplas (Nemenyi)
    results_nemenyi = sp.posthoc_nemenyi(
        data, val_col=col_num, group_col=col_cat).round(3)

    # Calcular as diferenças absolutas entre os valores médios
    groups = data.groupby(col_cat)[col_num].mean().reset_index()
    mean_diff = pd.DataFrame(index=results_nemenyi.index,
                             columns=results_nemenyi.columns,
                             dtype=float)
    for _, row in groups.iterrows():
        for _, row2 in groups.iterrows():
            mean_diff.loc[row[col_cat], row2[col_cat]] = abs(
                round(row[col_num], 1) - round(row2[col_num], 1)
            )

    for i in range(mean_diff.shape[0]):
        for j in range(mean_diff.shape[1]):
            if results_nemenyi.iloc[i, j] <= 0.05:
                mean_diff.iloc[i, j] = f"{mean_diff.iloc[i, j]:.1f}*"

    # Se verbose for True, imprimir os resultados
    if verbose:
        print("Estatística de Kruskal-Wallis:", est_kruskal.round(2))
        print("P-valor (Kruskal-Wallis):", p_value_kruskal.round(3))
        print()
        print("Diferenças absolutas entre valores médios:")
        print(mean_diff)
        print('* = Diferenças estatisticamente significativas')

    return est_kruskal, p_value_kruskal, results_nemenyi, mean_diff
