from inout import IO


class GerenciaIO(object):

    impressora_1 = None
    impressora_2 = None
    cd_1 = None
    cd_2 = None
    scanner = None
    modem = None

    def __init__(self):
        self.impressora_1 = IO()
        self.impressora_2 = IO()
        self.cd_1 = IO()
        self.cd_2 = IO()
        self.scanner = IO()
        self.modem = IO()

    def qtdImpressoraDisponivel(self):
        qtd = 0
        if self.impressora_1.isDisponivel():
            qtd += 1
        if self.impressora_2.isDisponivel():
            qtd += 1
        return qtd

    def alocaImpressora(self, idProcesso, qtdPraAlocar):
        if qtdPraAlocar == 1:
            if self.impressora_1.isDisponivel():
                self.impressora_1.ocupado(idProcesso)
            elif self.impressora_2.isDisponivel():
                self.impressora_2.ocupado(idProcesso)
        else:
            if self.impressora_1 and self.impressora_2.isDisponivel():
                self.impressora_1.ocupado(idProcesso)
                self.impressora_2.ocupado(idProcesso)

    def qtdCdDisponivel(self):
        qtd = 0
        if self.cd_1.isDisponivel():
            qtd += 1
        if self.cd_2.isDisponivel():
            qtd += 1
        return qtd

    def alocaCd(self, idProcesso, qtdPraAlocar):
        if qtdPraAlocar == 1:
            if self.cd_1.isDisponivel():
                self.cd_1.ocupado(idProcesso)
            elif self.cd_2.isDisponivel():
                self.cd_2.ocupado(idProcesso)
        else:
            if self.cd_1.isDisponivel() and self.cd_2.isDisponivel():
                self.cd_1.ocupado(idProcesso)
                self.cd_2.ocupado(idProcesso)

    def isScannerDisponivel(self):
        return self.scanner.isDisponivel()

    def alocaScanner(self, idProcesso):
        if self.isScannerDisponivel():
            self.scanner.ocupado(idProcesso)

    def isModemDisponivel(self):
        return self.modem.isDisponivel()

    def alocaModem(self, idProcesso):
        if self.isModemDisponivel():
            return self.modem.ocupado(idProcesso)

    def atualizaTempoUso(self):
        if self.impressora_1.processoBloqueado:
            self.impressora_1.decrementaTempoUso()
        if self.impressora_2.processoBloqueado:
            self.impressora_2.decrementaTempoUso()
        if self.cd_1.processoBloqueado:
            self.cd_1.decrementaTempoUso()
        if self.cd_2.processoBloqueado:
            self.cd_2.decrementaTempoUso()
        if self.scanner.processoBloqueado:
            self.scanner.decrementaTempoUso()
        if self.modem.processoBloqueado:
            self.modem.decrementaTempoUso()
