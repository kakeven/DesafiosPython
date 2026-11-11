# Desafio 05 — Etapa B: Avaliação offline da recuperação

**Trilha:** AI Engineering  
**Dificuldade:** Intermediária+  
**Tempo sugerido:** 30–45 minutos  
**Pré-requisito:** ter implementado `buscar_documentos()` no Mini-RAG dos desafios anteriores.

## 1. Objetivo

Agora que seu Mini-RAG recupera documentos, você precisa **medir a qualidade dessa recuperação**. Em vez de verificar apenas se a função executa, compare os documentos retornados com um gabarito de relevância conhecido.

Nesta etapa, você vai calcular duas métricas:

- **Recall@K:** proporção dos documentos relevantes que aparecem entre os primeiros `K` resultados.
- **Hit Rate@K:** proporção das perguntas em que pelo menos um documento relevante foi recuperado.

**Não implemente um LLM nem gere embeddings reais.** Reutilize sua função de busca.

## 2. O que implementar

Crie um arquivo `avaliacao.py` com a função:

```python
def avaliar_recuperacao(
    casos: list[dict],
    documentos: list[dict],
    limite: int = 3,
    similaridade_minima: float = 0.0
) -> dict:
    pass
```

> **Adaptação ao seu projeto:** se `buscar_documentos()` recebe `list[Documento]` do Pydantic, adapte apenas a anotação de `documentos` e o formato dos dados de teste. Não reescreva o algoritmo de recuperação.

Cada caso de avaliação contém:

- `embedding_pergunta`: vetor usado para realizar a busca.
- `ids_relevantes`: IDs dos documentos considerados relevantes segundo o gabarito.

Para cada caso:

1. Execute a função `buscar_documentos()` existente com o embedding, os documentos e os parâmetros de busca.
2. Obtenha os IDs dos documentos recuperados entre os primeiros `K` resultados.
3. Compare-os com `ids_relevantes`.
4. Calcule o Recall@K daquela pergunta e registre se houve ao menos um acerto.

Ao final, calcule o Recall@K médio e o Hit Rate@K considerando todos os casos.

## 3. Fórmulas

**Recall@K de uma pergunta:**

```text
Recall@K = (nº de documentos relevantes recuperados entre os K primeiros)
           / (nº total de documentos relevantes no gabarito)
```

**Recall@K médio:**

```text
Recall médio = soma dos recalls de cada pergunta / total de perguntas
```

**Hit Rate@K:**

```text
Hit Rate = nº de perguntas com pelo menos um acerto / total de perguntas
```

### Exemplo conceitual

Se os IDs relevantes são `[1, 3, 5]` e sua busca retorna `[1, 2, 3]`, com `K = 3`:

- Dois dos três documentos relevantes foram encontrados: `Recall@3 = 2/3`.
- A pergunta teve pelo menos um acerto: contribui com `1` para o cálculo do Hit Rate.

## 4. Regras de comportamento

- `K = limite` quando `limite > 0`.
- Se `limite <= 0`, nenhum documento é recuperado.
- Se `ids_relevantes` estiver vazio em qualquer caso, lance `ValueError`.
- Se `casos` estiver vazio, retorne `recall_medio = 0.0`, `hit_rate = 0.0` e `total_casos = 0`.
- Não arredonde os resultados durante os cálculos.
- Não altere as listas ou os dicionários recebidos.
- Não chame `construir_contexto()`: a avaliação deve usar diretamente a função de busca, sem aplicar o orçamento de palavras.

Retorne **exatamente** este formato:

```python
{
    "total_casos": int,
    "recall_medio": float,
    "hit_rate": float
}
```

## 5. Dados públicos para testar

Use os cinco documentos do JSON do Desafio 05 (cancelamento, pagamento e entrega), com os mesmos embeddings e IDs.

```python
casos = [
    {"embedding_pergunta": [1.0, 0.0, 0.0], "ids_relevantes": [1, 3]},
    {"embedding_pergunta": [0.0, 1.0, 0.0], "ids_relevantes": [2, 5]},
    {"embedding_pergunta": [0.0, 0.0, 1.0], "ids_relevantes": [4]},
    {"embedding_pergunta": [-1.0, 0.0, 0.0], "ids_relevantes": [1]},
]
```

Teste com `limite=2` e `similaridade_minima=0.0`.

**Resultado esperado:**

```python
{
    "total_casos": 4,
    "recall_medio": 0.75,
    "hit_rate": 0.75
}
```

Na quarta pergunta, o gabarito inclui um documento que sua busca por similaridade positiva não recupera. Isso é intencional: uma avaliação também deve revelar limitações do recuperador.

## 6. Teste automatizado

Crie um teste no `pytest`. O exemplo abaixo pressupõe que você tenha a variável `documentos` com os cinco documentos de exemplo (no tipo que sua função aceita):

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

Crie também testes próprios para uma lista de casos vazia, um gabarito vazio e um limite igual a zero. Priorize entender os cálculos, em vez de criar dezenas de verificações artificiais.

## 7. Mini relatório técnico (até 200 palavras)

No `README.md`, responda com suas palavras:

1. Por que Recall@K e Hit Rate@K são métricas diferentes?
2. Em que tipo de pergunta seu recuperador pode falhar?
3. O que poderia melhorar a recuperação **sem alterar o contrato HTTP**?

Não invente resultados experimentais: use apenas as métricas que você realmente calcular.

## 8. Critérios para concluir a etapa

- [ ] A função reutiliza `buscar_documentos()`.
- [ ] Calcula Recall@K por pergunta e a média final.
- [ ] Calcula Hit Rate@K.
- [ ] Passa no teste público (0.75 para ambas as métricas).
- [ ] Trata os três casos especiais indicados na seção 6.
- [ ] O README explica os resultados e uma limitação real.

**Foco desta etapa:** raciocinar sobre relevância, conjuntos de IDs, métricas e limitações da recuperação — não gastar a maior parte do tempo configurando a API ou fazendo validações de tipos.
