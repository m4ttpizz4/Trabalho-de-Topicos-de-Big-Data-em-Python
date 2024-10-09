#bibliotecas:
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

#variável global para salvar o estado do modo escuro:
modo_escuro = False

#função para alternar entre modos claro e escuro na interface principal:
def alternar_modo():
    global modo_escuro
    modo_escuro = not modo_escuro 
    
    #alterar cores com base no modo atual:
    if modo_escuro:
        root.configure(bg='#2E2E2E')
        btn_selecionar.configure(bg='#424242', fg='white')
        btn_modo.configure(bg='#424242', fg='white', text='Modo Claro')
        btn_grafico.configure(bg='#424242', fg='white')
    else:
        root.configure(bg='white')
        btn_selecionar.configure(bg='lightgray', fg='black')
        btn_modo.configure(bg='lightgray', fg='black', text='Modo Escuro')
        btn_grafico.configure(bg='lightgray', fg='black')

#função para abrir o arquivo e carregar os dados:
def carregar_planilha():
    arquivo = filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx"), ("CSV Files", "*.csv")])
    if arquivo:
        try:
            #lê a planilha selecionada:
            if arquivo.endswith('.xlsx'):
                dados = pd.read_excel(arquivo)
            else:
                dados = pd.read_csv(arquivo)
            
            #moldar os dados com numpy e verificar se as colunas corretas existem:
            if 'Estados' in dados.columns and 'Moradias' in dados.columns:
                #convertendo para numpy array:
                array_estados = np.array(dados['Estados'])
                array_inseguranca = np.array(dados['Moradias'])

                #gera o gráfico com base na escolha do usuário:
                tipo_grafico = combo_grafico.get()
                if tipo_grafico == "Barras":
                    gerar_grafico_barras(array_estados, array_inseguranca)
                elif tipo_grafico == "Pizza":
                    gerar_grafico_pizza(array_estados, array_inseguranca)
                elif tipo_grafico == "Linhas":
                    gerar_grafico_linhas(array_estados, array_inseguranca)
                else:
                    gerar_grafico_dispersao(array_estados, array_inseguranca)
            else:
                print("A planilha precisa conter as colunas 'Estados' e 'Moradias'.")
        except Exception as e:
            print(f"Erro ao carregar a planilha: {e}")

#função para gerar gráfico de barras com os estados:
def gerar_grafico_barras(estados, inseguranca):
    plt.figure(figsize=(12, 8))
    cor_grafico = 'white' if modo_escuro else 'black'
    cor_fundo = '#2E2E2E' if modo_escuro else 'white'
    plt.barh(estados, inseguranca, color='salmon')
    plt.xlabel('Moradias', color=cor_grafico)
    plt.ylabel('Estados', color=cor_grafico)
    plt.title('Distribuição de Moradias por Estado', color=cor_grafico)
    plt.gca().set_facecolor(cor_fundo)
    plt.gca().invert_yaxis()
    adicionar_botao_grafico()
    plt.show()

#função para gerar gráfico de pizza:
def gerar_grafico_pizza(estados, inseguranca):
    plt.figure(figsize=(8, 8))
    plt.pie(inseguranca, labels=estados, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Distribuição Proporcional de Moradias por Estado')
    adicionar_botao_grafico()
    plt.show()

#função para gerar gráfico de linhas:
def gerar_grafico_linhas(estados, inseguranca):
    plt.figure(figsize=(12, 8))
    cor_grafico = 'white' if modo_escuro else 'black'
    plt.plot(estados, inseguranca, marker='o', linestyle='-', color='orange')
    plt.xlabel('Estados', color=cor_grafico)
    plt.ylabel('Moradias', color=cor_grafico)
    plt.title('Evolução de Moradias por Estado', color=cor_grafico)
    adicionar_botao_grafico()
    plt.show()

#função para gerar gráfico de dispersão:
def gerar_grafico_dispersao(estados, inseguranca):
    plt.figure(figsize=(12, 8))
    cor_grafico = 'white' if modo_escuro else 'black'
    plt.scatter(estados, inseguranca, c=inseguranca, cmap='coolwarm', s=100)
    plt.xlabel('Estados', color=cor_grafico)
    plt.ylabel('Moradias', color=cor_grafico)
    plt.title('Dispersão de Moradias por Estado', color=cor_grafico)
    adicionar_botao_grafico()
    plt.show()

#função para adicionar um botão de alternar modo escuro no gráfico:
def adicionar_botao_grafico():
    ax_button = plt.axes([0.81, 0.01, 0.15, 0.05])
    botao_grafico = Button(ax_button, 'Modo Escuro' if not modo_escuro else 'Modo Claro')

    def alternar_modo_grafico(event):
        global modo_escuro
        modo_escuro = not modo_escuro
        
        #atualiza cores do gráfico:
        cor_grafico = 'white' if modo_escuro else 'black'
        cor_fundo = '#2E2E2E' if modo_escuro else 'white'
        plt.gca().set_facecolor(cor_fundo)
        plt.xlabel(plt.gca().get_xlabel(), color=cor_grafico)
        plt.ylabel(plt.gca().get_ylabel(), color=cor_grafico)
        plt.title(plt.gca().get_title(), color=cor_grafico)
        plt.draw()
        botao_grafico.on_clicked(alternar_modo_grafico)

#interface gráfica principal:
root = tk.Tk()
root.title('Leitor de Planilhas')
root.geometry('600x400')

#definindo cores iniciais
cor_fundo = 'white'
cor_botao = 'lightgray'
cor_texto = 'black'

#botão para alternar modo escuro:
btn_modo = tk.Button(root, text="Modo Escuro", command=alternar_modo, font=('Arial', 12), bg=cor_botao, fg=cor_texto)
btn_modo.pack(pady=10)

#selecionar o tipo de gráfico:
combo_grafico = tk.StringVar(value="Barras")
opcoes_grafico = tk.OptionMenu(root, combo_grafico, "Barras", "Pizza", "Linhas", "Dispersão")
opcoes_grafico.config(font=('Arial', 12), bg=cor_botao, fg=cor_texto)
opcoes_grafico.pack(pady=10)

#botão para gerar o gráfico selecionado:
btn_grafico = tk.Button(root, text="Gerar Gráfico", command=carregar_planilha, font=('Arial', 14), bg=cor_botao, fg=cor_texto)
btn_grafico.pack(pady=10)

#configurando a cor inicial do fundo:
root.configure(bg=cor_fundo)
root.mainloop()