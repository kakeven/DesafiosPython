documentos = [
    {
        "id": 1,
        "titulo": "Cancelar pedido",
        "embedding": [1.0, 0.0, 0.0]
    },
    {
        "id": 2,
        "titulo": "Formas de pagamento",
        "embedding": [0.0, 1.0, 0.0]
    },
    {
        "id": 3,
        "titulo": "Solicitar cancelamento",
        "embedding": [0.8, 0.2, 0.0]
    },
    {
        "id": 4,
        "titulo": "Acompanhar entrega",
        "embedding": [0.0, 0.0, 1.0]
    },
    {
        "id": 5,
        "titulo": "Pagamento de pedidos",
        "embedding": [0.6, 0.8, 0.0]
    }
]

embedding_pergunta = [1.0, 0.0, 0.0]






def produto_escalar(a, b):
    if len(a) != len(b):
        raise ValueError("Os vetores devem ter o mesmo tamanho")
    
    total = 0
    i=0
    for n in a:
        soma = n*b[i]
        total += soma
        i+=1

    return total

def norma(vetor):
    total = 0
    for v in vetor:
        soma = v**2
        total += soma  
    return total**0.5

def similaridade_cosseno(a, b):
    norma_a = norma(a)
    norma_b = norma(b)
    
    if norma_a == 0 or norma_b ==0:
        return 0.0
    
    return produto_escalar(a,b)/(norma_a*norma_b)
   





def buscar_documentos(
    embedding_pergunta: list[float],
    documentos: list[dict],
    limite: int = 3,
    similaridade_minima: float = 0.0
) -> list[dict]: # type: ignore
    lista_docs = []
    
    if limite<= 0 :
        return lista_docs
    if not embedding_pergunta:
        return []


    for doc in documentos:
        similaridade = similaridade_cosseno(doc['embedding'],embedding_pergunta)
        if similaridade>= similaridade_minima and similaridade>0:
            lista_docs.append({
                "id":doc['id'],
                'titulo':doc['titulo'],
                'similaridade': similaridade
            })
            


    lista_docs_ordenada = sorted(lista_docs,key= lambda doc:(-doc['similaridade'],doc['id']))

    return lista_docs_ordenada[:limite]
   
    
print(buscar_documentos(
    [1.0, 0.0],
    [
        {
            "id": 1,
            "titulo": "Documento",
            "embedding": [-1.0, 0.0]
        }
    ]
))