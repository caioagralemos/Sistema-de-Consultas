class Data:
    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano

    @property # getter // x.data = isso
    def data(self):
        return f'{self.dia}/{self.mes}/{self.ano}'

    def json(self): # transforma uma data em json puro
        return dict(dia=self.dia, mes=self.mes, ano=self.ano)