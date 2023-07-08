class Data:
    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    @property
    def data(self):
        return f'{self.dia}/{self.mes}/{self.ano}'

    def json(self):
        return dict(dia=self.dia, mes=self.mes, ano=self.ano)