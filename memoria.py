from bcolors import BColors

class Memoria:
    m_total = None
    m_livre = None
    l_espera = None
    l_executando = None




    def __init__(self):
        self.m_livre = 8192
        self.m_total = 8192

    def imprimeMemoria(self):
        print( BColors.AMARELO +BColors.BOLD + "\nMEMORIA:\n\n" + BColors.AZUL + "USADO: " + BColors.ROSA + str(self.m_total - self.m_livre) + "/" + str(self.m_total) + BColors.ENDC)


