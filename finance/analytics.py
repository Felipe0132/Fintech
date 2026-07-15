import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .models import *

def sum_by_value(movimentacao):

    movimentacao = movimentacao.values()

    if movimentacao:
        df = pd.DataFrame(movimentacao)

        return df["value"].sum()
    
    return 0.0

def grafico_by_category_gasto(movimentacao, user):
    movimentacao = movimentacao.values('type', 'value') # Data that will use

    if not movimentacao:
        return None

    df = pd.DataFrame(movimentacao)
    df['value'] = df['value'].astype(float)

    por_type = df[['type', 'value']].groupby('type').sum() # Group entries with the same type_id and sum their value

    fig, ax = plt.subplots(figsize=(8, 5))
    pie = ax.pie(por_type['value'])

    ax.pie_label(pie, '{frac:.1%}\n(R${absval:.2f})', textprops=dict(color="w", size=8, weight="bold"))
    ax.legend(pie.wedges, df['type__name'], title="Ingredients", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))



    plt.savefig(f'finance/static/assets/images/graficos/graficoCompareGasto{user.id}.png')
    plt.close(fig)

    return f'assets/images/graficos/graficoCompareGasto{user.id}.png'

def grafico_by_category_ganho(movimentacao, user):
    movimentacao = movimentacao.values('type', 'value') # Data that will use

    if not movimentacao:
        return None

    df = pd.DataFrame(movimentacao)
    df['value'] = df['value'].astype(float)

    por_type = df[['type', 'value']].groupby('type').sum() # Group entries with the same type_id and sum their value

    fig, ax = plt.subplots(figsize=(8, 5))
    pie = ax.pie(por_type['value'])

    ax.pie_label(pie, '{frac:.1%}\n(R${absval:.2f})', textprops=dict(color="w", size=8, weight="bold"))
    ax.legend(pie.wedges, df['type'], title="Ingredients", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))



    plt.savefig(f'finance/static/assets/images/graficos/graficoCompareGanho{user.id}.png')
    plt.close(fig)

    return f'assets/images/graficos/graficoCompareGanho{user.id}.png'

def grafico_by_category_gasto_not_paid(movimentacao, user):
    movimentacao = movimentacao.values('type', 'value') # Data that will use

    if not movimentacao:
        return None

    df = pd.DataFrame(movimentacao)
    df['value'] = df['value'].astype(float)

    por_type = df[['type', 'value']].groupby('type').sum() # Group entries with the same type_id and sum their value

    fig, ax = plt.subplots(figsize=(8, 5))
    pie = ax.pie(por_type['value'])

    ax.pie_label(pie, '{frac:.1%}\n(R${absval:.2f})', textprops=dict(color="w", size=8, weight="bold"))
    ax.legend(pie.wedges, df['type'], title="Ingredients", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))



    plt.savefig(f'finance/static/assets/images/graficos/graficoCompareGastoNotPaid{user.id}.png')
    plt.close(fig)

    return f'assets/images/graficos/graficoCompareGastoNotPaid{user.id}.png'