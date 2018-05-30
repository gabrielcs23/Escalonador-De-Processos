from gerencia_inout import GerenciaIO
from typing import List
from processo import Processo, insereProcesso



# função principal que faz uma rodada de escalonador.
def rodadaDeEscalonadorCurto(tempoSistema, memoria, gIO: GerenciaIO, listaBloqueado: List[Processo], listaPronto: List[Processo],
                             listaExecutando: List[Processo], listaFinalizados: List[Processo], cpus):


    moveBloqueadoParaExecutando(listaBloqueado, listaPronto)
    verificaIO(gIO, listaBloqueado, listaExecutando, cpus)
    desalocaProcessosNaCPU(tempoSistema, memoria, cpus, listaPronto, listaExecutando, listaFinalizados)
    alocaProcessosNaCPU(cpus, listaPronto, listaExecutando)




# função que verifica se io chegou e move de bloqueado para executando
def moveBloqueadoParaExecutando(listaBloqueado: List[Processo], listaPronto: List[Processo]):
    i = 0
    while(i < len(listaBloqueado)):
        estaPronto = True
        #verifica todas as entradas e saida e caso ainda precise processar define estaPronto como false
        for io in listaBloqueado[i].listaIO:
            if io.getTempoRestante() > 0 and io.processoId is not None:
                estaPronto = False
        #estaPronto indica se a io foi toda finalizada então desbloqueia tudo e torna livre e move o processo para pronto
        if estaPronto:
            for io in listaBloqueado[i].listaIO:
                io.livre()
                io.processoBloqueado=False

            listaBloqueado[i].listaIO = []
            insereProcesso(listaBloqueado[i], listaPronto)
            listaBloqueado.pop(i)
            i -= 1
        i += 1


# função para alocar, caso necessário, o processo da lista de memoria para a cpu
def alocaProcessosNaCPU(cpus, listaPronto, listaExecutando):
    i = 0
    while i < len(cpus):
        if cpus[i].quantum == 0 :
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
                        cpus[i].processo.tempoRestante=0
                    '''
                    listaExecutando.append(cpus[i].processo)
                    listaPronto.pop(0)
                    i -= 1
                    '''
                # insere um processo de outra prioridade, arrumando tempo de feedback
                else:
                    cpus[i].processo = listaPronto[0]
                    if (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or
                            cpus[i].processo.qtdModem):
                        cpus[i].quantum = 1
                    else:
                        #coloca tempo de feedback mas se ficar melhor colocamos o tempo como 0
                        if cpus[i].processo.tempoRestante-pow(2, cpus[i].processo.fila)<=0:
                            cpus[i].quantum = cpus[i].processo.tempoRestante
                            cpus[i].processo.tempoRestante=0
                        else:
                            cpus[i].quantum = pow(2, cpus[i].processo.fila)
                            cpus[i].processo.tempoRestante -= pow(2, cpus[i].processo.fila)

                cpus[i].posicaoLista = len(listaExecutando) - 1
                listaExecutando.append(cpus[i].processo)
                listaPronto.pop(0)
                i -= 1
        i += 1


