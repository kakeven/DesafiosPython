
pedidos = [
    {
    "id": 1,
    "valor": 45.9,
    "status": "entregue"
  },
  {
    "id": 2,
    "valor": 32.5,
    "status": "cancelado"
  },
  {
    "id": 3,
    "valor": 78,
    "status": "entregue"
  },
  {
    "id": 4,
    "valor": 25,
    "status": "pendente"
  },
  {
    "id": 5,
    "valor": 54.9,
    "status": "entregue"
  },
  {
    "id": 6,
    "valor": 45.9,
    "status": "entregue"
  }
]



def analisar_pedidos(pedidos: list[dict]) -> dict: # type: ignore
    qtd_pedidos = len(pedidos)
    
    total_faturado_entregue = 0
    media_pedidos_entregue = 0
    maior_pedido_id = None
    maior_pedido_valor = 0
    quantidade_cancelados = 0
    valores_duplicados = []
    valores_visitados = set()

    entregas = 0
   
    
    for i in range(qtd_pedidos):
        if pedidos[i]["status"] == 'entregue':
            total_faturado_entregue += pedidos[i]["valor"]
            entregas +=1

            if pedidos[i]["valor"] not in valores_visitados:
                valores_visitados.add(pedidos[i]["valor"])
            else: valores_duplicados.append(pedidos[i]["valor"])


            if pedidos[i]["valor"] > maior_pedido_valor:
                maior_pedido_valor = pedidos[i]["valor"]
                maior_pedido_id = pedidos[i]["id"]

            

        
        elif pedidos[i]["status"] == 'cancelado' :
            quantidade_cancelados += 1


    if entregas >0:
        media_pedidos_entregue = total_faturado_entregue/entregas
    else:
        media_pedidos_entregue = 0

    return {'total_faturado': round(total_faturado_entregue,2),'media_pedidos': round(media_pedidos_entregue,3),
            'maior_pedido':maior_pedido_id,'quantidade_cancelados':quantidade_cancelados,
            'valores_duplicados': sorted(valores_duplicados)}

print(analisar_pedidos(pedidos))



# total_faturado: soma dos valores dos pedidos entregues.
# media_pedidos: valor médio dos pedidos entregues.
# maior_pedido: ID do pedido entregue com maior valor.
# quantidade_cancelados: número de pedidos cancelados.
# valores_duplicados: lista de valores que aparecem mais de uma vez entre os pedidos entregues, sem repetições, em ordem crescente.