class Edge:
    def __init__(self, c: str):
        self.c = c

    def getC(self): return self.c

    @staticmethod
    def instance(c: str):
        return Edge(c)
    
    def equals(self, o):
        if isinstance(o, Edge):
            return Edge.testAB(self.c, o.getC())
        return False

    def __repr__(self):
        return f'[{self.c}]'
    
    @staticmethod
    def testAB(a: str, b: str):
        return a==b
    