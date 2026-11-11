from fastapi import FastAPI,Body, HTTPException
from rag import construir_contexto
from model import Contexto,Documento

app = FastAPI()


@app.get('/health')
def health_check():
    return {'status':'ok'}
 

@app.post('/contexto')
def contexto(dados: Contexto):
    embedding = dados.embedding_pergunta
    documentos = dados.documentos

    limite_documentos = dados.limite_documentos
    similaridade_minima = dados.similaridade_minima
    max_palavras = dados.max_palavras
    
    
    dados_recuperados=construir_contexto(embedding,documentos,limite_documentos,similaridade_minima,max_palavras)

    if dados_recuperados ==ValueError:
        raise HTTPException(status_code=400,detail='erro de vetor')
    return dados_recuperados