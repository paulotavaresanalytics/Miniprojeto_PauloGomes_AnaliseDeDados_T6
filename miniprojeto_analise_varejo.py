import kagglehub
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Importação dos dados
path = kagglehub.dataset_download("namespaiva/base-varejo")
print("Base baixada em:", path)

arquivos_csv = list(Path(path).rglob("*.csv"))
print("Arquivos CSV encontrados:")
for a in arquivos_csv:
    print("-", a.name)

# Se houver só um CSV, pode pegar direto o primeiro:
arquivo_varejo = arquivos_csv[0]
print("\nUsando arquivo:", arquivo_varejo.name)

df = pd.read_csv(arquivo_varejo, sep = ";")

print("\n=== Estrutura da base ===")
print("Registros:", df.shape[0], "| Colunas:", df.shape[1])
print("\nColunas:", df.columns.tolist())
print("\nTipos de dados:")
print(df.dtypes)
print("\nAmostra:")
print(df.head())

# ================== Sprint 2: Transformação de tipos ==================

# Remove colunas vazias no fim de cada lknha do csv
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# Converte DATA de string no formato (dd/mm/aaaa) para datetime real
df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

print("\n=== Sprint 2: Transformação de tipos ===")
print("Tipos de dados após conversão:")
print(df.dtypes)
print("Datas que não converteram (viraram NaT):", df["DATA"].isnull().sum())

# ================== Sprint 3: Limpeza de nulos e duplicatas ==================

print("\nDiagnóstico prévio ===")
print("Nulos por coluna:\n", df.isnull().sum())
print("Duplicatas exatas:", df.duplicated().sum())
print("Valores em PR_CAT antes do tratamento:")
print(df["PR_CAT"].value_counts(dropna=False).head(10))

# Justificativa: "#N/D" e nulos reais no campo: PR_CAT viram "Sem Categoria", pois a venda em si é um dado válido — só falta a categorização.
df["PR_CAT"] = df["PR_CAT"].replace("#N/D", "Sem Categoria")
df["PR_CAT"] = df["PR_CAT"].fillna("Sem Categoria")

# Justificativa: duplicata exata (todas as colunas iguais) não representa uma nova venda real, é repetição de registro — por isso é seguro remover.
qtd_antes = len(df)
df = df.drop_duplicates()
print(f"\nLinhas removidas por duplicata: {qtd_antes - len(df)}")

print("\n=== Sprint 3: Diagnóstico após da limpeza ===")
print("Nulos por coluna:\n", df.isnull().sum())
print("Valores em PR_CAT depois do tratamento:")
print(df["PR_CAT"].value_counts().head(10))

# ======= Valida se uma compra pode ter vários itens diferentes, conforme o: CO_ID ==================

print("\n=== Validação CO_ID ===")
print("Total de linhas (itens comprados):", len(df))
print("Total de compras únicas (CO_ID distintos):", df["CO_ID"].nunique())

itens_por_compra = df.groupby("CO_ID").size()
print("\nDistribuição de itens por compra:")
print(itens_por_compra.describe())
print("\nExemplo de uma compra com múltiplos itens:")
exemplo_id = itens_por_compra[itens_por_compra > 1].index[0]
print(df[df["CO_ID"] == exemplo_id])

# ================== Sprint 4: Estatística descritiva do número de filhos (CL_FHL) ==================

print("\n=== Sprint 4 ===")
media = df["CL_FHL"].mean() 
mediana = df["CL_FHL"].median()
desvio_padrao = df["CL_FHL"].std()
moda = df["CL_FHL"].mode()[0]
maximo = df["CL_FHL"].max()
minimo = df["CL_FHL"].min()
contagem = df["CL_FHL"].count()
quartis = df["CL_FHL"].quantile([0.25, 0.5, 0.75])

print(f"Média: {media:.2f}")
print(f"Mediana: {mediana}")
print(f"Desvio padrão: {desvio_padrao:.2f}")
print(f"Moda: {moda}")
print(f"Máximo: {maximo} | Mínimo: {minimo}")
print(f"Contagem: {contagem}")
print("Quartis (25%, 50%, 75%):\n", quartis)

