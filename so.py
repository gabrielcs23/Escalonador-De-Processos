from bcolors import BColors
from processo import Processo
from cpu import CPU

class So:


    #NÂO TESTEI NADA AINDA, TO FAZENDO VAMOS TESTAR COM A FUNÇÂO PRINCIPAL

    #cria as 4 cpus
    cpus = [CPU(count) for count in range(4)]
    tempoSistema = 0
    listaProcessosFinalizados=[]

    #ideal chamar desaloca seguido de aloca
    #interrupções, vamos fazer separado? Ou colocar nas funções de aloca desaloca por tempo? Acho melhor criar funções para
    #interromper que consideram que essas existem também

    #função para alocar, caso necessário, o processo da lista de memoria para a cpu
    def alocaProcessosNaCPU(cpus,memoria,listaProcessoPronto,listaProcessoExecutando):
        for i in range(0, len(cpus)):
            if(cpus[i].tempoRestanteProcesso==0):
                if(len(listaProcessoPronto)>0):
                    #insere um processo de prioridade 0, colocando na lista de executando, tirando de pronto e arrumando tempos
                    if(listaProcessoPronto[0].prioridade==0):
                        #coloca processo na cpu e arruma tempos
                        cpus[i].processo=listaProcessoPronto[0]
                        cpus[i].tempoRestanteProcesso= cpus[i].processo.t_processo
                        cpus[i].tempoTotalProcessamento= cpus[i].processo.tempo_restante
                        listaProcessoExecutando.append(cpus[i].processo)
                        listaProcessoPronto.pop(0)
                    #insere um processo de outra prioridade, arrumando tempo de feedback
                    else:
                        cpus[i].processo = listaProcessoPronto[0]
                        cpus[i].tempoRestanteProcesso = pow(2,cpus[i].processo.fila)
                        cpus[i].tempoTotalProcessamento = pow(2,cpus[i].processo.fila)
                        listaProcessoExecutando.addend(cpus[i].processo)
                        listaProcessoPronto.pop(0)

    #função feita para remover processo da cpu
    def desalocaProcessosNaCPU(self,cpus,memoria,listaProcessoPronto,listaProcessoExecutando,tempo):
        for i in range(0, len(cpus)):
            if(cpus[i].tempoRestanteProcesso==0):
                #verifica se o processo terminou ou não, se sim, então removo da lista de executando, da cpu e coloca na lista de finalizados
                if(cpus[i].processo.tempo_restante==0):
                    cpus[i].processo.tempo_finalizacao=self.tempoSistema
                    self.listaProcessosFinalizados.append(cpus[i].processo)
                    listaProcessoExecutando.pop(cpus[i].posicaoLista)
                #senão coloco na lista de prontos e removo da lista de executando
                else:
                    self.insereProcesso(cpus[i].processo,listaProcessoPronto)
                    listaProcessoExecutando.pop(cpus[i].posicaoLista)






    #função feita para inserir processo em uma das listas de processos da memória
    def insereProcesso(processoT,listaProcesso):
        for i in range(0, len(listaProcesso)):
            if processoT.prioridade<listaProcesso[i].prioridade:
                listaProcesso.insert(i,processoT)
                return
            #se for igual ve por ordem em feedback
            if processoT.prioridade==listaProcesso[i].prioridade:
                if processoT.fila<listaProcesso[i].fila:
                    listaProcesso.insert(i, processoT)
                    return
        listaProcesso.insert(i,processoT)

