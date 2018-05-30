from cpu import CPU
from processo import Processo
from gerencia_inout import GerenciaIO
from memoria import Memoria
from escalonador import escalona_lp
from escalonadorCurtoPrazo import rodadaDeEscalonadorCurto, desalocaProcessosNaCPU
from typing import List
from bcolors import BColors

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
            if cpu.processo is not None:
                cpu.processo.tempoProcessador -= 1

        self.gerenciadorIO.atualizaTempoUso()
        self.tempoSistema += 1

    def imprimeSO(self):
        print(BColors.BOLD + BColors.AMARELO + "\n\nTEMPO DE EXECUCAO: " + BColors.ENDC + str(self.tempoSistema))
        print(BColors.BOLD + BColors.AMARELO + "\nCPUs:\n" + BColors.ENDC)
        for i in range(4):
            if self.cpus[i].processo is not None:
                print(BColors.AZUL + BColors.BOLD + "CPU" + str(i) +": " + "\tPROCESSO ID=\n" + BColors.ENDC + str(self.cpus[i].processo.id))
            else:
                print(BColors.AZUL + BColors.BOLD + "CPU" + str(i) +": "+ BColors.VERMELHO + "Vazio\n" + BColors.ENDC)

        print(BColors.AMARELO + BColors.BOLD + "\n\nDISPOSITIVOS\t|\tPROCESSO\t|\tTempo Restante\n" + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "Impressora 1    \t"+ str(self.gerenciadorIO.impressora_1.processoId) + "\t\t|\t" + str(self.gerenciadorIO.impressora_1.getTempoRestante()) + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "Impressora 2    \t"+ str(self.gerenciadorIO.impressora_2.processoId) + "\t\t|\t" + str(self.gerenciadorIO.impressora_2.getTempoRestante()) + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "CD 1            \t"+ str(self.gerenciadorIO.cd_1.processoId) + "\t\t|\t" + str(self.gerenciadorIO.cd_1.getTempoRestante()) + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "CD 2            \t"+ str(self.gerenciadorIO.cd_2.processoId) + "\t\t|\t" + str(self.gerenciadorIO.cd_2.getTempoRestante()) + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "Modem           \t"+ str(self.gerenciadorIO.modem.processoId) + "\t\t|\t" + str(self.gerenciadorIO.modem.getTempoRestante()) + BColors.ENDC)
        print(BColors.AZUL + BColors.BOLD + "Scanner         \t"+ str(self.gerenciadorIO.scanner.processoId) + "\t\t|\t" + str(self.gerenciadorIO.scanner.getTempoRestante()) + BColors.ENDC)



def imprimeFilas(pProntos : List[Processo], pPSuspensos : List[Processo], pBlock : List[Processo],
                 pBSuspensos  : List[Processo], pFinalizados : List[Processo]):

    print(BColors.AMARELO + BColors.BOLD + "\nFILAS:" + BColors.ENDC)

    print(BColors.AZUL + BColors.BOLD + "\nProntos:")
    for k in range(len(pProntos)):
        if pProntos[k] is not None:
            print("id" + str(pProntos[k].id) + ", ")

    print("\nPronto-Suspensos:")
    for k in range(len(pPSuspensos)):
        if pPSuspensos[k] is not None:
            print("id" + str(pPSuspensos[k].id) + ", ")

    print("\nBloqueados:")
    for k in range(len(pBlock)):
        if pBlock[k] is not None:
            print("id" + str(pBlock[k].id) + ", ")

    print("\nBloqueado-Suspensos:")
    for k in range(len(pBSuspensos)):
        if pBSuspensos[k] is not None:
            print("id" + str(pBSuspensos[k].id) + ", ")

    print("\nFinalizados::")
    for k in range(len(pFinalizados)):
        if pFinalizados[k] is not None:
            print("id" + str(pFinalizados[k].id) + ", ")

    print("\n\n")



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

        # Escalonador de curto prazo
        rodadaDeEscalonadorCurto(so.tempoSistema, memoria, so.gerenciadorIO, processosBloqueados, processosProntos,
                                                       processosExecutando, processosFinalizados, so.cpus)
        # Espera um enter para entrar no próximo loop

        so.imprimeSO()
        memoria.imprimeMemoria()
        imprimeFilas(processosProntos, processosProntosSuspenso, processosBloqueados, processosBloqueadosSuspenso, processosFinalizados)
        so.passagemDeTempo()

        input()

    # TODO rest of the magic


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


main()  # TODO calling magic
