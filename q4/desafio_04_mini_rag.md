# Desafio 04 — Mini-RAG: recuperação e montagem de contexto

**Trilha:** AI Engineering  
**Área:** Recuperação de Informação, Embeddings e RAG  
**Linguagem:** Python 3  
**Dificuldade:** Intermediária  
**Tempo sugerido:** 90 minutos  
**Formato:** Implementação de funções com testes automatizados  
**Dependências:** Apenas biblioteca padrão do Python

> **Objetivo de aprendizagem:** evoluir seu motor de busca vetorial do Desafio 03 para selecionar documentos e construir um contexto limitado, pronto para ser entregue a um modelo de linguagem. **Não é necessário chamar uma IA, gerar embeddings nem implementar a resposta do modelo.**

## 1. Contexto

Uma plataforma de delivery mantém documentos sobre cancelamentos, pagamentos e entregas. Antes de responder ao cliente, um assistente precisa recuperar informações relevantes e organizar o material que será enviado ao modelo de linguagem.

O fluxo simplificado é:

```text
Pergunta + embedding já gerado
             ↓
    Recuperação vetorial
             ↓
   Ordenação por relevância
             ↓
 Seleção por orçamento de palavras
             ↓
Contexto textual pronto para o LLM
```

Sua tarefa se concentra na **recuperação e na montagem do contexto**. Em uma aplicação real, a resposta do LLM seria uma etapa posterior.

## 2. Objetivo

Implemente a função:

```python
def construir_contexto(
    embedding_pergunta: list[float],
    documentos: list[dict],
    limite_documentos: int = 3,
    similaridade_minima: float = 0.5,
    max_palavras: int = 100
) -> dict:
    pass
```

Você pode reutilizar as funções `produto_escalar`, `norma`, `similaridade_cosseno` e `buscar_documentos` do Desafio 03. O desafio é **integrar essas funções e controlar o contexto**, não reimplementar a matemática do zero.

## 3. Requisitos funcionais

### RF01 — Recuperação vetorial

1. Calcule a similaridade de cosseno entre `embedding_pergunta` e o embedding de cada documento.
2. Descarte similaridades **menores** que `similaridade_minima` e também todas as similaridades **menores ou iguais a zero**.
3. Ordene por **maior similaridade** e, em caso de empate, por **menor ID**.
4. Considere no máximo os primeiros `limite_documentos` documentos dessa ordenação.
5. Não arredonde as similaridades durante o cálculo ou a ordenação.

**Importante:** o limite de documentos é aplicado **antes** do orçamento de palavras. Se um dos documentos considerados não couber, não procure substitutos além desses primeiros `limite_documentos`.

Se os vetores tiverem dimensões diferentes, a função auxiliar de similaridade deve lançar `ValueError`, conforme o Desafio 03. Vetores de norma zero produzem similaridade `0.0`; vetores de dimensões diferentes devem ser detectados **antes** dessa regra.

### RF02 — Formatação do contexto

Cada documento incluído deve ser representado por um bloco de duas linhas:

```text
[Documento 1] Cancelar pedido
O cliente pode cancelar antes da confirmação.
```

Regras:

- A primeira linha contém `[Documento N]`, um espaço e o título original.
- A segunda linha contém o conteúdo original (`conteudo`), mesmo que esteja vazio.
- Separe blocos incluídos por **exatamente duas quebras de linha** (`\n\n`).
- `N` começa em 1 e aumenta somente quando o documento **é incluído** no contexto. Não corresponde ao ID original nem conta documentos descartados.
- Não adicione cabeçalho geral, rodapé, marcadores extras ou espaços adicionais.

### RF03 — Orçamento de palavras

O contexto final deve satisfazer:

```python
len(contexto.split()) <= max_palavras
```

- Considere como palavra cada item resultante de `str.split()` (separação por espaços em branco).
- Conte **tudo**: `[Documento`, `N]`, palavras do título e palavras do conteúdo.
- Percorra os documentos candidatos na ordem de relevância.
- Inclua um bloco **inteiro** somente se ele couber no orçamento restante.
- Se um bloco não couber, **pule-o e continue tentando os próximos candidatos**.
- Nunca corte um título ou conteúdo para caber.
- Um bloco que ocupe exatamente todas as palavras disponíveis **pode ser incluído**.

> Para este exercício, `max_palavras` simula um orçamento de contexto. Em sistemas reais, LLMs normalmente usam limites de **tokens**, que não são equivalentes a palavras.

### RF04 — Retorno padronizado

