import holidays

def checar_feriado(data):
    feriados = holidays.Brazil()

    if data in feriados:
        return True
    else:
        return False
