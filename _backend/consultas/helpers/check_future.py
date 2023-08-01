from datetime import datetime

def check_future(day1, day2):
    data1 = datetime(day1.ano, day1.mes, day1.dia)
    data2 = datetime(day2.ano, day2.mes, day2.dia)
    if data2 > data1:
        return (data2-data1).days
    else:
        return False