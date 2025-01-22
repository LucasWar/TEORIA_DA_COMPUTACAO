from State import State
class AFD: #AFD = (Q, Σ, δ, q0, F)
    def __init__(self, q: State, w: str, _range: int):
        self.q = q
        self.w = w

        self.movimentacao = []

        #Ideia para Turing Machine abaixo:
        self.set_fita(_range)
        self.init_fita(w)

        self.status = None
    def run(self):
        if(self.q==None or self.w==None): return False
        # for c in self.fita[self.current]:
        # transition = self.q.transition(self.fita[self.current])
        while True:
            transition = self.q.transition(self.fita[self.current])
            if transition != None:
                qNext = transition.getState()
                self.move_current(transition.getDirection(),transition.getWrite())
                print(f'{self.q.getName()} ({self.fita[self.current]}) -> {qNext.getName()}')
                self.q = qNext
                
            else:
                # print(self.q.isFinal)
                # print(f'{self.fita[self.current]} nao pertence ao alfabeto ou nao possui transicao!!')
                # print(self.fita)
                return self.print_result()
    
    def print_result(self):
        """ Print and Return True (ok) or False (no ok)"""
        if(self.q.isFinal):
            self.status = True
            print(f'reconheceu: {self.w}')
            print(self.fita)
        else:
            print(f'Não reconheceu: {self.w}')
            print(self.fita)
            self.status = False
        return self.q.isFinal

    #Ideia para Turing Machine abaixo:
    def init_fita(self, w):
        for a in list(w):
            self.fita[self.current] = a
            self.current += 1
        
        self.current = self.range+1
        #print(f'{self.fita}\nLEN: {len(self.fita)}\nMAX: {self.max}')
        #print(f'current -> {self.fita[self.current]}')
    
    def set_fita(self, _range):
        self.fita = []
        self.range = _range
        self.max = self.range*2

        self.fita.append('#')
        for i in range(1, self.max+2):
            self.fita.append('_')
        
        self.current = self.range+1
        self.max = self.max+1
    
    def move_current(self,direction,write): 
        if(write != None):
            self.fita[self.current] = write
            self.movimentacao.append(write)
        if(direction == '<'):
            self.current -= 1
            self.movimentacao.append('<')
        elif(direction == '>'):
            self.current += 1
            self.movimentacao.append('>')

        