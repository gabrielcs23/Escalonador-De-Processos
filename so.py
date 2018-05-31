from cpu import CPU
from processo import Processo
from gerencia_inout import GerenciaIO
from memoria import Memoria
from escalonador import escalona_lp, escalonador_mp_ativa
from escalonadorCurtoPrazo import rodadaDeEscalonadorCurto, moveBloqueadoParaExecutando
from typing import List
from bcolors import BColors
import os

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

    def passagemDeTempo(self):
        for cpu in self.cpus:
            if cpu.processo:
                cpu.quantum -= 1

        self.gerenciadorIO.atualizaTempoUso()
        self.tempoSistema += 1

    def imprimeSO(self):
        vazio = "--"
        print(BColors.BOLD + BColors.AMARELO + "\n\nTEMPO DE EXECUCAO: " + BColors.ROSA + str(self.tempoSistema))
        print(BColors.AMARELO + "\nCPUs:\n" + BColors.AZUL)
        print("+-------+-------+-------+-------+")
        print("| CPU 0 | CPU 1 | CPU 2 | CPU 3 |")
        print("+-------+-------+-------+-------+")
        print("|",end="")
        for i in range(4):
            if self.cpus[i].processo is not None:
                print(BColors.ROSA + BColors.BOLD + "  P" + str(self.cpus[i].processo.id)+"  ",end="")
            else:
                print(BColors.AZUL + BColors.BOLD + BColors.VERMELHO + "  --  " + BColors.ENDC,end="")
            print(" " + BColors.AZUL + "|",end="")
        print(BColors.AZUL)
        print("+-------+-------+-------+-------+")

        print(BColors.AMARELO + BColors.BOLD + "\n\nDISPOSITIVOS\t|\tPROCESSO \t|\tTempo Restante\n")
        if self.gerenciadorIO.impressora_1.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "Impressora 1    " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(self.gerenciadorIO.impressora_1.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "Impressora 1    " + BColors.AMARELO + "|\t\t" + BColors.ROSA + str(self.gerenciadorIO.impressora_1.processoId) + "\t\t|\t" + str(self.gerenciadorIO.impressora_1.getTempoRestante()) + BColors.ENDC)

        if self.gerenciadorIO.impressora_2.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "Impressora 2    " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.impressora_2.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "Impressora 2     \t" + str(
                self.gerenciadorIO.impressora_2.processoId) + "\t\t|\t" + str(
                self.gerenciadorIO.impressora_2.getTempoRestante()) + BColors.ENDC)

        if self.gerenciadorIO.cd_1.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "CD 1            " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.cd_1.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "CD 1            " + BColors.AMARELO + "|\t\t" + BColors.ROSA + "P" + str(
                self.gerenciadorIO.cd_1.processoId) + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.cd_1.getTempoRestante()) + BColors.ENDC)

        if self.gerenciadorIO.cd_2.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "CD 2            " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.cd_2.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "CD 2            " + BColors.AMARELO + "|\t\t" + BColors.ROSA + "P" + str(
                self.gerenciadorIO.cd_2.processoId) + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.cd_2.getTempoRestante()) + BColors.ENDC)

        if self.gerenciadorIO.modem.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "Modem           " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.modem.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "Modem           " + BColors.AMARELO + "|\t\t" + BColors.ROSA + "P" + str(
                self.gerenciadorIO.modem.processoId) + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.modem.getTempoRestante()) + BColors.ENDC)

        if self.gerenciadorIO.scanner.processoId is None:
            print(BColors.AZUL + BColors.BOLD + "Scanner         " + BColors.AMARELO + "|\t\t" + BColors.ROSA + vazio + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.scanner.getTempoRestante()) + BColors.ENDC)
        else:
            print(BColors.AZUL + BColors.BOLD + "Scanner         " + BColors.AMARELO + "|\t\t" + BColors.ROSA + "P" + str(
                self.gerenciadorIO.scanner.processoId) + BColors.AMARELO + "\t\t|\t" + BColors.ROSA + str(
                self.gerenciadorIO.scanner.getTempoRestante()) + BColors.ENDC)


