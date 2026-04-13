import sys, csv, math, functools

# Remover aspas duplas
def clear_string(string: str) -> str:
    string = string.strip()
    if string.startswith('"'):
        string = string[1:]
    if string.endswith('"'):
        string = string[:-2]
    string = string.replace('""', '"')
    return string

# Carregar dados
def carrega(arquivo_recebido):
    dados = []
    
    #encoding='utf-8' para suportar caracteres especiais
    with open(arquivo_recebido, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
        
            partes = linha.split(',', 1)
            #evitar linhas defeituosas
            if len(partes) != 2:
                continue

            rotulo = int(partes[0])
            titulo = clear_string(partes[1])
            dados.append((rotulo, titulo))

    return dados

#Distancia de Levenshtein
def levenshtein(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j

    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,
                dp[i][j-1] + 1,
                dp[i-1][j-1] + cost
            )
    return dp[m][n]

#Comparar e retornar k mais próximos
def vizinhos_proximos(treinamento, titulo_teste, k):
    distancias = []
    for rotulo_treino, titulo_treino in treinamento:
        distancia = levenshtein(titulo_teste, titulo_treino)

        distancias.append((distancia, rotulo_treino, titulo_treino))
    
    distancias_ordenadas = sorted(distancias, key = lambda x: x[0])
    vizinhos = distancias_ordenadas[:k]

    return [(rotulo, treino) for (_, rotulo, treino) in vizinhos]

#Previsão
def prever(vizinhos):
 contagem = {0:0, 1:0}

 for rotulo, _ in vizinhos:
     contagem[rotulo] +=1

 if contagem[1] >= contagem[0]:
     return 1
 else:
     return 0

#Classificar
def classificar(treinamento, teste, k):
    resultados = []

    for rotulo_real, titulo_teste in teste:
        vizinhos = vizinhos_proximos(treinamento, titulo_teste, k)
        rotulo_previsto = prever(vizinhos)
        resultados.append((rotulo_real, rotulo_previsto))

    return resultados

#Métricas
def calcular_metricas(resultados):
    contagem = {"TP":0,"TN":0, "FP":0, "FN":0}
    
    for real, previsto in resultados:
        if real == 1 and previsto ==1:
            contagem["TP"] += 1
        elif real == 0 and previsto ==0:
            contagem["TN"] += 1
        elif real == 0 and previsto ==1:
            contagem["FP"] +=1
        elif real == 1 and previsto ==0:
            contagem["FN"] += 1
    
    TP, TN, FP, FN = contagem["TP"], contagem["TN"], contagem["FP"], contagem["FN"]
    total = TP + TN + FP + FN
    acuracia = (TP + TN) / total if total != 0 else 0.0
    precisao = TP / (TP + FP) if (TP + FP) != 0 else 0.0
    recall = TP / (TP + FN) if (TP + FN) != 0 else 0.0
    f1 = (2 * precisao * recall) / (precisao + recall) if (precisao + recall) != 0 else 0.0

    return acuracia, precisao, recall, f1

#Tabela
def imprime_tabela(acc, prec, recall, f1):
    linha = "+-------------------+"
    print(linha)
    print("|  Metric   | Value |")
    print(linha)
    print(f"| Accuracy  | {acc:.2f}  |")
    print(f"| Precision | {prec:.2f}  |")
    print(f"| Recall    | {recall:.2f}  |")
    print(f"| F1-Score  | {f1:.2f}  |")
    print(linha)
    

# Capturar valores da linha de comando
linha = input().strip().split()
arquivo_treinamento = linha[0]
arquivo_teste = linha[1]
k = int(linha[2])

#Tratamento de dados 
dados_treinamento = carrega(arquivo_treinamento)
dados_teste = carrega(arquivo_teste)

#Percorrer dados no teste
resultados = classificar(dados_treinamento, dados_teste, k)

#Calculo de acuracia, precisao, recall, f1-score
acc, prec, rec, f1 = calcular_metricas(resultados)

#Tabela
imprime_tabela(acc, prec, rec, f1)