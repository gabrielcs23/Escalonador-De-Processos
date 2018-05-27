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

    # função para alocar, caso necessário, o processo da lista de memoria para a cpu
    def alocaProcessosNaCPU(self, cpus, listaProcessoPronto, listaProcessoExecutando):
        for i in range(0, len(cpus)):
            if cpus[i].tempoRestanteProcesso == 0:
                if len(listaProcessoPronto) > 0:
                    # insere um processo de prioridade 0, colocando na lista de executando, tirando de pronto e arrumando tempos
                    if listaProcessoPronto[0].prioridade == 0:
                        # coloca processo na cpu e arruma tempos
                        cpus[i].processo = listaProcessoPronto[0]
                        if(cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or cpus[i].processo.qtdModem):
                            cpus[i].tempoRestanteProcesso = 1
                        else:
                            cpus[i].tempoRestanteProcesso = cpus[i].processo.t_processo
                        listaProcessoExecutando.append(cpus[i].processo)
                        listaProcessoPronto.pop(0)
                    # insere um processo de outra prioridade, arrumando tempo de feedback
                    else:
                        cpus[i].processo = listaProcessoPronto[0]
                        if (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or
                                cpus[i].processo.qtdModem):
                            cpus[i].tempoRestanteProcesso = 1
                        else:
                            cpus[i].tempoRestanteProcesso = pow(2, cpus[i].processo.fila)
                        listaProcessoExecutando.addend(cpus[i].processo)
                        listaProcessoPronto.pop(0)

    def verificaIO(self,listaBloqueado,listaExecutando,cpus):
        for i in range(0, len(cpus)):
            if (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or cpus[i].processo.qtdModem):
                if cpus[i].quantum == 0:
                    self.insereProcesso(cpus[i].processo,listaBloqueado)
                    listaExecutando.pop(cpus[i].posicaoLista)


    # função feita para remover processo da cpu
    def desalocaProcessosNaCPU(self, cpus, listaProcessoPronto, listaProcessoExecutando):
        for i in range(0, len(cpus)):
            if cpus[i].tempoRestanteProcesso == 0:
                # verifica se o processo terminou ou não, se sim, então removo da lista de executando, da cpu e coloca na lista de finalizados
                if (cpus[i].processo.tempo_restante == 0):
                    cpus[i].processo.tempo_finalizacao = self.tempoSistema
                    self.listaProcessosFinalizados.append(cpus[i].processo)
                    listaProcessoExecutando.pop(cpus[i].posicaoLista)
                # senão coloco na lista de prontos e removo da lista de executando
                else:
                    self.insereProcesso(cpus[i].processo, listaProcessoPronto)
                    if (cpus[i].processo.fila == 3):
                        cpus[i].processo.fila = 1
                    else:
                        cpus[i].processo.fila += 1
                    listaProcessoExecutando.pop(cpus[i].posicaoLista)

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