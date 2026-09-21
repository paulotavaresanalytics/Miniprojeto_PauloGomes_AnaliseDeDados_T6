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