from pydantic import BaseModel

class Documento(BaseModel):
    id:int 
    titulo: str
    conteudo: str
    embedding: list[float]


class Contexto(BaseModel):
    embedding_pergunta: list[float]
    documentos:list[Documento]
    limite_documentos:int
    similaridade_minima:float
    max_palavras:int


