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