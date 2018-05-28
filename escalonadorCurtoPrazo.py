from gerencia_inout import GerenciaIO
from typing import List
from processo import Processo, insereProcesso


# função principal que faz uma rodada de escalonador.
def rodadaDeEscalonadorCurto(tempoSistema, gIO: GerenciaIO, listaBloqueado: List[Processo], listaPronto: List[Processo],
                             listaExecutando: List[Processo], listaFinalizados: List[Processo], cpus):
    moveBloqueadoParaExecutando(listaBloqueado, listaPronto)
    alocaProcessosNaCPU(cpus, listaPronto, listaExecutando)
    verificaIO(gIO, listaBloqueado, listaExecutando, cpus)
    desalocaProcessosNaCPU(tempoSistema, cpus, listaPronto, listaExecutando, listaFinalizados)


# função que verifica se io chegou e move de bloqueado para executando
def moveBloqueadoParaExecutando(listaBloqueado: List[Processo], listaPronto: List[Processo]):
    for i in range(0, len(listaBloqueado)):
        estaPronto = True
        for io in listaBloqueado[i].listaIO:
            if io.getTempoRestante() > 0:
                estaPronto = False
        if estaPronto:
            for io in listaBloqueado[i].listaIO:
                io.livre()

            listaBloqueado[i].listaIO = []
            insereProcesso(listaBloqueado[i], listaPronto)
            listaBloqueado.pop(i)


# função para alocar, caso necessário, o processo da lista de memoria para a cpu
def alocaProcessosNaCPU(cpus, listaPronto, listaExecutando):
    for i in range(0, len(cpus)):
        if cpus[i].quantum == 0 and cpus[i].processo is not None:
            if len(listaPronto) > 0:
                # insere um processo de prioridade 0, colocando na lista de executando,
                # tirando de pronto e arrumando tempos
                if listaPronto[0].prioridade == 0:
                    # coloca processo na cpu e arruma tempos
                    cpus[i].processo = listaPronto[0]
                    if (cpus[i].processo.qtdImpressora + cpus[i].processo.qtdCd + cpus[i].processo.qtdScanner +
                        cpus[i].processo.qtdModem) > 0:
                        cpus[i].quantum = 1
                    else:
                        cpus[i].quantum = cpus[i].processo.tempoRestante
                    listaExecutando.append(cpus[i].processo)
                    listaPronto.pop(0)
                # insere um processo de outra prioridade, arrumando tempo de feedback
                else:
                    cpus[i].processo = listaPronto[0]
                    if (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or
                            cpus[i].processo.qtdModem):
                        cpus[i].quantum = 1
                    else:
                        cpus[i].quantum = pow(2, cpus[i].processo.fila)
                    listaExecutando.append(cpus[i].processo)
                    listaPronto.pop(0)


# função interrompe com so
def verificaIO(gIO: GerenciaIO, listaBloqueado, listaExecutando, cpus):
    for i in range(0, len(cpus)):
        if (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or
                cpus[i].processo.qtdModem):
            if cpus[i].quantum == 0 and cpus[i].processo is not None:
                insereProcesso(cpus[i].processo, listaBloqueado)
                listaExecutando.pop(cpus[i].posicaoLista)

                # verifica quais io precisa e aloca
                if cpus[i].processo.qtdImpressora > 0 and \
                        gIO.qtdImpressoraDisponivel() == listaBloqueado[i].qtdImpressora:
                    if gIO.qtdImpressoraDisponivel() == 1:
                        gIO.impressora_1.ocupado(cpus[i].processo.id)
                        cpus[i].processo.listaIO.append(gIO.impressora_1)
                    if gIO.qtdImpressoraDisponivel() == 2:
                        gIO.impressora_1.ocupado(cpus[i].processo.id)
                        gIO.impressora_2.ocupado(cpus[i].processo.id)
                        cpus[i].processo.listaIO.append(gIO.impressora_1)
                        cpus[i].processo.listaIO.append(gIO.impressora_2)
                if cpus[i].processo.qtdCd > 0 and gIO.qtdCdDisponivel() == cpus[i].processo.qtdCd:
                    if gIO.qtdCdDisponivel() == 1:
                        gIO.cd_1.ocupado(cpus[i].processo.id)
                        cpus[i].processo.listaIO.append(gIO.cd_1)
                    if gIO.qtdCdDisponivel() == 2:
                        gIO.cd_1.ocupado(cpus[i].processo.id)
                        gIO.cd_2.ocupado(cpus[i].processo.id)
                        cpus[i].processo.listaIO.append(gIO.cd_1)
                        cpus[i].processo.listaIO.append(gIO.cd_2)
                if cpus[i].processo.qtdScanner > 0 and gIO.isScannerDisponivel():
                    gIO.scanner.ocupado(cpus[i].processo.id)
                    cpus[i].processo.listaIO.append(gIO.scanner)
                if cpus[i].processo.qtdModem > 0 and gIO.isModemDisponivel():
                    gIO.modem.ocupado(cpus[i].processo.id)
                    cpus[i].processo.listaIO.append(gIO.modem)
                cpus[i].processo = None


# função feita para remover processo da cpu
def desalocaProcessosNaCPU(tempoSistema, cpus, listaPronto: List[Processo], listaExecutando, listaFinalizados):
    for i in range(0, len(cpus)):
        if cpus[i].quantum == 0 and cpus[i].processo is not None:
            # verifica se o processo terminou ou não
            # se sim, então removo da lista de executando, da cpu e coloca na lista de finalizados
            if cpus[i].processo.tempoRestante == 0:
                cpus[i].processo.tempoFinalizacao = tempoSistema
                listaFinalizados.append(cpus[i].processo)
                listaExecutando.pop(cpus[i].posicaoLista)
            # senão coloco na lista de prontos e removo da lista de executando
            else:
                insereProcesso(cpus[i].processo, listaPronto)
                if cpus[i].processo.fila == 3:
                    cpus[i].processo.fila = 1
                else:
                    cpus[i].processo.fila += 1
                listaExecutando.pop(cpus[i].posicaoLista)
