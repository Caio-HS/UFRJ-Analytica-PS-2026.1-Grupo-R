#Codigo do gemini
# ESSE CODIGO GARANTE QUE O PAR (time, id_veiculo) E UNICO
import pandas as pd
import sys

inputFile = sys.argv[1]
inputExtension = "_metrico.csv"
outputExtension = "_preprocessado.csv"
inputFilename = inputFile + inputExtension
outputFilename = inputFile + outputExtension

# 1. Carregar o CSV
df = pd.read_csv(inputFilename)

# Salvar a ordem original das colunas para garantir que a saída seja idêntica
colunas_originais = df.columns.tolist()

# 2. Agrupar sem reordenar (sort=False)
# Isso garante que a ordem das linhas permaneça a mesma do arquivo de entrada
df_limpo = df.groupby(['time', 'id_veiculo'], sort=False).agg({
    'x': 'mean', 
    'y': 'mean'
}).reset_index()

# 3. Reorganizar as colunas para a ordem original
# (Caso o groupby tenha mudado a posição de 'x' e 'y')
df_limpo = df_limpo[colunas_originais]

# 4. Salvar o CSV limpo
df_limpo.to_csv(outputFilename, index=False)
