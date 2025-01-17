# Trabalho Prático 2 – DCC207 (Algoritmos 2)

**Universidade Federal de Minas Gerais**  
**Prof. Renato Vimieiro**  

Alunos: Pedro Augusto Torres Bento, Yan Aquino Amorim  

## Descrição

Este projeto apresenta soluções para o problema do Caixeiro Viajante (TSP) utilizando:

1. **Branch and Bound** (solução exata).  
2. **Twice-Around-Tree** (aproximação).  
3. **Christofides** (aproximação).  

Inclui parsing de instâncias TSPLIB, cálculo de matrizes de distância e avaliação de custos das rotas.

---

## Como Executar

1. **Pré-requisitos**: Python 3.x, `networkx`.  
2. Coloque arquivos `.tsp` no diretório `tsp_instances`.  
3. Execute:  
   - Para todos os arquivos:  
     ```bash
     python main.py
     ```
   - Para um arquivo específico:  
     ```bash
     python main.py caminho/para/arquivo.tsp
     ```
4. Resultados serão salvos em `tsp_results.json`.  

