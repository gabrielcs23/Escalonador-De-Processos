from gerencia_inout import GerenciaIO
from processo import Processo, insereProcesso
from typing import List, Dict


# escalonador a longo prazo
def escalona_lp(ger_io: GerenciaIO, fila_processos_prontos: List[Processo],
                fila_processos_prontos_suspensos: List[Processo], fila_processos_bloqueados: List[Processo],
                fila_processos_bloqueados_suspensos: List[Processo], lista_novos: Dict, memoria):
    # enquanto a lista de processos novos de tempo real estiver com elementos, faça...
    iterador = 0
    while len(lista_novos['tempoReal']) > 0:
        # se houver memoria livre pra colocar o proximo processo da lista de novos processos
        if memoria.m_livre >= lista_novos['tempoReal'][iterador].espacoMemoria:
            # coloca o processo e retira este processo da lista de novos processos
            insereProcesso(lista_novos['tempoReal'][iterador], fila_processos_prontos)
            memoria.m_livre -= lista_novos['tempoReal'][iterador].espacoMemoria
        else:
            # tenta liberar espaço para inserir processo
            # libera os processos de prioridade maior (>0)
            # se conseguir, insere na lista de prontos
            # caso contrario, insere na lista de prontos suspensos
            escalona_mp_suspende(lista_novos['tempoReal'][iterador].espacoMemoria,
                                 fila_processos_prontos, fila_processos_prontos_suspensos,
                                 fila_processos_bloqueados, fila_processos_bloqueados_suspensos,
                                 lista_novos['tempoReal'][iterador].prioridade, memoria)
            if memoria.m_livre >= lista_novos['tempoReal'][iterador].espacoMemoria:
                insereProcesso(lista_novos['tempoReal'][iterador], fila_processos_prontos)
                memoria.m_livre -= lista_novos['tempoReal'][iterador].espacoMemoria
            else:
                insereProcesso(lista_novos['tempoReal'][iterador], fila_processos_prontos_suspensos)
        lista_novos['tempoReal'].pop(iterador)
    # mesma ideia do while anterior, mas para lista de usuario
    while iterador < len(lista_novos['usuario']):
        # se o processo possui todos os recursos disponiveis, checa memoria
        impressoras = ger_io.qtdImpressoraDisponivel()
        for i in fila_processos_prontos:
            impressoras -= i.qtdImpressora
        cds = ger_io.qtdCdDisponivel()
        for i in fila_processos_prontos:
            cds -= i.qtdCd
        scanner = ger_io.isScannerDisponivel()
        for i in fila_processos_prontos:
            if i.qtdScanner == 1:
                scanner = scanner and False
            else:
                scanner = scanner and True
        modem = ger_io.isModemDisponivel()
        for i in fila_processos_prontos:
            if i.qtdModem == 1:
                modem = modem and False
            else:
                modem = modem and True
        if lista_novos['usuario'][iterador].qtdImpressora <= impressoras and lista_novos[
            'usuario'][iterador].qtdCd <= cds and (
                not lista_novos['usuario'][iterador].qtdScanner or scanner) and (
                not lista_novos['usuario'][iterador].qtdModem or modem):
            # se tem memoria, insere na lista de pronto
            if memoria.m_livre >= lista_novos['usuario'][iterador].espacoMemoria:
                insereProcesso(lista_novos['usuario'][iterador], fila_processos_prontos)
                memoria.m_livre -= lista_novos['usuario'][iterador].espacoMemoria
                ger_io.alocaCd(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdCd)
                ger_io.alocaImpressora(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdImpressora)
                ger_io.alocaScanner(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdScanner)
                ger_io.alocaModem(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdModem)
                lista_novos['usuario'].pop(iterador)
                iterador -= 1
            else:
                # caso contrario, tenta liberar memoria
                escalona_mp_suspende(lista_novos['usuario'][iterador].espacoMemoria,
                                     fila_processos_prontos, fila_processos_prontos_suspensos,
                                     fila_processos_bloqueados, fila_processos_bloqueados_suspensos,
                                     lista_novos['usuario'][iterador].prioridade, memoria)
                # se conseguiu liberar memoria, insere na lista de pronto
                if memoria.m_livre >= lista_novos['usuario'][iterador].espacoMemoria:
                    insereProcesso(lista_novos['usuario'][iterador], fila_processos_prontos)
                    memoria.m_livre -= lista_novos['usuario'][iterador].espacoMemoria
                    ger_io.alocaCd(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdCd)
                    ger_io.alocaImpressora(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdImpressora)
                    ger_io.alocaScanner(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdScanner)
                    ger_io.alocaModem(lista_novos['usuario'][iterador].id, lista_novos['usuario'][iterador].qtdModem)
                    lista_novos['usuario'].pop(iterador)
                    iterador -= 1
        iterador += 1


