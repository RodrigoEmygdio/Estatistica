import math

import numpy as np
import pandas as pd


def cria_tabelaFrequencia(colecao):
    colecao = np.sort(colecao)
    k = round(math.sqrt(colecao.shape[0]))
    At = colecao.max() - colecao.min()
    i = math.ceil(At/k)
    excesso = k * i - At
    intervalo_index = pd.interval_range(start=colecao.min() - math.ceil(excesso * 0.25),end=(excesso -  math.ceil(excesso * 0.25)) + colecao.max() ,freq=9, closed='left' )
    conputacao_valores = []
    for intervalo in intervalo_index.values:
        conputacao_valores.append(colecao[(colecao >= intervalo.left) & (colecao < intervalo.right)].shape[0])
    df = pd.DataFrame(data=conputacao_valores,index=intervalo_index,columns=['Frequencia'])
    return df.append(pd.DataFrame(data=[df['Frequencia'].sum()],index=['Total'],columns=df.columns))