Retorne um dicionário com exatamente estes campos:

```python
{
    "contexto": str,
    "documentos_utilizados": list[int],
    "total_documentos": int,
    "total_palavras": int,
    "status": str
}
```

- `contexto`: texto final no formato do RF02; `""` se nenhum bloco for incluído.
- `documentos_utilizados`: IDs originais dos documentos incluídos, na ordem em que aparecem no contexto.
- `total_documentos`: quantidade de documentos incluídos.
- `total_palavras`: `len(contexto.split())`.
- `status`:

| Situação | Valor |
|---|---|
| Um ou mais documentos incluídos | `"sucesso"` |
| Nenhum documento candidato após o filtro de similaridade, ou `limite_documentos <= 0` | `"sem_resultados"` |
| Há ao menos um candidato relevante, mas nenhum dos candidatos considerados cabe no orçamento | `"limite_insuficiente"` |

Se `max_palavras <= 0` e houver candidatos relevantes, o status deve ser `"limite_insuficiente"`. Se **não houver** candidatos relevantes, o status permanece `"sem_resultados"`.

### RF05 — Integridade dos dados

- Não modifique a lista de documentos de entrada.
- Não modifique os dicionários, os embeddings ou o embedding da pergunta.
- Não acrescente campos aos documentos originais.
- Considere que cada documento contém `id` (inteiro), `titulo` (string), `conteudo` (string) e `embedding` (lista numérica), todos com tipos válidos.

## 4. Dados de entrada

```python
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
```

## 5. Exemplo de execução

```python
resultado = construir_contexto(
    embedding_pergunta,
    documentos,
    limite_documentos=3,
    similaridade_minima=0.5,
    max_palavras=30
)

print(resultado)
```

Resultado esperado:

```python
{
    "contexto": (
        "[Documento 1] Cancelar pedido\n"
        "O cliente pode cancelar antes da confirmação.\n\n"
        "[Documento 2] Solicitar cancelamento\n"
        "Após a confirmação, o cancelamento depende da loja."
    ),
    "documentos_utilizados": [1, 3],
    "total_documentos": 2,
    "total_palavras": 23,
    "status": "sucesso"
}
```

Os documentos 1, 3 e 5 são os três primeiros candidatos por similaridade. Os blocos dos documentos 1 e 3 somam **23 palavras**; o bloco do documento 5 não cabe nas **7 palavras restantes** e é descartado.

## 6. Casos extremos obrigatórios

Verifique a implementação com:

1. Lista de documentos vazia.
2. Embedding da pergunta vazio e documentos com embeddings vazios (similaridade zero).
3. Vetores de dimensões diferentes (`ValueError`).
4. Vetores com números negativos ou norma zero.
5. Nenhum documento acima do limite mínimo de similaridade.
6. Similaridade igual a zero mesmo com `similaridade_minima=0.0`.
7. `limite_documentos` igual a zero ou negativo.
8. `max_palavras` igual a zero ou negativo.
9. Documento com título ou conteúdo vazio.
10. Documento longo que não cabe, seguido de um documento menor que cabe.
11. Empate de similaridade resolvido pelo menor ID.
12. Bloco que cabe **exatamente** no número máximo de palavras.
13. Contexto vazio e contagens iguais a zero quando nenhum bloco é incluído.

## 7. Testes automatizados

Os testes abaixo assumem que `documentos` e `embedding_pergunta` foram definidos como na seção 4 e que a função `construir_contexto` já foi implementada. Eles **não são a solução** do desafio.

### Teste A — Sem resultados relevantes

```python
resultado = construir_contexto(
    [0.0, 0.0, 1.0],
    documentos[:3],
    similaridade_minima=0.8
)
assert resultado["status"] == "sem_resultados"
assert resultado["contexto"] == ""
assert resultado["total_palavras"] == 0
```

### Teste B — Orçamento insuficiente

```python
resultado = construir_contexto(
    embedding_pergunta, documentos, max_palavras=2
)
assert resultado["status"] == "limite_insuficiente"
assert resultado["documentos_utilizados"] == []
assert resultado["total_documentos"] == 0
```

### Teste C — Contagem e exemplo principal

```python
resultado = construir_contexto(
    embedding_pergunta, documentos, max_palavras=30
)
assert resultado["documentos_utilizados"] == [1, 3]
assert resultado["total_documentos"] == 2
assert resultado["total_palavras"] == 23
assert resultado["total_palavras"] == len(resultado["contexto"].split())
assert resultado["status"] == "sucesso"
```

