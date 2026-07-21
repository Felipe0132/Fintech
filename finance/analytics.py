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

def sum_by_category(transactions):
    transactions = transactions.values('category__name', 'value')
    df = pd.DataFrame(list(transactions))

    if df.empty:
        return {}

    resultado = df.groupby('category__name')['value'].sum()
    return resultado.to_dict()

def sum_by_account(transactions):
    transactions = transactions.values('account__name', 'value')
    df = pd.DataFrame(list(transactions))

    if df.empty:
        return {}

    resultado = df.groupby('account__name')['value'].sum()
    return resultado.to_dict()

def total_by_account(transactions):
    transactions = transactions.values('account__name', 'value', 'type')
    df = pd.DataFrame(list(transactions))

    if df.empty:
        return {}

    df.loc[df["type"]=="G", "value"] = df["value"] * -1

    resultado = df.groupby('account__name')['value'].sum()
    return resultado.to_dict()