from bcolors import BColors


class Processo(object):

    id = None
    t_chegada = None
    prioridade = None
    t_processo = None
    mbytes = None
    n_printer = None
    n_modem = None
    n_scanner = None
    n_cd = None
    estado = None
    tempo_restante = None

    def __init__(self, t_c, p, t_p, mb, np, nm, ncd):
        self.id = id
        self.t_chegada = t_c
        self.prioridade = p
        self.t_processamento = t_p
        self.mbytes = mb
        self.n_printer = np
        self.n_modem = nm
        self.ncd = ncd
        self.estado = "Espera"
        self.tempo_restante = t_p

    def imprime_processo(self):

        print("Processo " + str(self.id) + "\n")
        print("Estado " + self.estado + "\n")
        print("Tempo de chegada: " + str(self.id) + "\n")
        print("Prioridade " + str(self.id) + "\n")
        print("Tamanho " + str(self.id) + "\n")
