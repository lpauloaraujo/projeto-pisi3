def classificar_lucratividade(valor):

    if valor < 0:
        return "prejuizo"
    elif valor >= 5.0:
        return "super_alta"
    elif valor >= 2.0:
        return "muito_alta"
    elif valor >= 1.4:
        return "alta"
    elif valor >= 0.8:
        return "media"
    elif valor >= 0.4:
        return "baixa"
    elif valor >= 0.2:
        return "muito_baixo"
    else:
        return "prejuizo"

def retorno_porcentagem(revenue, budget):

    lucro_percento = (revenue - budget) / budget
    return classificar_lucratividade(lucro_percento)
    
def verificador(budget, revenue):

    if not isinstance(budget, (int, float)) or budget == 0:
        return True
    if not isinstance(revenue, (int, float)) or revenue == 0:
        return True
    
    return False

def main(budget, revenue):

    if verificador(budget, revenue):
        return "lucratividade_indisponivel"

    classificacao = retorno_porcentagem(revenue, budget)
    return classificacao

if __name__ == "__main__":
    main()