from State import State
from Transition import Transition
from Edge import Edge
from MT import MT
import re 
import tkinter as tk
from tkinter import filedialog
import time 
# Classe da interface
class Interface:
    def __init__(self):
        self.ribbon_size = 60
        self.root = tk.Tk()
        self.root.geometry("800x300")
        self.root.title("Simulador Machine Turing")
        self.root.config(background='white')
        self.root.resizable(False, False)

        self.numPassos = 0
        self.tape = list(range(self.ribbon_size))  # Lista que representa toda a fita (valores de 0 a 24)
        self.posMarcador = 0  # Posição inicial do marcador
        self.janela_inicio = 0  # Índice inicial da janela visível
        self.janela_tamanho = 20  # Quantidade de células visíveis
        self.cells = []  # Lista de células (tk.Entry)

        self.ultimoArquivo = None

        self.fita = None
    def carregarArquivo(self, novoArquivo = False):
        if(self.ultimoArquivo == None or novoArquivo == True):
            caminho_arquivo = filedialog.askopenfilename(title="Selecione um arquivo")
            self.ultimoArquivo  = caminho_arquivo
        else:
            caminho_arquivo = self.ultimoArquivo
        nomeArquivo = caminho_arquivo.split('/')
        nomeArquivo = nomeArquivo[-1]
        estados = {}
        transicoes = {}

        if caminho_arquivo:
            self.caminho_text.config(text=nomeArquivo)
            with open(caminho_arquivo, 'r') as arquivo:
                conteudo = arquivo.read()

            conteudo = re.split(r'[\n:]', conteudo)
            estadoFinal = conteudo[conteudo.index('Estado_Final') + 1]
            estadoInicial = conteudo[conteudo.index('Estado_Inicial') + 1]
            self.fita = conteudo[conteudo.index('Fita') + 1]  # Obtém a fita inicial
            instrucoes = conteudo[conteudo.index('# Instrucoes') + 1:]

            # Criar estados e transições
            estados[estadoFinal] = State(estadoFinal)
            estados[estadoFinal].setFinal()

            for infor in instrucoes:
                infor = infor.split(',')
                estadoAtual = infor[0]

                transicoes.setdefault(estadoAtual, []).append(infor[0:])

                if estadoAtual not in estados:
                    estados[estadoAtual] = State(estadoAtual)

            for chave in estados:
                if chave in transicoes:
                    transicoesChave = transicoes[chave]
                    for transicao in transicoesChave:
                        valorLido, proximoEstado, gravaNaFita, movimento = transicao[1:]
                        estados[chave].addTransition(estados[proximoEstado], valorLido, gravaNaFita, movimento)

            # Criar o objeto MT
            self.mt = MT(estados[estadoInicial], self.fita, self.ribbon_size)
            self.tape = list(self.mt.fita)  # Atualiza a fita da interface
            self.fita = self.tape.copy()
            self.posMarcador = self.mt.current  # Atualiza o marcador
            self.posMarcadorOrig = self.posMarcador
            self.button_start.config(state='normal')
            # Ajustar a posição da janela visível com base no marcador
            self.janela_inicio = self.posMarcador
            self.limparInterface()
    
    def limparInterface(self):
        self.tape = self.fita.copy() # Fita inicial
        self.posMarcador = self.posMarcadorOrig  # Posição inicial do marcador
        self.janela_inicio =  self.posMarcador
        self.status2.config(text=f'Lendo:')
        self.status3.config(text=f'Escrevendo:')
        self.status.config(text=f'Status de aceitação: ')
        self.frameRodaPe.config(background='white')
        for widget in self.frameRodaPe.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(background='white')
        self.centralizarMarcador()
        # Atualizar a interface
        self.desenharFita()

    def resetMT(self):
        """Reseta o MT e a interface para o estado inicial."""
        # Redefinir a fita e o marcador
        self.limparInterface()

        # Reativar os botões necessários
        self.button_start.config(state='normal')
        self.button_stop.config(state='disabled')
        self.button_reset.config(state='disabled')

    def stopMT(self):
        self.stopStatus = True
        self.button_stop.config(state='disabled')
    def runMT(self):
        self.numPassos = 0
        self.button_stop.config(state='normal')
        self.button_start.config(state='disabled')
        
        self.mt.run()
        self.movimentos = self.mt.movimentacao
        self.referencia = 0
        self.stopStatus = False
        
        for i in self.movimentos:
            if(self.stopStatus == True):
                self.stopStatus = False
                break
            if(i == '<'):
                self.moverMarcador(-1)
                self.status2.config(text=f'Lendo: {self.tape[self.posMarcador]}')
            elif(i == '>'):
                self.moverMarcador(1)
                self.status2.config(text=f'Lendo: {self.tape[self.posMarcador]}')
            else:
                self.tape[self.posMarcador] = i
                self.status2.config(text=f'Lendo: {self.tape[self.posMarcador]}')
                self.status3.config(text=f'Escrevendo: {self.tape[self.posMarcador]}')
            self.status4.config(text=f'Numero de passos: {self.numPassos}')
            self.status5.config(text=f'Numero de 1s: {self.tape.count('1')}')
            self.referencia += 1
            self.desenharFita()  # Atualiza visualmente a fita
            self.root.update()  # Atualiza a interface gráfica
            time.sleep(0.15)  # Pausa para simular a execução passo a passo
        if(self.referencia == len(self.movimentos)):
            if(self.mt.status == True):
                self.status.config(text=f'Status de aceitação: Valido ✅')
                self.frameRodaPe.config(background='#9cf7a2')
                for widget in self.frameRodaPe.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(background='#9cf7a2')
            else:
                self.status.config(text=f'Status de aceitação: Invalido ❌')
                self.frameRodaPe.config(background='red')
                for widget in self.frameRodaPe.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(background='red')
        self.button_reset.config(state='normal')
        self.button_stop.config(state='disabled')
    def desenharFita(self):
        """Desenha a fita fixa de acordo com a janela atual."""

        # Se as células já existirem, apenas atualize seus valores
        if self.cells:
            for i, cell in enumerate(self.cells):
                cell.configure(state="normal")
                indice_real = self.janela_inicio + i  # Índice real no self.tape
                cell.delete(0, tk.END)
                if indice_real < len(self.tape):
                    cell.insert(0, self.tape[indice_real])
                    # cell.insert(0, self.tape[indice_real])

                # Destacar a célula do marcador
                if indice_real == self.posMarcador:
                    cell.config(highlightbackground="red", highlightcolor="red", highlightthickness=3)
                else:
                    cell.config(highlightbackground="white", highlightcolor="white", highlightthickness=1)
                cell.configure(state="readonly")  # Bloquear novamente
        else:
            # Criar as células apenas uma vez
            self.tape_frame = tk.Frame(self.root)
            self.tape_frame.pack(pady=10)

            for i in range(self.janela_tamanho):
                cell = tk.Entry(self.tape_frame, width=2, justify="center", font=("Arial", 18))
                cell.grid(row=0, column=i, padx=5)
                self.cells.append(cell)

            # Chamar a função para atualizar os valores na janela inicial
            self.desenharFita()

    def moverFita(self, direcao):
        """Move a fita para a esquerda (-1) ou direita (+1)."""

        # Calcula o novo índice inicial da janela
        novo_inicio = self.janela_inicio + direcao

        # Garante que o índice não ultrapasse os limites da fita
        if 0 <= novo_inicio <= len(self.tape) - self.janela_tamanho:
            self.janela_inicio = novo_inicio
            self.desenharFita()

    def moverMarcador(self, direcao):
        """Move o marcador para a esquerda (-1) ou direita (+1)."""
        nova_pos = self.posMarcador + direcao
        self.numPassos += 1
        # Garante que o marcador não ultrapasse os limites da fita
        if 0 <= nova_pos < len(self.tape):
            self.posMarcador = nova_pos

            # Se o marcador sair da janela visível, move a fita automaticamente
            if self.posMarcador < self.janela_inicio:
                self.janela_inicio -= 1
            elif self.posMarcador >= self.janela_inicio + self.janela_tamanho - 1:
                self.janela_inicio += 1

            self.desenharFita()
        
    def centralizarMarcador(self):
        """Ajusta a janela para garantir que o marcador fique visível ao iniciar."""
        # Se o marcador estiver fora da janela inicial, reposiciona a janela
        if self.posMarcador < self.janela_inicio:
            self.janela_inicio = max(0, self.posMarcador)
        elif self.posMarcador > self.janela_inicio + self.janela_tamanho:
            self.janela_inicio = max(0, self.posMarcador - self.janela_tamanho + 2)

    def desenharTelaPrincipal(self):
        """Desenha a interface principal."""
        self.tape_frame = tk.Frame(self.root)
        self.tape_frame.pack(side=tk.TOP, pady=10)
        # Garantir que o marcador fique visível na inicialização
        self.centralizarMarcador()
        # Frame para os botões de controle
        frameControles = tk.Frame(self.root)
        frameControles.pack(side=tk.TOP, fill=tk.X, pady=10)
        frameControles.config(background="white")
        # Botões de controle
        # botao_carregar_arquivo = tk.Button(frameControles, text="Carregar arquivo", command=lambda: self.carregarArquivo(),height=2)
        # botao_carregar_arquivo.pack(side=tk.LEFT, padx=5)

        self.button_start = tk.Button(frameControles, text="  >>> \n RUN",
                         height=2,
                         width=7,
                         font=('Arial', 8, 'bold'),
                         background='#f98927',
                         foreground='WHITE',
                         activebackground='#915001',
                         activeforeground='WHITE',
                         highlightthickness=2,
                         highlightbackground='#f98927',
                         highlightcolor='WHITE',
                         border=0,
                         state='disabled',
                         cursor='hand1',
                         command=lambda: self.runMT())

        # Usando lambda para alterar a cor ao passar o mouse
        self.button_start.pack(side=tk.LEFT, padx=5)
        self.button_start.bind("<Enter>", lambda event: self.button_start.config(background='#f7b668', foreground='WHITE'))
        self.button_start.bind("<Leave>", lambda event: self.button_start.config(background='#f98927', foreground='WHITE'))
        self.button_start.bind("<Button-1>", lambda event: self.button_start.config(background='#915001', foreground='WHITE')) # command=lambda: self.moverMarcador(1)"""
        

        self.button_stop = tk.Button(frameControles, text="  ⏸ \n STOP",  # Quebra de linha
                       height=2,  # Aumentando a altura para acomodar a quebra
                       width=9,
                       font=('Arial', 8, 'bold'),
                       background='red',  # Cor de fundo vermelha
                       foreground='white',  # Cor da fonte branca
                       activebackground='#d32f2f',  # Cor de fundo ativa, um tom de vermelho mais escuro
                       activeforeground='white',  # Cor da fonte ativa
                       highlightthickness=2,
                       highlightbackground='red',
                       highlightcolor='white',
                       border=0,
                       cursor='hand1',
                       state='disabled',
                       disabledforeground="gray",
                       command=lambda: self.stopMT()) # command=lambda: self.moverMarcador(1)"""
        
        self.button_stop.pack(side=tk.LEFT, padx=5)
        self.button_stop.bind("<Enter>", lambda event: self.button_stop.config(background='#f56c62', foreground='WHITE'))
        self.button_stop.bind("<Leave>", lambda event: self.button_stop.config(background='red', foreground='WHITE'))
        self.button_stop.bind("<Button-1>", lambda event: self.button_stop.config(background='#d32f2f', foreground='WHITE')) # """
        


        self.button_reset = tk.Button(frameControles, text="🔄 \n RESET",height=2,width=9,font=('Arial',8,'bold'),command=lambda: self.resetMT(),
                                        background='#2574f5',  # Cor de fundo vermelha
                                        foreground='white',  # Cor da fonte branca
                                        activebackground='#0a1efa',  # Cor de fundo ativa, um tom de vermelho mais escuro
                                        activeforeground='white',  # Cor da fonte ativa
                                        highlightthickness=2,
                                        highlightbackground='#2574f5',
                                        highlightcolor='white',
                                        border=0,
                                        cursor='hand1',
                                        state='disabled',
                                        disabledforeground="gray") # command=lambda: self.moverMarcador(1)"""
        self.button_reset.pack(side=tk.LEFT, padx=5)
        self.button_reset.bind("<Enter>", lambda event: self.button_reset.config(background='#0247f5', foreground='WHITE'))
        self.button_reset.bind("<Leave>", lambda event: self.button_reset.config(background='#2574f5', foreground='WHITE'))
        self.button_reset.bind("<Button-1>", lambda event: self.button_reset.config(background='#0247f5', foreground='WHITE')) # """

        self.caminho_text = tk.Label(frameControles,text="Selecionar o arquivo",background='white',bd=1,relief='solid',pady=7)
        self.caminho_text.pack(side=tk.LEFT,fill=tk.X,expand=True)
        self.caminho_text.bind("<Button-1>", lambda event: self.carregarArquivo(novoArquivo=True))
        
        self.button_reload = tk.Button(frameControles, text="🔄 \n RELOAD",height=2,width=9,font=('Arial',8,'bold'),command=lambda: self.carregarArquivo(),
                                        background='#c4c4c0',  # Cor de fundo vermelha
                                        foreground='white',  # Cor da fonte branca
                                        activebackground='#0a1efa',  # Cor de fundo ativa, um tom de vermelho mais escuro
                                        activeforeground='white',  # Cor da fonte ativa
                                        highlightthickness=2,
                                        highlightbackground='#c4c4c0',
                                        highlightcolor='white',
                                        border=0,
                                        cursor='hand1',
                                        state='normal',
                                        disabledforeground="gray") # command=lambda: self.moverMarcador(1)"""
        self.button_reload.pack(side=tk.LEFT, padx=5)
        # Frame para carregar arquivo
        # frame_arquivo_controle = tk.Frame(self.root,background='white')
        # frame_arquivo_controle.pack(side=tk.TOP, pady=10)

        # Frame para a fita
        
        # Inicializa a fita
        self.desenharFita()
        self.frameRodaPe = tk.Frame(self.root, background='white')
        self.frameRodaPe.pack(side=tk.BOTTOM, fill=tk.X)
        self.frameRodaPe.option_add("*Background", "white")

        # Configurar as colunas para ter um espaçamento maior
        self.frameRodaPe.columnconfigure(0, weight=1)
        self.frameRodaPe.columnconfigure(1, weight=1)
        self.frameRodaPe.columnconfigure(2, weight=1)

        self.status = tk.Label(self.frameRodaPe, text="Status de aceitação: ")
        self.status.grid(row=0, column=0, padx=50, pady=5, sticky="w")

        self.status2 = tk.Label(self.frameRodaPe, text="Lendo: ")
        self.status2.grid(row=0, column=1, padx=50, pady=5, sticky="w")

        self.status3 = tk.Label(self.frameRodaPe, text="Escrevendo: ")
        self.status3.grid(row=0, column=2, padx=50, pady=5, sticky="w")

        self.status4 = tk.Label(self.frameRodaPe, text="Número de passos: ")
        self.status4.grid(row=1, column=0, padx=50, pady=10, sticky="w")  

        self.status5 = tk.Label(self.frameRodaPe, text="Número de 1s: ")
        self.status5.grid(row=1, column=1, padx=50, pady=10, sticky="w")  
        self.root.mainloop()


# Testando a interface com o marcador em uma posição inicial fora da janela visível

