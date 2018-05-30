

class Memoria:
    m_total = None
    m_livre = None
    l_espera = None
    l_executando = None




    def __init__(self):
        self.m_livre = 8192
        self.m_total = 8192

    def imprimeMemoria(self):
        print("\n\nMEMORIA:\stUSADO: " + str(self.m_total - self.m_livre) + "\nTOTAL: " + str(self.m_total))


