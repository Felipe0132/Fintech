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

    total = sum_by_value(transactions)

    total_by = df.groupby('category__name')['value'].sum()
    porcentagem = total_by.div(total).mul(100).round(2) # Porcentagem de cada valor referente ao total

    resultado = pd.DataFrame({'valor': total_by, 'porcentagem': porcentagem})
    # Antes tinhamos 2 series separadas, total_by e porcentagem, as duas com as mesmas categorias, agora, juntamos elas e fizemos categoria ter o valor e porcentagens

    return resultado.apply(list, axis=1).to_dict() #Aqui percorreu cada linha e fez virar uma lista os valores, assim ficando categoria:[valor,categoria]

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