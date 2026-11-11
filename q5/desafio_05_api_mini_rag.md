# Desafio 05 — AI Engineer Take-Home: Mini-RAG como API e avaliação

**Trilha:** AI Engineering  
**Área:** APIs, FastAPI, validação de dados e integração de recuperação vetorial  
**Linguagem:** Python 3  
**Dificuldade:** Intermediária+ (progressão do Desafio 04)  
**Tempo sugerido:** 90 minutos para o núcleo + 30–45 minutos para a etapa de avaliação  
**Dependências:** `fastapi`, `uvicorn`, `pytest`, `httpx`  
**Formato:** Simulação de take-home: requisitos, testes públicos, extensão e justificativa técnica

> **Objetivo de aprendizagem:** integrar um componente de recuperação existente a uma API, testar seu comportamento e medir sua qualidade com um conjunto de avaliação pequeno. Há tarefas obrigatórias e uma extensão progressiva; não implemente um LLM.

## 1. Contexto

Você entrou em uma equipe que já possui um protótipo de Mini-RAG (seu código do Desafio 04). A plataforma de delivery quer disponibilizar esse componente para outros serviços. A recuperação vetorial já existe; agora ela precisa ser acessível por uma API que receba uma pergunta representada por embedding, selecione documentos e devolva o contexto resultante.

O fluxo será:

```text
Cliente HTTP
    ↓ POST /contexto
Validação do JSON
    ↓
Recuperação vetorial (Desafio 03)
    ↓
Construção do contexto (Desafio 04)
    ↓
Resposta JSON ou erro HTTP apropriado
```

**Escopo obrigatório (Etapa A):** API e robustez. **Extensão (Etapa B):** avaliação offline da recuperação. Não gere embeddings, não use LLM, banco de dados nem autenticação neste desafio.

## 2. Objetivo e entrega

Entregue `main.py`, `rag.py`, `test_main.py` e um `README.md` curto com instruções de execução, escolhas técnicas e limitações. Não precisa construir interface web ou Docker. O corretor poderá executar testes adicionais não mostrados aqui, desde que respeitem este contrato.

**Estratégia recomendada:** primeiro faça a Etapa A passar; só então implemente a Etapa B. O código do Desafio 04 é seu ponto de partida, não uma solução a reescrever inteira.

Crie uma aplicação FastAPI com:

- `GET /health`: verifica se a API está acessível.
- `POST /contexto`: recebe os parâmetros de recuperação e retorna o resultado de `construir_contexto()`.

Reaproveite sua solução do Desafio 04 e ajuste erros que impeçam que a API cumpra o contrato. **Não copie o algoritmo de busca para dentro da rota.**

## 3. Dados de entrada

A rota `POST /contexto` recebe JSON neste formato:

```json
{
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
```

Todos os campos de documento são obrigatórios. Os três parâmetros finais são opcionais, com os padrões indicados acima. `embedding_pergunta` e `documentos` são obrigatórios.

## 4. Requisitos funcionais

### RF01 — Saúde da aplicação

`GET /health` deve retornar HTTP `200` e o JSON exato:

```json
{"status": "ok"}
```

### RF02 — Contrato e validação da entrada

Utilize modelos Pydantic para os dados da requisição e da resposta. Valide:

1. `id`: inteiro (não booleano).
2. `titulo` e `conteudo`: strings, inclusive vazias.
3. Embeddings: listas de números finitos; rejeite `NaN`, `Infinity`, strings e booleanos como componentes.
4. `limite_documentos`: inteiro, com valor padrão `3`. Aceite zero e negativos para preservar o comportamento do Desafio 04.
5. `similaridade_minima`: número finito, com valor padrão `0.5`.
6. `max_palavras`: inteiro, com valor padrão `100`. Aceite zero e negativos.
7. Rejeite IDs de documentos repetidos para evitar ambiguidade.

Para erros de formato/tipo/valor da requisição, retorne HTTP `422`, com uma descrição que permita identificar o campo problemático. Use a validação do FastAPI/Pydantic; não é necessário inventar um formato próprio de erro.

