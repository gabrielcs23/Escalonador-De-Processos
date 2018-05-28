from gerencia_inout import GerenciaIO
from processo import Processo, insereProcesso
from typing import List, Dict


# escalonador a longo prazo
def escalona_lp(GerIO: GerenciaIO, fila_processos_prontos: List[Processo],
                fila_processos_prontos_suspensos: List[Processo], lista_novos: Dict,
                memoria):
    # enquanto a lista de processos novos de tempo real estiver com elementos, faça...
    while len(lista_novos['tempoReal']) > 0:
        # se houver memoria livre pra colocar o proximo processo da lista de novos processos
        if memoria.m_livre > lista_novos['tempoReal'][0].espacoMemoria:
            # coloca o processo e retira este processo da lista de novos processos
            insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos_suspensos)
            memoria.m_livre -= lista_novos['tempoReal'][0].espacoMemoria
            lista_novos['tempoReal'].pop(0)
        else:
            # coloca o processo na lista de prontos suspensos
            insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos_suspensos)
            lista_novos['tempoReal'].pop(0)
    # mesma ideia do while anterior, mas para lista de usuario
    while len(lista_novos['usuario']) > 0:
        if memoria.m_livre > lista_novos['usuario'][0].espacoMemoria:
            # se o processo possui todos os recursos disponiveis, vai pra fila de pronto
            if lista_novos['usuario'].qtdImpressora <= GerIO.qtdImpressoraDisponivel() and lista_novos[
                'usuario'].qtdCd <= GerIO.qtdCdDisponivel() and (
                    not lista_novos['usuario'].qtdScanner or GerIO.isScannerDisponivel()) and (
                    not lista_novos['usuario'].qtdModem or GerIO.isModemDisponivel()):
                insereProcesso(lista_novos['usuario'][0], fila_processos_prontos)
                memoria.m_livre -= lista_novos['usuario'][0].espacoMemoria
                lista_novos['usuario'].pop(0)
        else:
            insereProcesso(lista_novos['usuario'][0], fila_processos_prontos_suspensos)
            lista_novos['usuario'].pop(0)


# escalonador a medio prazo, parte que remove da memoria principal
# esta funcao libera memoria até ter no minimo uma quantidade (qtd_memoria) livre
def escalona_mp_suspende(qtd_memoria, processosBloqueados: List[Processo],
                         processosBloqueadosSuspensos: List[Processo], processosProntos: List[Processo],
                         processosProntosSuspensos: List[Processo], memoria):
    # retira o processo mais recente com prioridade 3 da fila de bloqueado,
    # caso nao exista retira o processo mais recente com prioridade 3 da fila de prontos

    # repete os passos acima com prioridade 2, 1, e 0, nesta ordem
    prioridade = 3
    # enquanto nao houver (qtd_memoria) memoria disponivel e prioridade for maior ou igual a 0...
    while memoria.m_livre < qtd_memoria and prioridade >= 0:
        # range começa em tamanho da fila -1 (ultimo elemento), vai até 0 (-1 nao incluso) e em passos de -1
        for i in range(len(processosBloqueados) - 1, -1, -1):
            # como a analise é feita do final até o começo da fila, a fila começa com a prioridade 3 e desce até 0
            # caso a prioridade seja inferior da analisada, break
            # caso seja maior, continue
            if processosBloqueados[i].prioridade > prioridade:
                continue
            elif processosBloqueados[i].prioridade < prioridade:
                break
            # caso contrário, estamos na região com prioridade igual a prioridade analisada
            else:
                # insere na fila de bloqueado suspenso, remove da fila de bloqueados,
                # atualiza memoria livre, diminui i para analisar o indice correto da proxima vez
                insereProcesso(processosBloqueados[i], processosBloqueadosSuspensos)
                memoria.m_livre += processosBloqueados[i].espacoMemoria
                processosBloqueados.pop(i)
                i -= 1
                # caso ja tenha memoria o suficiente, break
                if memoria.m_livre > qtd_memoria:
                    return
        # mesma analise anterior, porem para a lista de prontos/prontos suspensos
        for i in range(len(processosProntos) - 1, -1, -1):
            if processosProntos[i].prioridade > prioridade:
                continue
            elif processosProntos[i].prioridade < prioridade:
                break
            else:
                insereProcesso(processosProntos[i], processosProntosSuspensos)
                memoria.m_livre += processosProntos[i].espacoMemoria
                processosProntos.pop(i)
                i -= 1
                if memoria.m_livre > qtd_memoria:
                    return
        # diminui prioridade em 1 para analisar a próxima prioridade
        prioridade -= 1


# insere processos na memoria principal ate a memoria estar cheia ou ate nao ter mais processos que caibam na memoria
def escalonador_mp_ativa(GerIO: GerenciaIO, processosBloqueados: List[Processo],
                         processosBloqueadosSuspensos: List[Processo], processosProntos: List[Processo],
                         processosProntosSuspensos: List[Processo], memoria):
    # a partir de prioridade 0, insere processos na memoria principal ate a memoria estar cheia
    prioridade = 0
    while prioridade <= 3:
        # verifica cada processo a partir do indice 0
        for i in range(len(processosProntosSuspensos)):
            # como a analise é feita do inicio até o final da fila, a fila começa com a prioridade 0 e sobe até 3
            # caso a prioridade seja inferior da analisada, continue
            # caso seja maior, break
            if processosProntosSuspensos[i].prioridade < prioridade:
                continue
            elif processosProntosSuspensos[i].prioridade > prioridade:
                break
            else:
                # se houver espaço na memoria
                if memoria.m_livre - processosProntosSuspensos[i] > 0\
                        and processosProntosSuspensos[i].qtdImpressora <= GerIO.qtdImpressoraDisponivel()\
                        and processosProntosSuspensos[i].qtdCd <= GerIO.qtdCdDisponivel()\
                        and (not processosProntosSuspensos[i].qtdScanner or GerIO.isScannerDisponivel())\
                        and (not processosProntosSuspensos[i].qtdModem or GerIO.isModemDisponivel()):
                    # insere na fila de processos prontos, remove da lista de prontos suspenso e atualiza memoria
                    insereProcesso(processosProntosSuspensos[i], processosProntos)
                    memoria.m_livre -= processosProntosSuspensos[i].espacoMemoria
                    processosProntosSuspensos.pop(i)
                    # se nao houver mais memoria, return
                    if memoria.m_livre == 0:
                        return
        # mesma ideia do for anterior, mas para a fila de bloqueados suspenso
        for i in range(len(processosBloqueadosSuspensos)):
            if processosBloqueadosSuspensos[i].prioridade < prioridade:
                continue
            elif processosBloqueadosSuspensos[i].prioridade > prioridade:
                break
            else:
                if memoria.m_livre - processosBloqueadosSuspensos[i] > 0:
                    insereProcesso(processosBloqueadosSuspensos[i], processosBloqueados)
                    memoria.m_livre -= processosBloqueadosSuspensos[i].espacoMemoria
                    processosBloqueadosSuspensos.pop(i)
                    if memoria.m_livre == 0:
                        return
        prioridade += 1
