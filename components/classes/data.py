class Data:
    def __init__(self, dia, mes, ano, hora, minuto):
        self.dia = dia
        self.mes = mes
        self.ano = ano
        self.hora = hora
        self.minuto = minuto

    @property # getter // x.data = isso
    def data(self):
        return f'{self.dia}/{self.mes}/{self.ano} {self.hora}:{self.minuto}'

    def json(self): # transforma uma data em json puro
        return dict(dia=self.dia, mes=self.mes, ano=self.ano, hora=self.hora, minuto=self.minuto)
