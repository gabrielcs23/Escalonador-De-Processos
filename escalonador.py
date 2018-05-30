from gerencia_inout import GerenciaIO
from processo import Processo, insereProcesso
from typing import List, Dict


# escalonador a longo prazo
def escalona_lp(ger_io: GerenciaIO, fila_processos_prontos: List[Processo],
                fila_processos_prontos_suspensos: List[Processo], fila_processos_bloqueados: List[Processo],
                fila_processos_bloqueados_suspensos: List[Processo], lista_novos: Dict, memoria):
    # enquanto a lista de processos novos de tempo real estiver com elementos, faça...
    while len(lista_novos['tempoReal']) > 0:
        # se houver memoria livre pra colocar o proximo processo da lista de novos processos
        if memoria.m_livre >= lista_novos['tempoReal'][0].espacoMemoria:
            # coloca o processo e retira este processo da lista de novos processos
            insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos)
            memoria.m_livre -= lista_novos['tempoReal'][0].espacoMemoria
        else:
            # tenta liberar espaço para inserir processo
            # libera os processos de prioridade maior (>0)
            # se conseguir, insere na lista de prontos
            # caso contrario, insere na lista de prontos suspensos
            escalona_mp_suspende(lista_novos['tempoReal'][0].espacoMemoria,
                                 subfila_de_prioridade(1, 3, fila_processos_prontos), fila_processos_prontos_suspensos,
                                 subfila_de_prioridade(1, 3, fila_processos_bloqueados),
                                 fila_processos_bloqueados_suspensos, memoria)
            if memoria.m_livre >= lista_novos['tempoReal'][0].espacoMemoria:
                insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos)
                memoria.m_livre -= lista_novos['tempoReal'][0].espacoMemoria
            else:
                insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos_suspensos)
        lista_novos['tempoReal'].pop(0)
    # mesma ideia do while anterior, mas para lista de usuario
    while len(lista_novos['usuario']) > 0:
        # se o processo possui todos os recursos disponiveis, checa memoria
        if lista_novos['usuario'][0].qtdImpressora <= ger_io.qtdImpressoraDisponivel() and lista_novos[
            'usuario'][0].qtdCd <= ger_io.qtdCdDisponivel() and (
                not lista_novos['usuario'][0].qtdScanner or ger_io.isScannerDisponivel()) and (
                not lista_novos['usuario'][0].qtdModem or ger_io.isModemDisponivel()):
            # se tem memoria, insere na lista de pronto
            if memoria.m_livre >= lista_novos['usuario'][0].espacoMemoria:
                insereProcesso(lista_novos['usuario'][0], fila_processos_prontos)
                memoria.m_livre -= lista_novos['usuario'][0].espacoMemoria
            else:
                # caso contrario, tenta liberar memoria
                escalona_mp_suspende(lista_novos['usuario'][0].espacoMemoria,
                                     subfila_de_prioridade(
                                         lista_novos['usuario'][0].prioridade, 3, fila_processos_prontos),
                                     fila_processos_prontos_suspensos,
                                     subfila_de_prioridade(
                                         lista_novos['usuario'][0].prioridade, 3, fila_processos_bloqueados),
                                     fila_processos_bloqueados_suspensos, memoria)
                # se conseguiu liberar memoria, insere na lista de pronto
                if memoria.m_livre >= lista_novos['usuario'][0].espacoMemoria:
                    insereProcesso(lista_novos['usuario'][0], fila_processos_prontos)
                    memoria.m_livre -= lista_novos['usuario'][0].espacoMemoria
        else:
            insereProcesso(lista_novos['usuario'][0], fila_processos_prontos_suspensos)
        lista_novos['usuario'].pop(0)


# escalonador a medio prazo, parte que remove da memoria principal
# esta funcao libera memoria até ter no minimo uma quantidade (qtd_memoria) livre
def escalona_mp_suspende(qtd_memoria,  fila_processos_prontos: List[Processo],
                         fila_processos_prontos_suspensos: List[Processo], fila_processos_bloqueados: List[Processo],
                         fila_processos_bloqueados_suspensos: List[Processo], memoria):
    # retira o processo mais recente com prioridade 3 da fila de bloqueado,
    # caso nao exista retira o processo mais recente com prioridade 3 da fila de prontos

    # repete os passos acima com prioridade 2, 1, e 0, nesta ordem
    prioridade = 3
    # enquanto nao houver (qtd_memoria) memoria disponivel e prioridade for maior ou igual a 0...
    while memoria.m_livre < qtd_memoria and prioridade >= 0:
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
                i -= 1
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
                i -= 1
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
                if memoria.m_livre - fila_processos_prontos_suspensos[i] > 0\
                        and fila_processos_prontos_suspensos[i].qtdImpressora <= ger_io.qtdImpressoraDisponivel()\
                        and fila_processos_prontos_suspensos[i].qtdCd <= ger_io.qtdCdDisponivel()\
                        and (not fila_processos_prontos_suspensos[i].qtdScanner or ger_io.isScannerDisponivel())\
                        and (not fila_processos_prontos_suspensos[i].qtdModem or ger_io.isModemDisponivel()):
                    # insere na fila de processos prontos, remove da lista de prontos suspenso e atualiza memoria
                    insereProcesso(fila_processos_prontos_suspensos[i], fila_processos_prontos)
                    memoria.m_livre -= fila_processos_prontos_suspensos[i].espacoMemoria
                    fila_processos_prontos_suspensos.pop(i)
                    # se nao houver mais memoria, return
                    if memoria.m_livre == 0:
                        return
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
        prioridade += 1


def subfila_de_prioridade(menor_prioridade:int, maior_prioridade:int, lista:List[Processo]):
    comeco = 0
    fim = len(lista) - 1
    for i in range(len(lista)):
        if lista[i].prioridade<menor_prioridade:
            comeco = i
    for i in range(len(lista)-1, -1, -1):
        if lista[i].prioridade>maior_prioridade:
            fim = i
    return lista[comeco+1:fim]