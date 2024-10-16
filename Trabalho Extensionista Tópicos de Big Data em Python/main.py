#bibliotecas:
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#variáveis globais para salvar o estado do modo escuro e do canvas:
modo_escuro = False
canvas = None 
mouse_press = False 
mouse_start_x = 0
mouse_start_y = 0

#função para alternar entre modo escuro no menú inicial:
def alternar_modo():
    global modo_escuro
    modo_escuro = not modo_escuro

    if modo_escuro:
        root.configure(bg='#2E2E2E')
        btn_selecionar.configure(bg='#424242', fg='white')
        btn_modo.configure(bg='#424242', fg='white', text='Modo Claro')
        btn_reset.configure(bg='#424242', fg='white')
        btn_personalizar.configure(bg='#424242', fg='white')
    else:
        root.configure(bg='white')
        btn_selecionar.configure(bg='lightgray', fg='black')
        btn_modo.configure(bg='lightgray', fg='black', text='Modo Escuro')
        btn_reset.configure(bg='lightgray', fg='black')
        btn_personalizar.configure(bg='lightgray', fg='black')

#função para abrir o arquivo e carregar os dados:
def carregar_planilha():
    arquivo = filedialog.askopenfilename(filetypes=[("Planilhas Excel", "*.xlsx"), ("CSV Files", "*.csv")])
    if arquivo:
        try:
            if arquivo.endswith('.xlsx'):
                dados = pd.read_excel(arquivo)
            else:
                dados = pd.read_csv(arquivo)

            print(dados.head())

            if 'Estados' in dados.columns and 'Moradias' in dados.columns:
                array_estados = np.array(dados['Estados'])
                array_inseguranca = np.array(dados['Moradias'])
                tipo_grafico = combo_grafico.get()
                print(f"Tipo de gráfico selecionado: {tipo_grafico}")
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