# escalonador a medio prazo, parte que remove da memoria principal
# esta funcao libera memoria até ter no minimo uma quantidade (qtd_memoria) livre
def escalona_mp_suspende(qtd_memoria,  fila_processos_prontos: List[Processo],
                         fila_processos_prontos_suspensos: List[Processo], fila_processos_bloqueados: List[Processo],
                         fila_processos_bloqueados_suspensos: List[Processo], prioridade_min: int, memoria):
    # retira o processo mais recente com prioridade 3 da fila de bloqueado,
    # caso nao exista retira o processo mais recente com prioridade 3 da fila de prontos

    # repete os passos acima com prioridade 2, 1, e 0, nesta ordem
    prioridade = 3
    # enquanto nao houver (qtd_memoria) memoria disponivel e prioridade for maior ou igual a 0...
    while memoria.m_livre < qtd_memoria and prioridade > prioridade_min:
        # range começa em tamanho da fila -1 (ultimo elemento), vai até 0 (-1 nao incluso) e em passos de -1
        for i in range(len(fila_processos_bloqueados) - 1, -1, -1):
            # como a analise é feita do final até o começo da fila, a fila começa com a prioridade 3 e desce até 0
            # caso a prioridade seja inferior da analisada, break
            # caso seja maior, continue
            # faço essa checagem para que se analise apenas a prioriade da vez
            if fila_processos_bloqueados[i].prioridade > prioridade:
                continue
            elif fila_processos_bloqueados[i].prioridade < prioridade:
                break
            # caso contrário, estamos na região com prioridade igual a prioridade analisada
            else:
                # insere na fila de bloqueado suspenso, remove da fila de bloqueados,
                # atualiza memoria livre, diminui i para analisar o indice correto da proxima vez
                insereProcesso(fila_processos_bloqueados[i], fila_processos_bloqueados_suspensos)
                memoria.m_livre += fila_processos_bloqueados[i].espacoMemoria
                fila_processos_bloqueados.pop(i)
                # caso ja tenha memoria o suficiente, break
                if memoria.m_livre > qtd_memoria:
                    return
        # mesma analise anterior, porem para a lista de prontos/prontos suspensos
        for i in range(len(fila_processos_prontos) - 1, -1, -1):
            if fila_processos_prontos[i].prioridade > prioridade:
                continue
            elif fila_processos_prontos[i].prioridade < prioridade:
                break
            else:
                insereProcesso(fila_processos_prontos[i], fila_processos_prontos_suspensos)
                memoria.m_livre += fila_processos_prontos[i].espacoMemoria
                fila_processos_prontos.pop(i)
                if memoria.m_livre > qtd_memoria:
                    return
        # diminui prioridade em 1 para analisar a próxima prioridade
        prioridade -= 1


# insere processos na memoria principal ate a memoria estar cheia ou ate nao ter mais processos que caibam na memoria
def escalonador_mp_ativa(ger_io: GerenciaIO, fila_processos_prontos: List[Processo],
                         fila_processos_prontos_suspensos: List[Processo], fila_processos_bloqueados: List[Processo],
                         fila_processos_bloqueados_suspensos: List[Processo], memoria):
    # a partir de prioridade 0, insere processos na memoria principal ate a memoria estar cheia
    prioridade = 0
    while prioridade <= 3:
        # verifica cada processo a partir do indice 0
        for i in range(len(fila_processos_prontos_suspensos)):
            # como a analise é feita do inicio até o final da fila, a fila começa com a prioridade 0 e sobe até 3
            # caso a prioridade seja inferior da analisada, continue
            # caso seja maior, break
            if fila_processos_prontos_suspensos[i].prioridade < prioridade:
                continue
            elif fila_processos_prontos_suspensos[i].prioridade > prioridade:
                break
            else:
                # se houver espaço na memoria
                impressoras = ger_io.qtdImpressoraDisponivel()
                for j in fila_processos_prontos:
                    impressoras -= j.qtdImpressora
                cds = ger_io.qtdCdDisponivel()
                for j in fila_processos_prontos:
                    cds -= j.qtdCd
                scanner = ger_io.isScannerDisponivel()
                for j in fila_processos_prontos:
                    if j.qtdScanner == 1:
                        scanner = scanner and False
                    else:
                        scanner = scanner and True
                modem = ger_io.isModemDisponivel()
                for j in fila_processos_prontos:
                    if j.qtdModem == 1:
                        modem = modem and False
                    else:
                        modem = modem and True
                if memoria.m_livre - fila_processos_prontos_suspensos[i].espacoMemoria > 0\
                        and fila_processos_prontos_suspensos[i].qtdImpressora <= impressoras\
                        and fila_processos_prontos_suspensos[i].qtdCd <= cds\
                        and (not fila_processos_prontos_suspensos[i].qtdScanner or scanner)\
                        and (not fila_processos_prontos_suspensos[i].qtdModem or modem):
                    # insere na fila de processos prontos, remove da lista de prontos suspenso e atualiza memoria
                    insereProcesso(fila_processos_prontos_suspensos[i], fila_processos_prontos)
                    memoria.m_livre -= fila_processos_prontos_suspensos[i].espacoMemoria
                    fila_processos_prontos_suspensos.pop(i)
                    prioridade -= 1
                    # se nao houver mais memoria, return
                    if memoria.m_livre == 0:
                        return
                    break
        # mesma ideia do for anterior, mas para a fila de bloqueados suspenso
        for i in range(len(fila_processos_bloqueados_suspensos)):
            if fila_processos_bloqueados_suspensos[i].prioridade < prioridade:
                continue
            elif fila_processos_bloqueados_suspensos[i].prioridade > prioridade:
                break
            else:
                if memoria.m_livre - fila_processos_bloqueados_suspensos[i] > 0:
                    insereProcesso(fila_processos_bloqueados_suspensos[i], fila_processos_bloqueados)
                    memoria.m_livre -= fila_processos_bloqueados_suspensos[i].espacoMemoria
                    fila_processos_bloqueados_suspensos.pop(i)
                    if memoria.m_livre == 0:
                        return
                    prioridade -= 1
                    break
        prioridade += 1


def subfila_de_prioridade(menor_prioridade: int, lista: List[Processo]):
    for i in range(len(lista)):
        if lista[i].prioridade == menor_prioridade:
            return lista[i:]
    return []
