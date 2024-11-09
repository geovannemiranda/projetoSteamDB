import pandas as pd

# Carregar o arquivo CSV com a codificação correta
df = pd.read_csv("steam_sales.csv", on_bad_lines='skip', encoding='latin1')

# Mantém apenas as colunas 'nome' e 'preço'
df = df[['Nome do Jogo', 'Preço']]

# Salvar o arquivo organizado em um novo CSV
df.to_csv("dados_organizados.csv", index=False)
