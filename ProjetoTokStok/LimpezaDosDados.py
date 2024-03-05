import pandas as pd
import matplotlib.pyplot as plt

# carregar ficheiro
df = pd.read_csv('DecoracaoDeParedeCSV.csv', sep=';')

# imprime os 5 primeiros / default é 5
print(df.head())

#excluir espaços em branco no inicio e fim, podem ser expressas em 2 convensões:
# (mapper, axis={'index', 'columns'}, ...) / df.rename(str.lower, axis='columns')
# (index=index_mapper, columns=columns_mapper, ...) / df.rename(columns={"A": "a", "B": "c"})
# strip é uma função que pertence a classe de strings. Como parametro opcional colocamos o conjunto de caracteres a serem removidos
df = df.rename(columns=lambda x : x.strip())

# verifica se há linhas com valores nulos
# is.null() Return a boolean same-sized object indicating if the values are NA.
print(df.isnull().sum())

# apaga as linhas com valores nulos e salva numa nova variavel / Default axis: index, how: any
df=df.dropna(subset=['Fornecedor','VC','Custo','VENDA'])
df=df.dropna(how="all")

# verifica se há linha duplicadas
# duplicated(): Return boolean Series denoting duplicate rows. Considering certain columns is optional: df.duplicated(subset=['brand'])
# By default use all of the columns.
print(df.duplicated().sum())

# elimina linhas duplicadas / By default, it removes duplicate rows based on all columns.
# df.drop_duplicates(subset=['brand', 'style'], keep='last')
df = df.drop_duplicates()

#criar df com as colunas pretendidas
df = df[['Categoria','Descrição', 'CV', 'VC', 'Custo', 'VENDA', 'OR']]

# exclusão de espaços em branco entre números, ex: '3 654' para '3654' e substituir , por . e transformar dados em float
#Em pandas, quando você tem uma coluna que contém dados de texto (strings), você pode usar o acessador .str para aplicar operações de string a todos os elementos dessa coluna.
df[['VC', 'Custo', 'VENDA']] = df[['VC', 'Custo', 'VENDA']].apply(lambda x: x.str.replace(' ', '').str.replace(',', '.').astype(float))

print(df.head(20))

# gravar o ficheiro tratado
df.to_csv('DecoracaoDeParedeSlim.csv', index=False)