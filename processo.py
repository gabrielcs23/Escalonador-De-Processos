from typing import List
# essa é a classe responsável por cada instância de processo


class Processo(object):
    # atributos da classe
    id = None
    listaIO = []
    tempoChegada = None
    prioridade = None
    tempoProcessador = None
    espacoMemoria = None
    qtdImpressora = None
    qtdScanner = None
    qtdModem = None
    qtdCd = None
    tempoRestante = None
    tempoFinalizacao = None  # indica quando o processo saiu do sistema
    fila = None  # indica qual fila do feedback ele está

    def __init__(self, tempoChegada, prioridade, tempoProcessador, espacoMemoria, qtdImpressora, qtdScanner, qtdModem, qtdCd):
        self.id = id
        self.tempoChegada = tempoChegada
        self.prioridade = prioridade
        self.tempoProcessador = tempoProcessador
        self.espacoMemoria = espacoMemoria
        self.qtdImpressora = qtdImpressora
        self.qtdScanner = qtdScanner
        self.qtdModem = qtdModem
        self.qtdCd = qtdCd
        self.tempoRestante = self.tempoProcessador
        self.fila = 1

    def imprime_processo(self):

        print("Processo " + str(self.id) + "\n")
        print("Tempo de chegada: " + str(self.id) + "\n")
        print("Prioridade " + str(self.id) + "\n")
        print("Tamanho " + str(self.id) + "\n")


# função feita para inserir processo em uma das listas de processos da memória
def insereProcesso(processo: Processo, listaProcesso: List[Processo]):
    for i in range(0, len(listaProcesso)):
        if processo.prioridade < listaProcesso[i].prioridade:
            listaProcesso.insert(i, processo)
            return
        # se for igual ve por ordem em feedback
        if processo.prioridade == listaProcesso[i].prioridade:
            if processo.fila < listaProcesso[i].fila:
                listaProcesso.insert(i, processo)
                return
    listaProcesso.append(processo)
