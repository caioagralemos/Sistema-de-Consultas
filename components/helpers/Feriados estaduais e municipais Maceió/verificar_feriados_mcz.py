import datetime as dt
import math

'''
O Dia da Páscoa, por definição, é o primeiro Domingo após a lua cheia que ocorre após o equinócio vernal, e pode cair entre 22 de Março e 
25 de Abril. A seqüência dos dias de Páscoa se repete em ciclos de aproximadamente 5.700.000 anos. As fórmulas existentes calculam o que 
se convencionou chamar de "Cálculo Eclesiástico", quando em 325 o Concílio de Nicea assim definiu.
Sexta-Feira Santa acontece 2 dias antes da Páscoa.
Corpus Christi acontece 60 dias depois da Páscoa.
Existem diversas fórmulas para a determinação do Domingo de Páscoa, entretanto uma das mais simples é a fórmula de Gauss, descrita a 
seguir:

Tabela importante para o cálculo, pois define os valores de de X e Y para a fórmula.
O código ira funcionar de 1901 até o ano de 2099, pois os valores de X e Y estão definidos manualmente para poupar processamento da
máquina, visto que é irreal de acontecer de alguém marcar uma consulta para depois de 2099.

faixa de anos	X	Y
1582	1599	22	2
1600	1699	22	2
1700	1799	23	3
1800	1899	24	4
1900	2019	24	5
2020	2099	24	5
2100	2199	24	6
2200	2299	25	7

'''

def pascoa(dia, mes, ano):
    x = 24
    y = 5
    a = math.fmod(ano, 19)
    b = math.fmod(ano, 4)
    c = math.fmod(ano, 7)
    d = math.fmod((19*a)+x, 30)
    e = math.fmod((2*b)+(4*c)+(6*d)+y, 7)

    if d + e > 9:
        diaPascoa = d+e-9
        mesPascoa = 4
    else:
        diaPascoa = d+e+22
        mesPascoa = 3
    
    if mesPascoa == 4 and diaPascoa == 26:
        diaPascoa = 19
    elif mesPascoa == 4 and diaPascoa == 25 and d == 28 and a > 10:
        diaPascoa = 18
    
    if dia == diaPascoa and mes == mesPascoa:
        return True

    mesSextSanta = mesPascoa
    diaSextSanta = diaPascoa - 2
    if diaSextSanta <= 0:
        mesSextSanta -= 1
        diaSextSanta = 30 - diaSextSanta

    if dia == diaSextSanta and mes == mesSextSanta:
        return True

#Março 31
#Abril 30
#Maio 31
#Junho 30

    diaCorpusChristi = diaPascoa + 60
    if mesPascoa == 3:
        diaCorpusChristi -= 31
        mesCorpusChristi = mesPascoa + 1
        if diaCorpusChristi > 30:
            diaCorpusChristi -= 30
            mesCorpusChristi += 1
    elif mesPascoa == 4:
        diaCorpusChristi -= 30
        mesCorpusChristi = mesPascoa + 1
        if diaCorpusChristi > 31:
            diaCorpusChristi -= 31
            mesCorpusChristi += 1
    
    if dia == diaCorpusChristi and mes == mesCorpusChristi:
        return True
    
    return False

def feriados_est_mcz(dia, mes, ano):

    if pascoa(dia, mes, ano) or (dia == 24 and mes == 6) or (dia == 29 and mes == 6) or (dia == 16 and mes == 9) or (dia == 20 and mes == 11) or (dia == 30 and mes == 11) or (dia == 27 and mes == 8) or (dia == 8 and mes == 12):
        return True
    else:
        return False


'''ano = 2023
mes = 4
dia = 7

if feriados_est_mcz(dia, mes, ano):
    print('Essa data é no dia de um feriado')
else:
    print('Essa data não é no dia da páscoa')'''