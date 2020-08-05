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
        self.dataFrame = None
        self.frequenciaCampo = 'Frequencia'
        self.frequenciaRelativaCampo = "Frequencia Relatativa"
        self.frequenciaAcumulada = 'Frequencia Acumulada'
        self.numeroCasasDecimais = 2

    def cria_tabelaFrequencia(self):
        limite_superior = int((self.excesso - round(self.excesso * 0.25)) + self.colecao.max())
        limite_inferior = int(self.colecao.min() - math.ceil(self.excesso * 0.25))
        intervalo_index = pd.interval_range(start=limite_inferior, end=limite_superior, freq=self.intervalo_classes,
                                            closed='right')
        if (intervalo_index.right.max() == self.colecao.max()):
            intervalo_index.right.values[-1] = self.colecao.max() + 1

        conputacao_valores = []
        for intervalo in intervalo_index.values:
            conputacao_valores.append(
                self.colecao[(self.colecao >= intervalo.left) & (self.colecao < intervalo.right)].shape[0])
        self.dataFrame = pd.DataFrame(data=conputacao_valores, index=intervalo_index, columns=[self.frequenciaCampo])
        return self.dataFrame.append(
            pd.DataFrame(data=[self.dataFrame[self.frequenciaCampo].sum()], index=['Total'], columns=self.dataFrame.columns))

    def cria_frequencia_relativa(self):
        if not isinstance(self.dataFrame, pd.DataFrame):
            self.cria_tabelaFrequencia()

        self.dataFrame[self.frequenciaRelativaCampo] = (self.dataFrame[self.frequenciaCampo].values / self.dataFrame[
            self.frequenciaCampo].sum()) * 100
        self.dataFrame[self.frequenciaRelativaCampo] = self.dataFrame[self.frequenciaRelativaCampo].round(self.numeroCasasDecimais)
        return self.dataFrame

    def cria_frequancia_acumulada(self):
        if not isinstance(self.dataFrame, pd.DataFrame):
            self.cria_frequencia_relativa()

        self.dataFrame[self.frequenciaAcumulada] = self.dataFrame[self.frequenciaCampo].cumsum()
        return self.dataFrame