# ================== Sprint 5: Agrupamentos por groupby e pivot_table ==================

print("\n=== Agrupamento 1: itens vendidos por categoria (PR_CAT) ===")
itens_por_categoria = df.groupby("PR_CAT").size().sort_values(ascending=False)
print(itens_por_categoria)

print("\n=== Agrupamento 2: número de compras únicas por gênero (CL_GENERO) ===")
compras_por_genero = df.groupby("CL_GENERO")["CO_ID"].nunique().sort_values(ascending=False)
print(compras_por_genero)

# Agrupamento extra (opcional, mas reforça a análise): pivot_table cruzando
# gênero x categoria, contando itens comprados
print("\n=== Agrupamento 3 (pivot_table): categoria x gênero ===")
pivot_categoria_genero = pd.pivot_table(
    df, index="PR_CAT", columns="CL_GENERO", values="CO_ID", aggfunc="count", fill_value=0
).sort_values(by="M", ascending=False)
print(pivot_categoria_genero.head(10))

# ================== Bônus: Percentuais de concentração ==================

print("\n=== % de participação de cada categoria no total geral de itens ===")
pct_categoria_total = (itens_por_categoria / itens_por_categoria.sum() * 100).round(2)
print(pct_categoria_total)

print("\n=== % de participação de cada gênero no total de compras ===")
pct_genero_total = (compras_por_genero / compras_por_genero.sum() * 100).round(2)
print(pct_genero_total)

print("\n=== % de F e M dentro de cada categoria (linha) ===")
pct_dentro_categoria = pivot_categoria_genero.div(pivot_categoria_genero.sum(axis=1), axis=0) * 100
print(pct_dentro_categoria.round(2))

print("\n=== % que cada categoria representa dentro do total de cada gênero (coluna) ===")
pct_por_genero = pivot_categoria_genero.div(pivot_categoria_genero.sum(axis=0), axis=1) * 100
print(pct_por_genero.round(2))

# ================== Conclusões e Insights ==================

print("\n" + "="*60)
print("CONCLUSÕES E INSIGHTS")
print("="*60)

conclusoes = """
1. ALIMENTOS domina o mix de vendas, respondendo por ~52% de todos os itens
   comprados — mais que o triplo da segunda colocada (HIGIENE, ~19%). Isso indica
   uma base de clientes fortemente orientada a compras de reposição/consumo básico.

2. A distribuição de gênero é praticamente idêntica na maioria das categorias
   (aprox. 52% mulheres / 48% homens), com uma exceção discreta: PET e BEBIDAS
   são as duas únicas categorias em que a participação masculina (48,1% e 48,3%,
   respectivamente) supera levemente a média masculina geral (47,9% do total de
   itens). A diferença é pequena, mas consistente nas duas categorias, sugerindo
   uma leve inclinação masculina para produtos de consumo próprio (bebidas) e
   cuidado com animais de estimação (pet), em comparação ao padrão de compra
   predominantemente voltado a itens de uso doméstico geral.

3. Mulheres representam ~52% das compras únicas (CO_ID) e ~52% dos itens
   comprados — uma leve maioria, mas não uma diferença expressiva. A base de
   clientes é razoavelmente equilibrada entre os gêneros.

4. A categoria "Sem Categoria" (originalmente "#N/D") representa apenas ~0,44%
   dos itens — volume baixo de dado ausente, o que reforça que a qualidade da
   base é boa e a decisão de imputação não distorce a análise.

5. As compras tendem a ter múltiplos itens (validado via CO_ID), confirmando que
   a unidade de análise de "ticket" precisa considerar o agrupamento por compra,
   não a linha individual — do contrário, métricas de volume seriam
   superestimadas ao nível de transação.

6. Problema remanescente: a base não possui coluna de valor monetário (preço/
   receita), o que limita a análise a volume (contagem de itens/compras). Uma
   extensão futura seria cruzar PR_ID com uma tabela de preços para estimar
   receita por categoria e confirmar se a leve inclinação masculina em PET e
   BEBIDAS também se reflete em ticket médio mais alto nessas categorias.
"""
print(conclusoes)