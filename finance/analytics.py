import pandas as pd
import numpy as np
from .models import *
from decimal import Decimal

def sum_by_value(movimentacao):

    movimentacao = movimentacao.values()

    if movimentacao:
        df = pd.DataFrame(movimentacao)

        return df["value"].sum()
    
    return Decimal(0.0)