import math

import numpy as np
import pandas as pd


class TabelaFrequncia:
    def __init__(self, dados: np.array):
        self.colecao = np.sort(dados)
        self.numero_classes = round(math.sqrt(self.colecao.shape[0]))
        self.At = self.colecao.max() - self.colecao.min()
        self.intervalo_classes = math.ceil(self.At / self.numero_classes)
        self.excesso = self.numero_classes * self.intervalo_classes - self.At
        self.df = None
        self.frequenciaCampo = 'Frequencia'
        self.frequenciaRelativaCampo = "Frequencia Relatativa"
        self.numeroCasasDecimais = 2

    def cria_tabelaFrequencia(self):
        limite_superior = int((self.excesso - round(self.excesso * 0.25)) + self.colecao.max())
        limite_inferior = int(self.colecao.min() - math.ceil(self.excesso * 0.25))
        intervalo_index = pd.interval_range(start=limite_inferior, end=limite_superior, freq=self.intervalo_classes,
                                            closed='left')
        conputacao_valores = []
        for intervalo in intervalo_index.values:
            conputacao_valores.append(
                self.colecao[(self.colecao >= intervalo.left) & (self.colecao < intervalo.right)].shape[0])
        self.df = pd.DataFrame(data=conputacao_valores, index=intervalo_index, columns=[self.frequenciaCampo])
        return self.df.append(
            pd.DataFrame(data=[self.df[self.frequenciaCampo].sum()], index=['Total'], columns=self.df.columns))

    def cria_frequencia_relativa(self):
        if not isinstance(self.df, pd.DataFrame):
            self.cria_tabelaFrequencia()

        self.df[self.frequenciaRelativaCampo] = (self.df[self.frequenciaCampo].values / self.df[self.frequenciaCampo].sum()) * 100
        self.df[self.frequenciaRelativaCampo] =  self.df[self.frequenciaRelativaCampo].round(self.numeroCasasDecimais)
        return self.df

