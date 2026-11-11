avaliacoes = [
    {"id": 10, "texto": "Ruim! RUIM, excelente."},
    {"id": 11, "texto": "Excelente!!! Excelente!!!"},
    {"id": 12, "texto": ""}
]

palavras_positivas = {
    "excelente", "rápida", "gostei", "bom", "ótimo"
}

palavras_negativas = {
    "ruim", "atrasado", "fria", "péssimo", "demorado"
}

def normalizar_frase(texto):
    pontuacoes = ['.',',','!','?']
    texto = texto.lower()

    for p in pontuacoes:
        texto = texto.replace(p,'')

    return texto



def classificar_avaliacoes(avaliacoes: list[dict],positivas: set,negativas: set) -> dict: # type: ignore

    classificacoes = []
    qtd_positivo = 0
    qtd_neutro = 0
    qtd_negativo = 0
    
    for avaliacao in avaliacoes:
        id_avaliacao = avaliacao['id']
        contador_positivo = 0
        contador_negativo = 0
        
        frase = normalizar_frase(avaliacao['texto'])        
        conjunto_frase = frase.split()
        

        for palavra in conjunto_frase:
            if palavra in positivas:
                contador_positivo+=1
            elif palavra in negativas:
                contador_negativo+=1
            

        if contador_positivo>contador_negativo:
            sentimento = 'positivo'
            qtd_positivo+=1
        elif contador_negativo>contador_positivo:
            sentimento = 'negativo'
            qtd_negativo+=1
        else:
            sentimento = 'neutro'
            qtd_neutro+=1
        classificacoes.append({'id':id_avaliacao,'sentimento':sentimento})

    return {'classificacoes':classificacoes,'resumo':{
        'positivo':qtd_positivo,
        'negativo':qtd_negativo,
        'neutro':qtd_neutro
    }}


print(classificar_avaliacoes(avaliacoes,palavras_positivas,palavras_negativas))