### RF03 — Dimensões incompatíveis

Se algum embedding de documento tiver dimensão diferente da dimensão de `embedding_pergunta`, retorne HTTP `400` com:

```json
{"detail": "Dimensões incompatíveis entre embeddings"}
```

Essa verificação deve funcionar mesmo se um dos vetores estiver vazio ou tiver norma zero. Uma lista de documentos vazia é válida e não precisa dessa comparação.

**Atenção:** não devolva HTTP `500` para esse erro previsível do cliente.

### RF04 — Reutilização do Mini-RAG

`POST /contexto` deve usar a função `construir_contexto()` do Desafio 04, mantendo as regras de:

- Filtro de similaridade e descarte de similaridades menores ou iguais a zero.
- Ordenação por similaridade decrescente e, no empate, ID crescente.
- Aplicação de `limite_documentos` **antes** do orçamento de palavras.
- Inclusão de blocos inteiros que caibam no orçamento, pulando candidatos grandes sem buscar além do limite de candidatos.
- Formatação `[Documento N] Título\nConteúdo`, com `\n\n` **somente entre** os blocos.
- Status: `sucesso`, `sem_resultados` ou `limite_insuficiente`.

Não arredonde similaridades para tomar decisões e não altere os dados recebidos.

### RF05 — Resposta da API

Com entrada válida, `POST /contexto` deve devolver HTTP `200` e **exatamente** as cinco chaves do Mini-RAG:

```json
{
  "contexto": "[Documento 1] Cancelar pedido\nO cliente pode cancelar antes da confirmação.\n\n[Documento 2] Solicitar cancelamento\nApós a confirmação, o cancelamento depende da loja.",
  "documentos_utilizados": [1, 3],
  "total_documentos": 2,
  "total_palavras": 23,
  "status": "sucesso"
}
```

`sem_resultados` e `limite_insuficiente` são resultados válidos do domínio e **também devem retornar HTTP `200`**, não `404` nem `500`.

## 5. Organização sugerida (não obrigatória)

```text
mini_rag_api/
├── main.py          # FastAPI, rotas, modelos e tratamento de erros
├── rag.py           # Funções dos desafios anteriores
└── test_main.py     # Testes HTTP
```

Você pode escolher outra estrutura, desde que a rota não duplique a lógica vetorial.

## 6. Casos extremos obrigatórios

1. `GET /health`.
2. Requisição válida do exemplo (IDs `[1, 3]`, 23 palavras).
3. Campos opcionais omitidos — uso dos valores padrão.
4. Lista `documentos` vazia — `sem_resultados` com HTTP `200`.
5. Nenhum documento relevante — `sem_resultados` com HTTP `200`.
6. `max_palavras=0` com candidatos relevantes — `limite_insuficiente` com HTTP `200`.
7. `limite_documentos=0` — `sem_resultados` com HTTP `200`.
8. Documento grande seguido por outro menor que caiba.
9. Dois documentos com similaridades iguais — menor ID primeiro.
10. Embeddings de dimensões diferentes — HTTP `400` com `detail` definido.
11. Dimensões diferentes e vetor de norma zero — também HTTP `400`.
12. `embedding_pergunta` vazio e documentos com embeddings não vazios — HTTP `400`.
13. Campo obrigatório ausente — HTTP `422`.
14. Valor de embedding como string ou booleano — HTTP `422`.
15. IDs repetidos — HTTP `422`.
16. Título ou conteúdo vazio — aceitar, respeitando a formatação.
17. Nenhuma quebra de linha sobrando no fim do contexto.

## 7. Testes automatizados (sem solução)