def imprimeFilas(pProntos : List[Processo], pPSuspensos : List[Processo], pBlock : List[Processo],
                 pBSuspensos  : List[Processo], pFinalizados : List[Processo]):

    print(BColors.AMARELO + BColors.BOLD + "\nFILAS:" + BColors.ENDC)

    print(BColors.AZUL + BColors.BOLD + "\nNovos:" + BColors.ROSA )


    print(BColors.AZUL + BColors.BOLD + "\nProntos:" + BColors.ROSA )
    for k in range(len(pProntos)):
        if pProntos[k] is not None:
            print("P" + str(pProntos[k].id) + ", ",end="")

    print(BColors.AZUL + BColors.BOLD + "\nPronto-Suspensos:" + BColors.ROSA)
    for k in range(len(pPSuspensos)):
        if pPSuspensos[k] is not None:
            print("P" + str(pPSuspensos[k].id) + ", ",end="")

    print(BColors.AZUL + BColors.BOLD + "\nBloqueados:" + BColors.ROSA)
    for k in range(len(pBlock)):
        if pBlock[k] is not None:
            print("P" + str(pBlock[k].id) + ", ",end="")

    print(BColors.AZUL + BColors.BOLD + "\nBloqueado-Suspensos:" + BColors.ROSA)
    for k in range(len(pBSuspensos)):
        if pBSuspensos[k] is not None:
            print("P" + str(pBSuspensos[k].id) + ", ",end="" + BColors.ROSA)

    print(BColors.AZUL + BColors.BOLD + "\nFinalizados:" + BColors.ROSA)
    for k in range(len(pFinalizados)):
        if pFinalizados[k] is not None:
            print("P" + str(pFinalizados[k].id) + BColors.AZUL + " entrou na cpu em " + BColors.ROSA + "T=" + str(pFinalizados[k].tempoInicial) + BColors.AZUL + " e finalizou em " + BColors.ROSA + "T=" + str(pFinalizados[k].tempoFinalizacao) + "\n"
                  , end="")

    print("\n")



def main():
    filaEntrada = inicilizarEntrada('entrada.txt')
    processosNovos = {'tempoReal': [], 'usuario': []}
    processosProntos = []
    processosProntosSuspenso = []
    processosBloqueados = []
    processosBloqueadosSuspenso = []  # Não ta sendo passado pra nenhuma função
    processosExecutando = []
    processosFinalizados = []

    so = SO()
    memoria = Memoria()
    gerenciaIO = GerenciaIO()

    totalProcessos = len(filaEntrada)

    while len(processosFinalizados) != totalProcessos:
        # Escalonador de longo prazo
        while len(filaEntrada) > 0 and filaEntrada[0].tempoChegada == so.tempoSistema:  # Isso vai dar certo?
            if filaEntrada[0].prioridade == 0:
                processosNovos['tempoReal'].append(filaEntrada.pop(0))
            else:
                processosNovos['usuario'].append(filaEntrada.pop(0))
        escalona_lp(so.gerenciadorIO, processosProntos, processosProntosSuspenso, processosBloqueados, processosBloqueadosSuspenso, processosNovos, memoria)

        # Escalonador de médio prazo (acho que não vai ser chamado explicitamente, só indiremantente pro swap)
        if (len(processosProntos) == 0 and len(processosProntosSuspenso) > 0) or (len(processosBloqueados) == 0 and len(processosBloqueadosSuspenso) > 0):
            escalonador_mp_ativa(gerenciaIO, processosProntos,processosProntosSuspenso,processosBloqueados, processosBloqueadosSuspenso, memoria)


        # Escalonador de curto prazo
        rodadaDeEscalonadorCurto(so.tempoSistema, memoria, so.gerenciadorIO, processosBloqueados, processosProntos,
                                                       processosExecutando, processosFinalizados, so.cpus)

        #moveBloqueadoParaExecutando(processosBloqueadosSuspenso,processosProntosSuspenso)
        # Espera um enter para entrar no próximo loop
        os.system('cls' if os.name == 'nt' else 'clear')
        so.imprimeSO()
        memoria.imprimeMemoria()
        imprimeFilas(processosProntos, processosProntosSuspenso, processosBloqueados, processosBloqueadosSuspenso, processosFinalizados)
        so.passagemDeTempo()

        input()

# arquivo de entrada deve ter cada parametro do processo separado por VIRGULA + ESPAÇO
def inicilizarEntrada(nomeArquivo):
    identificador = 1
    arquivoEntrada = open(nomeArquivo, 'r')
    filaEntrada = []
    for linha in arquivoEntrada:
        linha = linha.split(', ')
        linha = [int(x) for x in linha]
        novoProcesso = Processo(linha[0], linha[1], linha[2], linha[3], linha[4], linha[5], linha[6], linha[7])
        novoProcesso.id = identificador
        filaEntrada.append(novoProcesso)
        identificador += 1

    arquivoEntrada.close()
    return filaEntrada


main()