#função para recriar e redesenhar o gráfico quando alternar modo:
def redesenhar_grafico(fig, ax, estados, inseguranca, tipo_grafico):
    ax.clear()
    cor_grafico = 'white' if modo_escuro else 'black'
    cor_fundo = '#2E2E2E' if modo_escuro else 'white'

    if tipo_grafico == "Barras":
        ax.barh(estados, inseguranca, color='salmon')
        ax.set_xlabel('Moradias', color=cor_grafico)
        ax.set_ylabel('Estados', color=cor_grafico)
        ax.set_title('Distribuição de Moradias por Estado', color=cor_grafico)
        ax.tick_params(axis='y', labelsize=10)
    elif tipo_grafico == "Pizza":
        ax.pie(inseguranca, labels=estados, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
        ax.set_title('Distribuição Proporcional de Moradias por Estado', color=cor_grafico)
    elif tipo_grafico == "Linhas":
        ax.plot(estados, inseguranca, marker='o', linestyle='-', color='orange')
        ax.set_xlabel('Estados', color=cor_grafico)
        ax.set_ylabel('Moradias', color=cor_grafico)
        ax.set_title('Evolução de Moradias por Estado', color=cor_grafico)
        ax.tick_params(axis='x', labelsize=10)
    else:
        ax.scatter(estados, inseguranca, c=inseguranca, cmap='coolwarm', s=100)
        ax.set_xlabel('Estados', color=cor_grafico)
        ax.set_ylabel('Moradias', color=cor_grafico)
        ax.set_title('Dispersão de Moradias por Estado', color=cor_grafico)
        ax.set_facecolor(cor_fundo)
        fig.canvas.draw()

#função para gerar gráfico de barras com os estados:
def gerar_grafico_barras(estados, inseguranca):
    print("Gerando gráfico de barras...")
    fig, ax = plt.subplots(figsize=(10, 6)) 
    desenhar_canvas(fig)
    redesenhar_grafico(fig, ax, estados, inseguranca, "Barras")

#função para gerar gráfico de pizza:
def gerar_grafico_pizza(estados, inseguranca):
    print("Gerando gráfico de pizza...") 
    fig, ax = plt.subplots(figsize=(8, 8))
    desenhar_canvas(fig)
    redesenhar_grafico(fig, ax, estados, inseguranca, "Pizza")

#função para gerar gráfico de linhas:
def gerar_grafico_linhas(estados, inseguranca):
    print("Gerando gráfico de linhas...")  
    fig, ax = plt.subplots(figsize=(10, 6))
    desenhar_canvas(fig)
    redesenhar_grafico(fig, ax, estados, inseguranca, "Linhas")

#função para gerar gráfico de dispersão:
def gerar_grafico_dispersao(estados, inseguranca):
    print("Gerando gráfico de dispersão...")
    fig, ax = plt.subplots(figsize=(10, 6))
    desenhar_canvas(fig)
    redesenhar_grafico(fig, ax, estados, inseguranca, "Dispersão")

#função para desenhar o gráfico no canvas do tkinter:
def desenhar_canvas(fig):
    global canvas
    try:
        if canvas:
            canvas.get_tk_widget().pack_forget()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.get_tk_widget().bind("<ButtonPress-1>", on_mouse_press)
            canvas.get_tk_widget().bind("<B1-Motion>", on_mouse_drag)
            canvas.get_tk_widget().bind("<ButtonRelease-1>", on_mouse_release)
    except Exception as e:
        print(f"Erro ao desenhar o gráfico: {e}")

#funções para mover o gráfico:
def on_mouse_press(event):
    global mouse_press, mouse_start_x, mouse_start_y
    mouse_press = True
    mouse_start_x = event.x
    mouse_start_y = event.y

def on_mouse_drag(event):
    global mouse_press
    if mouse_press:
        dx = event.x - mouse_start_x
        dy = event.y - mouse_start_y
        widget = canvas.get_tk_widget()
        x = widget.winfo_x() + dx
        y = widget.winfo_y() + dy
        widget.place(x=x, y=y)

#mudança na função do mouse:
def on_mouse_release(event):
    global mouse_press
    mouse_press = False

#função para resetar o gráfico atual:
def resetar_grafico():
    global canvas
    if canvas:
        canvas.get_tk_widget().pack_forget()
        canvas = None

#função para personalizar o gráfico:
def personalizar_grafico():
    if canvas:
        janela_personalizar = tk.Toplevel(root)
        janela_personalizar.title("Personalizar Gráfico")
        tk.Label(janela_personalizar, text="Título:").pack(pady=5)
        titulo_var = tk.StringVar(value=canvas.figure.axes[0].get_title())
        tk.Entry(janela_personalizar, textvariable=titulo_var).pack(pady=5)
        tk.Label(janela_personalizar, text="Largura do Gráfico:").pack(pady=5)
        largura_var = tk.DoubleVar(value=10.0)
        tk.Entry(janela_personalizar, textvariable=largura_var).pack(pady=5)
        tk.Label(janela_personalizar, text="Altura do Gráfico:").pack(pady=5)
        altura_var = tk.DoubleVar(value=6.0)
        tk.Entry(janela_personalizar, textvariable=altura_var).pack(pady=5)

        def aplicar_personalizacoes():
            novo_titulo = titulo_var.get()
            largura = largura_var.get()
            altura = altura_var.get()
            canvas.figure.set_size_inches(largura, altura)
            for ax in canvas.figure.axes:
                ax.set_title(novo_titulo)
                canvas.draw()
                janela_personalizar.destroy()
            tk.Button(janela_personalizar, text="Aplicar", command=aplicar_personalizacoes).pack(pady=10)

#configurações da janela principal:
root = tk.Tk()
root.title("Visualização de Dados")
cor_fundo = 'white'
cor_botao = 'lightgray'
cor_texto = 'black'

#botão para selecionar planilha:
btn_selecionar = tk.Button(root, text="Selecionar Planilha", command=carregar_planilha, font=('Arial', 14),
bg=cor_botao, fg=cor_texto)
btn_selecionar.pack(pady=10)

#botão para alternar modo escuro:
btn_modo = tk.Button(root, text="Modo Escuro", command=alternar_modo, font=('Arial', 12), 
bg=cor_botao, fg=cor_texto)
btn_modo.pack(pady=10)

#botão para resetar o gráfico:
btn_reset = tk.Button(root, text="Resetar Gráfico", command=resetar_grafico, font=('Arial', 12), 
bg=cor_botao, fg=cor_texto)
btn_reset.pack(pady=10)

#botão para personalizar o gráfico:
btn_personalizar = tk.Button(root, text="Personalizar Gráfico", command=personalizar_grafico, font=('Arial', 12),
bg=cor_botao, fg=cor_texto)
btn_personalizar.pack(pady=10)

#combo para selecionar tipo de gráfico:
tipos_graficos = ["Barras", "Pizza", "Linhas", "Dispersão"]
combo_grafico = tk.StringVar(value="Barras")
drop_grafico = tk.OptionMenu(root, combo_grafico, *tipos_graficos)
drop_grafico.pack(pady=10)

#configurando a cor inicial do fundo:
root.configure(bg=cor_fundo)
root.mainloop()
