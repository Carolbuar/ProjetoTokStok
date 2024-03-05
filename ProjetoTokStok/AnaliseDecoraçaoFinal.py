import pandas as pd # => O Pandas é uma biblioteca de análise de dados muito popular em Python
import matplotlib.pyplot as plt # => é uma biblioteca amplamente utilizada para visualização de dados em Python, aqui esta referenciando a linha 36 a 60.
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #=>está relacionada à integração entre Matplotlib e Tkinter,permitindo a exibição de gráficos Matplotlib em janelas Tkinter, aqui esta presente na linha 65.
import tkinter as tk # =>  O tkinter oferece diversos widgets, como botões, rótulos, entradas de #texto, e outros, que podem ser incorporados em janelas para criar interfaces gráficas interativas.
from tkinter import PhotoImage
from PIL import Image, ImageTk
import numpy as np

# Carregar ficheiro
df = pd.read_csv('DecoracaoDeParedeCSV.csv', sep=';')

# Imprime os 5 primeiros / default é 5
print(df.head())

#excluir espaços em branco no inicio e fim, podem ser expressas em 2 convensões:
# (mapper, axis={'index', 'columns'}, ...) / df.rename(str.lower, axis='columns')
# (index=index_mapper, columns=columns_mapper, ...) / df.rename(columns={"A": "a", "B": "c"})
# strip é uma função que pertence a classe de strings. Como parametro opcional colocamos o conjunto de caracteres a serem removidos
df = df.rename(columns=lambda x: x.strip())

# verifica se há linhas com valores nulos
# is.null() Return a boolean same-sized object indicating if the values are NA.
print(df.isnull().sum())

# apaga as linhas com valores nulos e salva numa nova variavel / Default axis: index, how: any
df = df.dropna(subset=['Fornecedor', 'VC', 'VENDA'])
df=df.dropna(how="all")

# Verifica se há linhas duplicadas
print(df.duplicated().sum())

# verifica se há linha duplicadas
# duplicated(): Return boolean Series denoting duplicate rows. Considering certain columns is optional: df.duplicated(subset=['brand'])
# By default use all of the columns.
df = df.drop_duplicates()

# Criação de DataFrame com colunas pretendidas
df = df[['Categoria', 'Descrição', 'CV', 'VC', 'Custo', 'VENDA', 'OR']]

# Remover espaços em branco e substituir , por . e transformar dados em float
df[['VC', 'Custo', 'VENDA']] = df[['VC', 'Custo', 'VENDA']].apply(lambda x: x.str.replace(' ', '').str.replace(',', '.').astype(float))

print(df)

# PERGUNTA: Por onde começar a renovação de uma coleção de produtos de certa loja para melhorar o desempenho do setor?

# GRÁFICOS QUE AJUDARÃO NA TOMADA DE DECISÃO:
# 1. divisão do setor de decoração de parede por categoria (gráfico pizza): por tamanho de coleção e por participacao no VC- lado a lado
# 2. gráfico de barras comparando qtd produtos nacionais e importados de cada categoria, para analisar o impacto de margem
# 3. 5 produtos de menor faturamento da categoria com pior desempenho (barras horizontais do menor para o maior)

qtdProdutosPorCategoria = df.groupby('Categoria')['Descrição'].count().reset_index()
print(qtdProdutosPorCategoria)
 
vcProdutosPorCategoria = df.groupby('Categoria')['VC'].sum().reset_index()
print(vcProdutosPorCategoria)

# Adicionando colunas para contagem de 'IMP' e 'N'
df['Qtd_IMP'] = (df['OR'] == 'IMP').astype(int)
df['Qtd_N'] = (df['OR'] == 'N').astype(int)

# Agrupando por Categoria e somando as colunas Qtd_IMP e Qtd_N
impNacionalPorCategoria = df.groupby('Categoria').agg({'Qtd_IMP': 'sum', 'Qtd_N': 'sum'}).reset_index()
print(impNacionalPorCategoria)

#------------------------------------------------------

def mostrar_grafico_pizza():

    # Criação da figura e dos subgráficos
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(14, 5))
    df['Categoria'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, ax=axes[0], textprops={'color':'white'})
    vcProdutosPorCategoria['VC'].plot.pie(autopct='%1.1f%%', startangle=90, ax=axes[1], labels=None, textprops={'color':'white'})
    #df['Categoria'].value_counts().plot.pie(autopct=lambda x: f'{x:.0f}', startangle=90)
    axes[0].set_title('Participacão das Categorias por Produtos', color='white')
    axes[1].set_title('Participacão das Categorias por VC', color='white')
    #plt.ylabel(None)
    fig.set_facecolor('black')
    plt.show()