# função interrompe com so
def verificaIO(gIO: GerenciaIO, listaBloqueado, listaExecutando, cpus):
    i = 0
    while i < len(cpus):
        if (cpus[i].processo is not None and (cpus[i].processo.qtdImpressora or cpus[i].processo.qtdCd or cpus[i].processo.qtdScanner or
                cpus[i].processo.qtdModem)):
            if cpus[i].quantum == 0 and cpus[i].processo is not None:
                insereProcesso(cpus[i].processo, listaBloqueado)
                listaExecutando.pop(cpus[i].posicaoLista)
                atualizaPosicaoCPUS(cpus,cpus[i].posicaoLista)

                # verifica quais io precisa e aloca
                if cpus[i].processo.qtdImpressora > 0 and (not gIO.impressora_1.processoBloqueado or not gIO.impressora_2.processoBloqueado):
                    if cpus[i].processo.qtdImpressora==1:
                        if(gIO.impressora_1.processoId==cpus[i].processo.id and gIO.impressora_1.processoBloqueado):
                            gIO.impressora_2.ocupado(cpus[i].processo.id)
                            gIO.impressora_2.processoBloqueado = True
                            cpus[i].processo.listaIO.append(gIO.impressora_2)
                            cpus[i].processo.qtdImpressora -= 1
                        elif (not gIO.impressora_2.processoBloqueado):
                            gIO.impressora_1.ocupado(cpus[i].processo.id)
                            gIO.impressora_1.processoBloqueado=True
                            cpus[i].processo.listaIO.append(gIO.impressora_1)
                            cpus[i].processo.qtdImpressora-=1

                    if (not gIO.impressora_1.processoBloqueado and not gIO.impressora_2.processoBloqueado) and cpus[i].processo.qtdImpressora==2:
                        gIO.impressora_1.ocupado(cpus[i].processo.id)
                        gIO.impressora_1.processoBloqueado=True
                        gIO.impressora_2.ocupado(cpus[i].processo.id)
                        gIO.impressora_2.processoBloqueado=True
                        cpus[i].processo.qtdImpressora-=2
                        cpus[i].processo.listaIO.append(gIO.impressora_1)
                        cpus[i].processo.listaIO.append(gIO.impressora_2)
                if cpus[i].processo.qtdCd > 0 and (not gIO.cd_1.processoBloqueado or not gIO.cd_2.processoBloqueado):
                    if cpus[i].processo.qtdCd==1:
                        if (gIO.cd_1.processoId==cpus[i].processo.id and gIO.cd_1.processoBloqueado):
                            gIO.cd_2.ocupado(cpus[i].processo.id)
                            gIO.cd_2.processoBloqueado = True
                            cpus[i].processo.qtdCd -= 1
                            cpus[i].processo.listaIO.append(gIO.cd_2)
                        elif(not gIO.cd_2.processoBloqueado):
                            gIO.cd_1.ocupado(cpus[i].processo.id)
                            gIO.cd_1.processoBloqueado=True
                            cpus[i].processo.qtdCd-=1
                            cpus[i].processo.listaIO.append(gIO.cd_1)
                    if (not gIO.cd_1.processoBloqueado and not gIO.cd_2.processoBloqueado) and cpus[i].processo.qtdCd==2:
                        gIO.cd_1.ocupado(cpus[i].processo.id)
                        gIO.cd_1.processoBloqueado=True
                        gIO.cd_2.ocupado(cpus[i].processo.id)
                        gIO.cd_2.processoBloqueado=True
                        cpus[i].processo.qtdCd-=2
                        cpus[i].processo.listaIO.append(gIO.cd_1)
                        cpus[i].processo.listaIO.append(gIO.cd_2)

                if cpus[i].processo.qtdScanner > 0 and not gIO.scanner.processoBloqueado:
                    gIO.scanner.ocupado(cpus[i].processo.id)
                    gIO.scanner.processoBloqueado=True
                    cpus[i].processo.qtdScanner-=1
                    cpus[i].processo.listaIO.append(gIO.scanner)
                if cpus[i].processo.qtdModem > 0 and not gIO.modem.processoBloqueado:
                    gIO.modem.ocupado(cpus[i].processo.id)
                    gIO.modem.processoBloqueado=True
                    cpus[i].processo.qtdModem-=1
                    cpus[i].processo.listaIO.append(gIO.modem)
                cpus[i].processo = None
                cpus[i].quantum=0
        i += 1


# função feita para remover processo da cpu
def desalocaProcessosNaCPU(tempoSistema, memoria, cpus, listaPronto: List[Processo], listaExecutando, listaFinalizados):
    i = 0
    while i < len(cpus):
        if cpus[i].quantum == 0 and cpus[i].processo is not None:
            # verifica se o processo terminou ou não
            # se sim, então removo da lista de executando, da cpu e coloca na lista de finalizados
            if cpus[i].processo.tempoRestante == 0:
                cpus[i].processo.tempoFinalizacao = tempoSistema
                listaFinalizados.append(cpus[i].processo)
                listaExecutando.pop(cpus[i].posicaoLista)
                atualizaPosicaoCPUS(cpus,cpus[i].posicaoLista)
                memoria.m_livre+=cpus[i].processo.espacoMemoria
                cpus[i].processo=None
                cpus[i].quantum=0
            # senão coloco na lista de prontos e removo da lista de executando
            else:
                if cpus[i].processo.fila == 3:
                    cpus[i].processo.fila = 1
                else:
                    cpus[i].processo.fila += 1
                insereProcesso(cpus[i].processo, listaPronto)
                listaExecutando.pop(cpus[i].posicaoLista)
                atualizaPosicaoCPUS(cpus,cpus[i].posicaoLista)
                cpus[i].processo=None
                cpus[i].quantum=0
        #verifica os processos de feedback
        if cpus[i].processo is not None:
            if cpus[i].processo.fila>=1 and cpus[i].processo.tempoRestante<=0 and cpus[i].quantum == 0:
                cpus[i].processo.tempoFinalizacao = tempoSistema
                listaFinalizados.append(cpus[i].processo)
                listaExecutando.pop(cpus[i].posicaoLista)
                atualizaPosicaoCPUS(cpus, cpus[i].posicaoLista)
                memoria.m_livre += cpus[i].processo.espacoMemoria
                cpus[i].processo = None
                cpus[i].quantum=0
        i += 1

#função para diminuir a posição na lista de executando após tirar um valor de lá
def atualizaPosicaoCPUS(cpus,i):
    for c in cpus:
        if c.posicaoLista is not None and c.posicaoLista >= i:
            c.posicaoLista-=1