Use `pytest` e `fastapi.testclient.TestClient`. Os exemplos abaixo assumem que a aplicação FastAPI se chama `app`, em `main.py`. Crie uma fixture ou função auxiliar `payload_exemplo()` contendo o JSON da seção 3. Ela deve retornar uma **nova cópia** do payload a cada chamada.

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


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
```

**Sua tarefa:** completar `payload_exemplo()` e criar testes para todos os demais casos da seção 6. Não é necessário copiar este arquivo de testes literalmente.

## 8. Etapa B — Avaliação offline da recuperação (extensão progressiva)

Esta etapa aproxima o desafio de um **take-home de AI Engineer**. Em vez de apenas ver se a API responde, você mede se o mecanismo recupera documentos relevantes em um conjunto de perguntas conhecido. **Não exige LLM nem embeddings reais.**

### B1 — Função de avaliação

Crie em `avaliacao.py`:

```python
def avaliar_recuperacao(
    casos: list[dict],
    documentos: list[dict],
    limite: int = 3,
    similaridade_minima: float = 0.0
) -> dict:
    pass
```

Cada caso possui `embedding_pergunta` e `ids_relevantes` (lista de IDs considerados relevantes segundo um gabarito). Para cada caso, utilize **a função de busca existente**, sem alterar o orçamento nem chamar `construir_contexto()`. Os documentos recuperados devem vir na ordem retornada pela busca e limitados a `limite`.

Calcule:

- **Recall@k por pergunta**: quantidade de IDs relevantes recuperados entre os primeiros `k`, dividida pela quantidade total de IDs relevantes no gabarito.
- **Recall@k médio**: média aritmética do recall entre os casos.
- **Taxa de acerto@k (hit rate)**: fração dos casos com **pelo menos um** ID relevante recuperado.

Convenções para tornar a avaliação determinística:

- Aqui `k = limite` quando `limite > 0`; com `limite <= 0`, nenhum documento é recuperado.
- Casos com `ids_relevantes` vazio são **inválidos** e devem gerar `ValueError`; não tente dividir por zero.
- Se `casos` estiver vazio, retorne `recall_medio=0.0`, `hit_rate=0.0` e `total_casos=0`.
- Não arredonde valores no cálculo; os testes poderão usar `pytest.approx`.
- Não altere listas ou dicionários recebidos.

Retorne exatamente:

```python
{
    "total_casos": int,
    "recall_medio": float,
    "hit_rate": float
}
```

### B2 — Dados públicos da avaliação

Use os cinco documentos da seção 3 e estes casos:

```python
casos = [
    {"embedding_pergunta": [1.0, 0.0, 0.0], "ids_relevantes": [1, 3]},
    {"embedding_pergunta": [0.0, 1.0, 0.0], "ids_relevantes": [2, 5]},
    {"embedding_pergunta": [0.0, 0.0, 1.0], "ids_relevantes": [4]},
    {"embedding_pergunta": [-1.0, 0.0, 0.0], "ids_relevantes": [1]}
]
```

**Teste público da extensão (sem fornecer implementação):**

```python
import pytest
from avaliacao import avaliar_recuperacao

def test_avaliacao_publica():
    resultado = avaliar_recuperacao(
        casos, documentos, limite=2, similaridade_minima=0.0
    )
    assert resultado["total_casos"] == 4
    assert resultado["recall_medio"] == pytest.approx(0.75)
    assert resultado["hit_rate"] == pytest.approx(0.75)
