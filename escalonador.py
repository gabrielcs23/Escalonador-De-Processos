from filaDeProcessos import FilaDeProcessos
from processo import Processo
TEMPOREAL = 0


def main():
    filaTempoReal = FilaDeProcessos()
    filaUsuario = FilaDeProcessos()
    filaEntrada = inicilizarEntrada('entrada.txt')
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
