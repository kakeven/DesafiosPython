documentos = [
    {
        "id": 1,
        "titulo": "Cancelar pedido",
        "conteudo": "O cliente pode cancelar antes da confirmação.",
        "embedding": [1.0, 0.0, 0.0]
    },
    {
        "id": 2,
        "titulo": "Formas de pagamento",
        "conteudo": "Aceitamos Pix e cartões de crédito.",
        "embedding": [0.0, 1.0, 0.0]
    },
    {
        "id": 3,
        "titulo": "Solicitar cancelamento",
        "conteudo": "Após a confirmação, o cancelamento depende da loja.",
        "embedding": [0.8, 0.2, 0.0]
    },
    {
        "id": 4,
        "titulo": "Acompanhar entrega",
        "conteudo": "O cliente acompanha a entrega pelo aplicativo.",
        "embedding": [0.0, 0.0, 1.0]
    },
    {
        "id": 5,
        "titulo": "Pagamento de pedidos",
        "conteudo": "O pagamento pode ser realizado no aplicativo.",
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
    if len(a)!=len(b):
        raise ValueError("Vetores devem possuim o mesmo tamanho")
    
    norma_a = norma(a)
    norma_b = norma(b)
    
    if norma_a == 0 or norma_b ==0:
        return 0.0
    
    return produto_escalar(a,b)/(norma_a*norma_b)
   
def buscar_documentos(embedding_pergunta: list[float],documentos: list[dict],limite: int = 3,similaridade_minima: float = 0.0,incluir_conteudo=False) -> list[dict]: # type: ignore
    lista_docs = []
    
    if limite<= 0 :
        return lista_docs
    if not embedding_pergunta:
        return []


    for doc in documentos:
        similaridade = similaridade_cosseno(doc['embedding'],embedding_pergunta)
        if similaridade>= similaridade_minima and similaridade>0: 
            if incluir_conteudo:
                lista_docs.append({
                    "id":doc['id'],
                    'titulo':doc['titulo'],
                    'conteudo':doc['conteudo'],
                    'similaridade': similaridade
                })
            else:
                lista_docs.append({
                    "id":doc['id'],
                    'titulo':doc['titulo'],
                    'similaridade': similaridade
                })
            


    lista_docs_ordenada = sorted(lista_docs,key= lambda doc:(-doc['similaridade'],doc['id']))

    return lista_docs_ordenada[:limite]




def contar_palavras(titulo='',texto='',contador=1):
    numero = len(texto.split())
    base = len(f'[Documento] {contador}'.split())
    
    
    return numero+base + len(titulo.split())

def construir_contexto(
    embedding_pergunta: list[float],
    documentos: list[dict],
    limite_documentos: int = 3,
    similaridade_minima: float = 0.5,
    max_palavras: int = 100
):  
    docs = buscar_documentos(embedding_pergunta,documentos,limite=limite_documentos,similaridade_minima=similaridade_minima,incluir_conteudo=True)
    dados = {'contexto':'',
                'documentos_utilizados':[],
                "total_documentos": 0,
                "total_palavras": 0,
                "status": None
                 }

    
    if limite_documentos <=0 or docs == []:
        dados["status"] = 'sem_resultados'
        return dados
    
    total_palavras = 0
    total_documentos = 0
    
    
        
    for doc in docs:
        
        qtd_caracteres = contar_palavras(doc['titulo'],doc['conteudo'])
        
        if qtd_caracteres>max_palavras:
            continue
        
        if qtd_caracteres+total_palavras <=max_palavras:
            total_documentos +=1
            total_palavras +=qtd_caracteres
        
            frase = f'[Documento {total_documentos}] {doc["titulo"]}\n{doc["conteudo"]}\n\n'
        
            dados["contexto"] +=frase
            dados["documentos_utilizados"].append(doc['id'])
        
        
            
    dados["total_documentos"] = total_documentos
    dados['total_palavras'] = total_palavras

    if total_documentos>0:
        dados["status"] = 'sucesso'
    else:
        dados['status'] = 'limite_insuficiente'
    
        

    return dados


