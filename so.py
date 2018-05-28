from cpu import CPU
from processo import Processo
from gerencia_inout import GerenciaIO
from typing import List
from memoria import Memoria
from escalonador import escalonador_mp_ativa, escalona_lp, escalona_mp_suspende
import escalonadorCurtoPrazo


class SO(object):
    # NÂO TESTEI NADA AINDA, TO FAZENDO VAMOS TESTAR COM A FUNÇÂO PRINCIPAL

    # cria as 4 cpus
    cpus = [CPU() for count in range(4)]
    tempoSistema = 0
    gerenciadorIO = GerenciaIO()
    listaProcessosFinalizados = []

    # ideal chamar desaloca seguido de aloca
    # interrupções, vamos fazer separado? Ou colocar nas funções de aloca desaloca por tempo? Acho melhor criar
    # funções para interromper que consideram que essas existem também

    # função feita para inserir processo em uma das listas de processos da memória
    def insereProcesso(self, processo: Processo, listaProcesso: List[Processo]):
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

    def passagemDeTempo(self):
        for cpu in self.cpus:
            cpu.quantum -= 1
            cpu.processo.tempoProcessador -= 1
        self.gerenciadorIO.atualizaTempoUso()
        self.tempoSistema += 1


def main():
    filaEntrada = inicilizarEntrada('entrada.txt')
    processosNovos = {'tempoReal': [], 'usuario': []}
    processosProntos = []
    processosProntosSuspenso = []
    processosBloqueados = []
    processosBloqueadosSuspenso = []
    processosExecutando = []
    processosFinalizados = []

    so = SO()
    memoria = Memoria()
    gerenciaIO = GerenciaIO()

    while True:
        # Escalonador de longo prazo
        while len(filaEntrada) > 0 and filaEntrada[0].tempoChegada == so.tempoSistema:  # Isso vai dar certo?
            if filaEntrada[0].prioridade == 0:
                processosNovos['tempoReal'].append(filaEntrada.pop(0))
            else:
                processosNovos['usuario'].append(filaEntrada.pop(0))
        escalona_lp(so, gerenciaIO, processosProntos, processosProntosSuspenso, processosNovos, memoria)
        # Escalonador de médio prazo
        # Escalonador de curto prazo
        escalonadorCurtoPrazo.rodadaDeEscalonadorCurto(so, gerenciaIO, processosBloqueados, processosProntos,
                                                       processosExecutando, processosFinalizados, so.cpus)

    # TODO some magic


# arquivo de entrada deve ter cada parametro do processo separado por VIRGULA + ESPAÇO
def inicilizarEntrada(nomeArquivo):
    arquivoEntrada = open(nomeArquivo, 'r')
    filaEntrada = []
    for linha in arquivoEntrada:
        linha.split(', ')
        novoProcesso = Processo(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7])
        filaEntrada.append(novoProcesso)
    arquivoEntrada.close()
    return filaEntrada


main()  # TODO calling magic
