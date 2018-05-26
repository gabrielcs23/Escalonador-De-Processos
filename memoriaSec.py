from io import IO


class MemSecundaria:

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
