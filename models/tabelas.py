import math

import numpy as np
import pandas as pd


class TabelFrequncia:
    def __init__(self, dados: np.array):
        self.colecao = np.sort(dados)
        self.numero_classes = round(math.sqrt(self.colecao.shape[0]))
        self.At = self.colecao.max() - self.colecao.min()
        self.intervalo_classes = math.ceil(self.At / self.numero_classes)
        self.excesso = self.numero_classes * self.intervalo_classes - self.At

    def cria_tabelaFrequencia(self):
        limite_superior = int((self.excesso - round(self.excesso * 0.25)) + self.colecao.max())
        limite_inferior = int(self.colecao.min() - math.ceil(self.excesso * 0.25))
        intervalo_index = pd.interval_range(start=limite_inferior, end=limite_superior, freq=self.intervalo_classes, closed='left')
        conputacao_valores = []
        for intervalo in intervalo_index.values:
            conputacao_valores.append(
                self.colecao[(self.colecao >= intervalo.left) & (self.colecao < intervalo.right)].shape[0])
        df = pd.DataFrame(data=conputacao_valores, index=intervalo_index, columns=['Frequencia'])
        return df.append(pd.DataFrame(data=[df['Frequencia'].sum()], index=['Total'], columns=df.columns))
