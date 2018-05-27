from processo import Processo


class FilaDeProcessos(object):
    processosEspera: []
    processosProntos: []
    processosBloqueados: []
    processosExecutando: []

    def __init__(self):
        pass
