TEMPOMAXIMO = 3


class IO(object):

    def __init__(self):
        self.emUso = False
        self.tempoUso = TEMPOMAXIMO
        self.processoId = None

    def isDisponivel(self):
        return not self.emUso

    def decrementaTempoUso(self):
        self.tempoUso -= 1
        if self.tempoUso == 0:
            self.livre()

    def livre(self):
        self.tempoUso = TEMPOMAXIMO
        self.processoId = None

    def getTempoRestante(self):
        return self.tempoUso

    def ocupado(self, processoId):
        self.emUso = True
        self.processoId = processoId
