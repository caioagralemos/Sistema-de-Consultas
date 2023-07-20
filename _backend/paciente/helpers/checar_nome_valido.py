from django.core.exceptions import ValidationError


def checar_nome_valido(nome):
    permitidas = 'ABCDEFGHIJKLMNOPQRSTUVXWYZabcdefghijklmnopqrstuvxwyzáãçéêíóõôú '
    if nome[0] != nome[0].upper():
        raise ValidationError('Nome inválido!')
    for index in range(len(nome)):
        if nome[index] not in permitidas:
            raise ValidationError('Nome inválido!')
        if nome[index] == ' ':
            if nome[index+1] == 'd' and (((nome[index+2] == 'a' or nome[index+2] == 'e') and nome[index+3] == ' ') or ((nome[index+2] == 'o' and nome[index+3] == 's') and nome[index+4] == ' ')):
                continue
            elif not nome[index+1] or nome[index+1] == " " or nome[index+1] != nome[index+1].upper():
                raise ValidationError('Nome inválido!')
        if nome[index] != nome[index].lower():
            if index != 0 and nome[index-1] != ' ':
                raise ValidationError('Nome inválido!')