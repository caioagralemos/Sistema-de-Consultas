from components.classes.data import Data

class Consulta:
    def __init__(self, nome, cpf, data):
        self.nome = nome
        self.cpf = cpf
        self.data = data

    def json(self):
        return dict(nome=self.nome, cpf=self.cpf, data=self.data.json())

    @classmethod
    def parse(cls, dados):
        dados_data = dados.pop('data')
        data = Data(**dados_data)
        dados['data'] = data
        return cls(**dados)