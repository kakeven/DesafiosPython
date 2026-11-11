from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def payload_exemplo():
    return{
  "embedding_pergunta": [1.0, 0.0, 0.0],
  "documentos": [
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
  ],
  "limite_documentos": 3,
  "similaridade_minima": 0.5,
  "max_palavras": 30
}



def test_health():
    resposta = client.get("/health")
    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}


def test_contexto_principal():
    resposta = client.post("/contexto", json=payload_exemplo())
    assert resposta.status_code == 200
    dados = resposta.json()
    assert dados["documentos_utilizados"] == [1, 3]
    assert dados["total_documentos"] == 2
    assert dados["total_palavras"] == 23
    assert dados["status"] == "sucesso"
    assert dados["contexto"] == (
        "[Documento 1] Cancelar pedido\n"
        "O cliente pode cancelar antes da confirmação.\n\n"
        "[Documento 2] Solicitar cancelamento\n"
        "Após a confirmação, o cancelamento depende da loja."
    )


def test_limite_insuficiente():
    payload = payload_exemplo()
    payload["max_palavras"] = 2
    resposta = client.post("/contexto", json=payload)
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "limite_insuficiente"
    assert resposta.json()["contexto"] == ""


def test_dimensoes_incompativeis():
    payload = payload_exemplo()
    payload["embedding_pergunta"] = [1.0, 0.0]
    resposta = client.post("/contexto", json=payload)
    assert resposta.status_code == 400
    assert resposta.json() == {
        "detail": "Dimensões incompatíveis entre embeddings"
    }


def test_campo_ausente():
    payload = payload_exemplo()
    del payload["embedding_pergunta"]
    resposta = client.post("/contexto", json=payload)
    assert resposta.status_code == 422


def test_documentos_vazios():
    payload = payload_exemplo()
    payload["documentos"] = []
    resposta = client.post("/contexto", json=payload)
    assert resposta.status_code == 200
    assert resposta.json()["status"] == "sem_resultados"
