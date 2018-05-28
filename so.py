from cpu import CPU
from processo import Processo


class SO:
    # NÂO TESTEI NADA AINDA, TO FAZENDO VAMOS TESTAR COM A FUNÇÂO PRINCIPAL

    # cria as 4 cpus
    cpus = [CPU() for count in range(4)]
    tempoSistema = 0
    listaProcessosFinalizados = []

    # ideal chamar desaloca seguido de aloca
    # interrupções, vamos fazer separado? Ou colocar nas funções de aloca desaloca por tempo? Acho melhor criar
    # funções para interromper que consideram que essas existem também


    # função feita para inserir processo em uma das listas de processos da memória
    def insereProcesso(self, processoT, listaProcesso):
        for i in range(0, len(listaProcesso)):
            if processoT.prioridade < listaProcesso[i].prioridade:
                listaProcesso.insert(i, processoT)
                return
            # se for igual ve por ordem em feedback
            if processoT.prioridade == listaProcesso[i].prioridade:
                if processoT.fila < listaProcesso[i].fila:
                    listaProcesso.insert(i, processoT)
                    return
        listaProcesso.append(processoT)

def main():
    filaEntrada = inicilizarEntrada('entrada.txt')
    processosNovos = {'tempoReal': [], 'usuario': []}
    processosProntos = []
    processosProntosSuspenso = []
    processosBloqueados = []
    processosBloqueadosSuspenso = []
    processosExecutando = []
    processosFinalizados = []
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