```

Na quarta pergunta, o gabarito contém um documento que a busca por similaridade positiva **não recupera**. Esse caso é intencional: os testes devem mostrar limitações do recuperador, não apenas cenários favoráveis.

### B3 — Mini relatório técnico (até 200 palavras)

No `README.md`, explique: (1) por que recall e hit rate são métricas diferentes; (2) um tipo de pergunta em que seu sistema pode falhar; (3) o que você faria para melhorar a recuperação sem mudar o contrato HTTP. **Descreva limites reais, não invente números.**

## 9. Simulação de revisão de código

Depois que todos os testes públicos passarem, prepare-se para uma pequena alteração pedida por um entrevistador: "O cliente agora quer `limite_documentos=1`. O que muda no retorno? Quais testes comprovam que o restante do contrato permanece intacto?" **Não crie uma segunda rota para isso**. Demonstre o comportamento por teste e explique a decisão em 3–5 frases. Esse exercício treina extensão e defesa do código existente.

### Checklist antes de entregar

- `pytest` passa localmente.
- A API respeita exatamente o contrato JSON e os códigos HTTP previstos.
- `README.md` informa como executar e quais dependências instalar.
- Os testes cobrem casos felizes e falhas, sem depender de internet.
- Você sabe explicar por que cada validação pertence à API ou ao núcleo de busca.

## 10. Restrições técnicas

- Não use banco de dados, FAISS, NumPy nem serviços de IA neste desafio.
- Não escreva toda a lógica dentro da função da rota.
- Não use `except Exception` para mascarar todos os erros como se fossem do cliente.
- Não modifique os dados de entrada nem o contrato de saída do Mini-RAG.
- Considere apenas requisições com JSON dentro dos limites habituais de um exercício local; autenticação, rate limiting e limites de tamanho do payload ficam fora do escopo.
- Resolva primeiro com sua própria implementação; use testes e mensagens de erro para diagnosticar problemas.

## 11. Critérios de avaliação

| Critério | Peso |
|---|---:|
| Contrato HTTP, rotas e códigos de status | 15% |
| Validação com Pydantic | 15% |
| Integração e reutilização do Mini-RAG | 20% |
| Casos extremos e testes automatizados | 20% |
| README, organização e justificativa técnica | 10% |
| Avaliação offline: métricas e casos (Etapa B) | 20% |
| **Total** | **100%** |

**Nota máxima:** 10 pontos. A **Etapa A vale 8 pontos** e a **Etapa B vale 2 pontos**. A tabela acima detalha a avaliação global; a revisão oral e o relatório ajudam a julgar clareza.

**Importante:** para acompanhar sua progressão, você pode encerrar a primeira sessão após a Etapa A; a pontuação global completa pressupõe as duas etapas.

## 12. Bônus — raciocínio de engenharia (sem código obrigatório)

Responda com suas palavras:

1. Por que `sem_resultados` deve retornar HTTP `200`, enquanto dimensões incompatíveis retornam `400`?
2. Qual a diferença entre a validação de tipos do Pydantic e a validação de regras do negócio?
3. O que pode acontecer se você reutilizar um objeto de payload mutável entre testes?
4. Por que é preferível manter o algoritmo RAG separado da rota HTTP?
5. Qual é o custo aproximado de calcular similaridade para `N` documentos de dimensão `D` e ordenar os resultados?
6. Se os documentos forem armazenados em um banco, quais mudanças arquiteturais seriam necessárias sem alterar o contrato da API?

## 13. Perguntas para revisão técnica

1. Qual a diferença entre `GET` e `POST` neste contexto?
2. O que o FastAPI faz quando uma requisição não corresponde ao esquema de entrada?
3. Quando usar HTTP `400`, `422` e `500`?
4. O que é um teste de integração HTTP e como ele difere de testar `construir_contexto()` isoladamente?
5. Como assegurar que mudanças futuras em `rag.py` não quebrem os clientes da API?

---

**Objetivo final:** expor seu Mini-RAG por HTTP e avaliá-lo com um pequeno benchmark reproduzível. Priorize a Etapa A antes da Etapa B. Não é necessário acrescentar interface, LLM ou agentes.

### Origem da inspiração (não é reprodução literal)

- [Hex — AI Engineering Take-Home](https://github.com/hex-inc/ai-eng-takehome): avaliação por casos e melhoria de um sistema existente.
- [Argmax — Search by Ingredients Challenge](https://github.com/argmaxml/hiring_challenge_2025): busca aplicada e defesa/extensão da solução.
- [Curling AI — Multi-Source Agent Challenge](https://github.com/Curling-AI/hiring-challenge-alpha): integração, comportamento robusto e organização de componentes.

Os requisitos, contratos, métricas e testes deste documento são **autorais**, adaptados para a progressão didática; não são questões copiadas desses processos.
