a = [2, 3, 1]
b = [4, 2,7]

c = [3, 4]

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
    
    
print(norma(c))
print(produto_escalar(a,b))
print(similaridade_cosseno(a,b))