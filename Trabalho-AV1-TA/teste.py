import tkinter as tk
from tkinter import messagebox

class TuringMachineSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")

        # Configuração inicial
        self.tape = [""] * 11
        self.head_position = 5
        self.state = "q0"

        # Criação da interface
        self.create_widgets()

    def create_widgets(self):
        # Frame da fita
        self.tape_frame = tk.Frame(self.root)
        self.tape_frame.pack(pady=10)

        self.cells = []
        for i in range(len(self.tape)):
            cell = tk.Entry(self.tape_frame, width=2, justify="center", font=("Arial", 18))
            cell.grid(row=0, column=i, padx=5)
            self.cells.append(cell)

        # Destacar célula inicial
        self.update_tape_display()

        # Botões de controle
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=10)

        self.reset_button = tk.Button(self.controls_frame, text="RESET", command=self.reset, bg="orange")
        self.reset_button.grid(row=0, column=0, padx=10)

        self.step_button = tk.Button(self.controls_frame, text="STEP", command=self.step, bg="skyblue")
        self.step_button.grid(row=0, column=1, padx=10)

        self.run_button = tk.Button(self.controls_frame, text="RUN", command=self.run, bg="lightgray")
        self.run_button.grid(row=0, column=2, padx=10)

    def update_tape_display(self):
        for i, value in enumerate(self.tape):
            self.cells[i].delete(0, tk.END)
            self.cells[i].insert(0, value if value else "")

        # Atualizar o destaque do cabeçote
        for i, cell in enumerate(self.cells):
            if i == self.head_position:
                cell.config(highlightbackground="yellow", highlightcolor="yellow", highlightthickness=2)
            else:
                cell.config(highlightthickness=0)

    def reset(self):
        self.tape = [""] * 11
        self.head_position = 5
        self.state = "q0"
        self.update_tape_display()

    def step(self):
        # Simulação de uma transição simples da MT (apenas exemplo)
        current_value = self.tape[self.head_position]

        if self.state == "q0":
            if current_value == "1":
                self.tape[self.head_position] = "0"
                self.state = "q1"
                self.head_position += 1
            elif current_value == "":
                self.tape[self.head_position] = "1"
                self.head_position -= 1
        elif self.state == "q1":
            if current_value == "0":
                self.tape[self.head_position] = "1"
                self.state = "q0"
                self.head_position -= 1

        # Garantir que o cabeçote não saia dos limites
        self.head_position = max(0, min(self.head_position, len(self.tape) - 1))

        self.update_tape_display()

    def run(self):
        messagebox.showinfo("Run", "Execução completa simulada!")

# Criar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = TuringMachineSimulator(root)
    root.mainloop()