### Teste D — Integridade dos dados

```python
import copy

original = copy.deepcopy(documentos)
pergunta_original = embedding_pergunta.copy()

construir_contexto(embedding_pergunta, documentos)

assert documentos == original
assert embedding_pergunta == pergunta_original
```

### Teste E — Pular um bloco grande

```python
docs_teste = [
    {
        "id": 1,
        "titulo": "Documento grande",
        "conteudo": "palavra " * 50,
        "embedding": [1.0, 0.0]
    },
    {
        "id": 2,
        "titulo": "Documento curto",
        "conteudo": "Informação útil.",
        "embedding": [0.9, 0.1]
    }
]

resultado = construir_contexto(
    [1.0, 0.0], docs_teste, max_palavras=10
)
assert resultado["documentos_utilizados"] == [2]
assert resultado["contexto"].startswith("[Documento 1] Documento curto\n")
```

### Teste F — Empate de similaridade

```python
docs_empate = [
    {"id": 5, "titulo": "B", "conteudo": "Texto B", "embedding": [1.0, 0.0]},
    {"id": 2, "titulo": "A", "conteudo": "Texto A", "embedding": [1.0, 0.0]}
]

resultado = construir_contexto(
    [1.0, 0.0], docs_empate, limite_documentos=2
)
assert resultado["documentos_utilizados"] == [2, 5]
```

### Teste G — Limite exato

```python
resultado = construir_contexto(
    embedding_pergunta, documentos, max_palavras=23
)
assert resultado["documentos_utilizados"] == [1, 3]
assert resultado["total_palavras"] == 23
```

### Teste H — Zero não é relevância positiva

```python
resultado = construir_contexto(
    [1.0, 0.0, 0.0],
    [documentos[1], documentos[3]],
    similaridade_minima=0.0
)
assert resultado["status"] == "sem_resultados"
```

### Teste I — Dimensões incompatíveis

```python
try:
    construir_contexto(
        [1.0, 0.0],
        [documentos[0]]
    )
except ValueError:
    pass
else:
    raise AssertionError("Era esperado ValueError para dimensões diferentes")
```

## 8. Restrições técnicas

- Use apenas Python nativo e, se desejar, módulos da biblioteca padrão.
- Não use NumPy, Pandas, FAISS, scikit-learn ou serviços externos na solução principal.
- Não use modelos de IA para gerar embeddings ou responder perguntas.
- Não copie uma solução pronta: implemente sua própria lógica e registre os erros encontrados.
- Priorize funções pequenas, nomes claros, resultados determinísticos e testes reproduzíveis.

## 9. Critérios de avaliação

| Critério | Peso |
|---|---:|
| Recuperação e ordenação corretas | 20% |
| Construção e formatação do contexto | 25% |
| Controle do orçamento de palavras | 25% |
| Casos extremos e testes | 20% |
| Organização, clareza e legibilidade | 10% |
| **Total** | **100%** |

**Nota máxima: 10 pontos.**

## 10. Desafio bônus — RAG em produção (sem código obrigatório)

Responda com suas próprias palavras:

1. O que pode acontecer se um documento recuperado for semanticamente relevante, mas estiver desatualizado?
2. Por que enviar todos os documentos recuperados ao LLM pode ser uma má ideia?
3. O que é *chunking*? Como o tamanho de um trecho afeta recuperação e contexto?
4. Como tratar um documento que contenha instruções maliciosas tentando controlar o assistente (*prompt injection*)?
5. Como você avaliaria a qualidade da recuperação usando perguntas com documentos relevantes conhecidos?
6. Qual é a diferença entre limitar por palavras e limitar por tokens?

## 11. Perguntas para revisão técnica

1. Qual é a responsabilidade da recuperação vetorial e qual é a responsabilidade do LLM em um RAG?
2. Por que a ordenação dos documentos deve ocorrer antes da montagem do contexto?
3. Qual é a complexidade de calcular similaridades em `N` documentos com embeddings de `D` dimensões?
4. Como o orçamento de palavras afeta a utilidade do contexto?
5. Por que um resultado com alta similaridade não garante uma resposta correta?
6. Como você escreveria testes para garantir que a função não altera os dados recebidos?

---

**Objetivo final:** entregar uma função funcional e testada que transforma resultados de busca vetorial em um contexto textual, respeitando relevância, limite de documentos e orçamento de palavras. **Não implemente o LLM:** o foco deste desafio é a engenharia da recuperação.
