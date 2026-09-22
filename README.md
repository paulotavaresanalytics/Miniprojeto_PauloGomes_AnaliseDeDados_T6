# Miniprojeto_PauloGomes_AnaliseDeDados_T6

Análise Exploratória de Dados (AED) da base Varejo (Kaggle), desenvolvida como
Mini-Projeto Avaliativo do curso de Análise de Dados com Python (SCTEC, Turma T6).

## 1. Situação-problema

O ponto de partida foi entender o que a base "Varejo" realmente representa: cada
linha do CSV não é uma venda fechada, é um **item comprado**. Uma mesma compra
pode ter vários itens, e é o campo `CO_ID` que amarra esses itens numa mesma
transação. Isso muda a forma de pensar a análise — contar linhas não é o mesmo
que contar compras, e essa distinção guiou boa parte das decisões do projeto.

## 2. Entregáveis do projeto

- Script Python comentado (`miniprojeto_analise_varejo.py`)
- Dataset limpo exportado (`df_limpo.csv`)
- Este README.md, com a reflexão sobre ETL e qualidade de dados
- `README_PauloGomes_T6.md` com instruções de execução
- Repositório público no GitHub, com histórico de commits por sprint

## 3. Ambiente de desenvolvimento

O projeto foi desenvolvido em **GitHub Codespaces**, direto no repositório:

1. Repositório aberto e Codespace criado a partir do botão "Create codespace on main"
2. Verificação do Python já disponível no ambiente: `python3 --version` → 3.14.2
3. Instalação das bibliotecas necessárias:
```bash
   pip install pandas numpy matplotlib kagglehub
```
4. Autenticação no Kaggle via `kaggle.json` (token de API), necessária para o
   `kagglehub` baixar a base `namespaiva/base-varejo` diretamente no ambiente

## 4. Reflexão teórica: ETL e qualidade de dados

Esse projeto é, na prática, um mini-ETL: **E**xtração (download via `kagglehub`
+ leitura com `pandas.read_csv`, com atenção ao separador `;` característico
de bases exportadas em pt-BR), **T**ransformação (conversão de tipos, tratamento
de valores ausentes e categorias inconsistentes) e **L**oad (exportação do
dataset limpo em `df_limpo.csv`, pronto para alimentar análises futuras ou um
dashboard).

Qualidade de dados não é só "tirar o que está errado" — é entender **por que**
está errado antes de decidir o que fazer. A categoria ausente aparecia como a
string `"#N/D"` em vez de um nulo tradicional, o que só foi percebido ao
inspecionar `value_counts()` da coluna, não apenas `isnull().sum()`. Ambos os
casos (nulo real e `#N/D`) foram tratados como "Sem Categoria" — a lógica
aplicada é equivalente a um `if/else`: se a categoria está ausente ou marcada
como não-disponível, atribui-se "Sem Categoria"; caso contrário, mantém-se o
valor original. Isso foi implementado de forma vetorizada (`.replace()` +
`.fillna()`), que é a abordagem idiomática em pandas para esse tipo de
condicional em massa.

Duplicatas exatas foram removidas por representarem repetição de registro, não
uma nova transação. Já a coluna `DATA`, originalmente texto, foi convertida
para `datetime` com `errors="coerce"` — decisão que evita que uma data mal
formatada quebre o pipeline inteiro, transformando-a em `NaT` reportável em vez
de um erro fatal.

## 5. Como o projeto foi construído (sprints)

- **Sprint 1 — Importação:** download da base via `kagglehub` e inspeção inicial
  (shape, colunas, tipos, amostra) para mapear o dataset real, sem assumir
  nomes de colunas de projetos anteriores.
- **Sprint 2 — Transformação de tipos:** remoção de colunas fantasma geradas
  pelo `;` sobrando no CSV e conversão de `DATA` para `datetime`.
- **Sprint 3 — Limpeza de nulos e duplicatas:** tratamento do `#N/D` em
  `PR_CAT` e remoção de duplicatas exatas, com justificativa para cada decisão.
- **Validação de regra de negócio:** confirmação de que `CO_ID` agrupa vários
  itens numa mesma compra, com estatística de itens por transação.
- **Sprint 4 — Estatística descritiva:** média, mediana, desvio padrão, moda,
  máximo, mínimo, contagem e quartis da coluna `CL_FHL` (número de filhos).
- **Sprint 5 — Agrupamentos e conclusões:** cruzamento categoria x gênero,
  percentuais de concentração e análise temporal (dia da semana / semana a
  semana), fechando com o bloco de insights.

## 6. Conclusões e insights

1. **ALIMENTOS domina o mix de vendas**, respondendo por ~52% de todos os itens
   comprados — mais que o triplo da segunda colocada (HIGIENE, ~19%), indicando
   uma base de clientes orientada a consumo básico recorrente.

2. **Gênero não segmenta a categoria comprada**: a proporção F/M se mantém
   praticamente igual em quase todas as categorias (~52%/48%), com exceção
   discreta de PET e BEBIDAS, onde a presença masculina (48,1% e 48,3%) supera
   levemente a média geral (47,9%).

3. **[DIA]** concentra o maior volume de compras da semana, o que aponta para
   um padrão de consumo ligado a [rotina de reposição doméstica / final de
   semana / início de semana — ajuste conforme o dia real].

4. **Semana [SEMANA]** teve o maior número de compras no período analisado,
   sinalizando [pico sazonal / efeito de datas específicas — investigar se
   coincide com algum evento do calendário de varejo].

5. **Mulheres representam ~52%** das compras únicas — leve maioria, mas a base
   é razoavelmente equilibrada entre os gêneros.

6. **Problema remanescente:** a base não possui coluna de valor monetário, o
   que limita a análise a volume (itens/compras). Uma extensão natural seria
   cruzar `PR_ID` com uma tabela de preços para estimar receita e ticket médio
   por categoria, dia e semana.