def mostrar_grafico_IMP_NAC():

    plt.figure(figsize=(12, 6), facecolor='white')

    # Configurando a largura das barras e a posição dos grupos
    largura_barra = 0.40
    posicao_barras = np.arange(len(impNacionalPorCategoria['Categoria']))

    # Criando o gráfico de barras lado a lado
    plt.barh(posicao_barras - largura_barra/2, impNacionalPorCategoria['Qtd_IMP'], height=largura_barra, label='Qtd_IMP')
    plt.barh(posicao_barras + largura_barra/2, impNacionalPorCategoria['Qtd_N'], height=largura_barra, label='Qtd_N')

    # Configurando rótulos, título, etc.
    plt.yticks(posicao_barras, impNacionalPorCategoria['Categoria'])
    plt.xlabel('Quantidade')
    plt.legend()

    plt.show()


def mostrar_grafico_piores_5_produtos():

    dadosCategoriaTelas = df[df['Categoria'] == 'Telas']
    print(dadosCategoriaTelas)

    plt.figure(figsize=(12, 6), facecolor='white')
    #df_piores_produtos = dadosCategoriaTelas.sort_values(by='VC', ascending=True).head(5)
    piores_5_produtos = dadosCategoriaTelas.nsmallest(5, 'VC')

    bars=plt.barh(piores_5_produtos['Descrição'], piores_5_produtos['VC'], color='yellow')
    #plt.xticks()

    #criação de uma instancia de eixos / get current axes
    ax = plt.gca()
    # Remover a label do eixo x
    ax.set_yticks([])

    # Adicionando rótulos diretamente ao gráfico
    for bar, descricao in zip(bars, piores_5_produtos['Descrição']):
        #funcao para adicionar texto no grafico
        plt.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2, f'{descricao}',
                va='center', color='black', fontsize=10)
    plt.title('Top 5 - Categoria Telas', fontsize=20, fontweight='bold')
    plt.xlabel('Valor de Contribuição')
    # plt.ylabel('Produto')
    plt.show()


# Função principal para criar a interface gráfica
def criar_interface_grafica():
    # Crie a janela principal
    window = tk.Tk()#=>aqui estamos criando uma janela gráfica Tkinter vazia que pode ser usada como a base para construir uma interface gráfica
    window.title("Visualização de Dados")#=> Titulo da interface grafica

    window.geometry("500x300")
    
     # Carregue a imagem usando o Pillow
    global imagem_tk
    imagem_pillow = Image.open('C:\IEFP\Python\ProjetoTokStok/Loja decoraçao.jpg')

    # Converte a imagem Pillow para PhotoImage
    imagem_tk = ImageTk.PhotoImage(imagem_pillow)

    # Crie um rótulo para exibir a imagem
    label_imagem = tk.Label(window, image=imagem_tk)
    label_imagem.pack()
    
    # Botão para mostrar o gráfico de pizza
    btn_pizza = tk.Button(window, text="Gráficos VC x Coleção", command=mostrar_grafico_pizza,width=40, height=3, background="black", foreground='white')#=> TK.Button cri botao em que a janela estara o texto "grafico de pizza", command=mostrar_grafico_pizza quando precionado ira aparecer o grafico, width=40 aqui referencia o tamanho do botao.
    btn_pizza.place(x=100, y=60)#=>aqui ajusta a disposiçao do botao na interface grafica

    btn_IMP_NAC = tk.Button(window, text="Gráfico IMP x NAC", command=mostrar_grafico_IMP_NAC, width=40, height=3,  background="black", foreground='white')
    btn_IMP_NAC.place(x=100, y=120)

    btn_piores_5 = tk.Button(window, text="Gráfico dos 5 Piores Produtos", command=mostrar_grafico_piores_5_produtos, width=40, height=3, background="black", foreground='white')
    btn_piores_5.place(x=100, y=180)

    # Inicie o loop principal da interface gráfica
    window.mainloop()#=> inicia o loop principal e mantém a aplicação em execução até que o usuário feche a janela.

# Chame a função para criar a interface gráfica
criar_interface_grafica()
