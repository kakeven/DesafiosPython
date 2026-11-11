# Desafios de Python para AI Engineering

Este repositório reúne desafios que estou resolvendo para desenvolver minhas habilidades em **Python e AI Engineering**, com foco na preparação para atuar na área de **AI Engineering**.

A proposta é aprender de forma prática: começar com problemas de lógica e análise de dados e avançar, passo a passo, até os componentes de um sistema que busca informações para apoiar respostas de uma IA. Os cenários dos exercícios usam temas próximos ao universo de delivery, como pedidos, avaliações, pagamentos, cancelamentos e entregas.

## O que estou praticando

- **Lógica e análise de dados:** transformar dados de pedidos em informações úteis.
- **Processamento de linguagem natural:** identificar o sentimento de avaliações de clientes a partir de regras simples.
- **Embeddings e busca vetorial:** comparar representações numéricas para encontrar documentos relacionados a uma pergunta.
- **RAG (Retrieval-Augmented Generation):** recuperar informações relevantes e organizar um contexto que poderia ser usado por um assistente de IA.
- **APIs e avaliação:** disponibilizar a busca por meio de uma API e estudar como medir a qualidade dos resultados recuperados.

## Jornada dos desafios

| Desafio | Tema | Ideia central |
| --- | --- | --- |
| [01](q1/q1.py) | Análise de pedidos | Extrair indicadores de uma lista de pedidos. |
| [02](q2/q2.md) | Classificação de avaliações | Reconhecer sentimentos positivos, negativos e neutros em textos. |
| [03](q3/q3.md) | Busca vetorial | Encontrar documentos relevantes usando similaridade entre embeddings. |
| [04](q4/desafio_04_mini_rag.md) | Mini-RAG | Selecionar documentos e montar um contexto para uma resposta. |
| [05](q5/desafio_05_api_mini_rag.md) | API e avaliação de recuperação | Expor o Mini-RAG por HTTP e explorar métricas de qualidade da busca. |

Cada pasta contém o código do desafio e, quando disponível, seu enunciado. No desafio 05, a [etapa de avaliação offline](q5/desafio_05_etapa_B_avaliacao.md) aprofunda o estudo de **Recall@K** e **Hit Rate@K**.

## Por que este projeto existe

Quero consolidar os fundamentos necessários para construir soluções de IA que sejam úteis em situações reais. Além de fazer o código funcionar, estes desafios me ajudam a pensar sobre a relevância das informações recuperadas, as limitações de uma busca e a forma de integrar esses componentes em uma aplicação.

Este é um projeto de estudo em evolução, que registra meu aprendizado ao longo da preparação para AI Engineering.
