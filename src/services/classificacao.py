def classificar_perfil(usuario):
    sobra = usuario["renda"] - (usuario["gastos_fixos"] + usuario["gastos_variaveis"])

    if usuario["dividas"] > 0 or sobra < 0:
        return "Endividado"
    
    # Se sobra dinheiro e ele já tem uma reserva guardada 
    if sobra > 0 and usuario.get("reserva_atual", 0) > 0:
        return "Pronto"

    if sobra > 0:
        return "Estável"

    return "Indefinido"