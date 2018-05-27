from processo import Processo
from so import SO


# escalonador a longo prazo
def escalona_lp(self, fila_processos_prontos, lista_novos, memoria):
    # enquanto a lista de processos novos de tempo real estiver com elementos, faça...
    while len(lista_novos['tempoReal']) > 0:
        # se houver memoria livre pra colocar o proximo processo da lista de novos processos
        if memoria.m_livre > lista_novos['tempoReal'][0].mbytes:
            # coloca o processo e retira este processo da lista de novos processos
            SO.insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos)
            memoria.m_livre -= lista_novos['tempoReal'][0].mbytes
            lista_novos['tempoReal'].pop(0)
        else:
            # libera qtd de memoria suficiente pra inserir o proximo processo na lista de pronto
            self.escalona_mp_suspende(self, lista_novos['tempoReal'][0].mbytes, fila_processos_prontos, memoria)
            # e agora que possui memoria disponivel, insere o novo processo na lista de prontos
            SO.insereProcesso(lista_novos['tempoReal'][0], fila_processos_prontos)
            memoria.m_livre -= lista_novos[0].mbytes
            lista_novos['tempoReal'].pop(0)
    # mesma ideia do while anterior, mas para lista de usuario
    while len(lista_novos['usuario']) > 0:
        if memoria.m_livre > lista_novos['usuario'][0].mbytes:
            SO.insereProcesso(lista_novos['usuario'][0], fila_processos_prontos)
            memoria.m_livre -= lista_novos['usuario'][0].mbytes
            lista_novos['usuario'].pop(0)
        else:
            self.escalona_mp_suspende(self, lista_novos['usuario'][0].mbytes, fila_processos_prontos, memoria)
            SO.insereProcesso(lista_novos['usuario'][0], fila_processos_prontos)
            memoria.m_livre -= lista_novos['usuario'][0].mbytes
            lista_novos['usuario'].pop(0)

# escalonador a medio prazo, parte que remove da memoria principal
# esta funcao libera memoria até ter no minimo uma quantidade (qtd_memoria) livre
def escalona_mp_suspende(self, qtd_memoria, processosBloqueados, processosBloqueadosSuspensos, processosProntos, processosProntosSuspensos, memoria):
    # retira o processo mais recente com prioridade 3 da fila de bloqueado,
    # caso nao exista retira o processo mais recente com prioridade 3 da fila de prontos

    # repete os passos acima com prioridade 2, 1, e 0, nesta ordem
    prioridade = 3
    # enquanto nao houver (qtd_memoria) memoria disponivel e prioridade for maior ou igual a 0...
    while memoria.m_livre < qtd_memoria and prioridade >= 0:
        # range começa em tamanho da fila -1 (ultimo elemento), vai até 0 (-1 nao incluso) e em passos de -1
        for i in range(len(processosBloqueados)-1,-1,-1):
            # caso a região tenha prioridade menor do que a prioridade analisada, break
            if processosBloqueados[i].prioridade < prioridade:
                break
            # caso contrário, estamos na região com prioridade igual a prioridade analisada
            else:
                # insere na fila de bloqueado suspenso, remove da fila de bloqueados,
                # atualiza memoria livre, diminui i para analisar o indice correto da proxima vez
                SO.insereProcesso(processosBloqueados[i], processosBloqueadosSuspensos)
                memoria.m_livre += processosBloqueados[i].mbytes
                processosBloqueados.pop(i)
                i -= 1
                # caso ja tenha memoria o suficiente, break
                if memoria.m_livre > qtd_memoria:
                    return
        # mesma analise anterior, porem para a lista de prontos/prontos suspensos
        for i in range(len(processosProntos)-1,-1,-1):
            if processosProntos[i].prioridade != prioridade:
                break
            else:
                SO.insereProcesso(processosProntos[i], processosProntosSuspensos)
                memoria.m_livre += processosProntos[i].mbytes
                processosProntos.pop(i)
                i -= 1
                if memoria.m_livre > qtd_memoria:
                    return
        # diminui prioridade em 1 para analisar a próxima prioridade
        prioridade -= 1
