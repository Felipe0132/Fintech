import pandas as pd

def sum_by_value(movimentacao):

    movimentacao = movimentacao.values()

    if movimentacao:
        df = pd.DataFrame(movimentacao)

        return df["value"].sum()
    
    return 0.0