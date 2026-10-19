class UnionFind:
    def __init__(self, n=0):
        self.parent = []
        self.rank = []
        self.tam = []
        self.conjuntos = 0
        for i in range(n):
            self.makeSet()

    def makeSet(self):
        x = len(self.parent)
        self.parent.append(x)
        self.rank.append(0)
        self.tam.append(1)
        self.conjuntos += 1
        return x

    def find(self, x):
        raiz = x
        while self.parent[raiz] != raiz:
            raiz = self.parent[raiz]
        while self.parent[x] != raiz:
            siguiente = self.parent[x]
            self.parent[x] = raiz
            x = siguiente
        return raiz

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.tam[ra] += self.tam[rb]
        self.conjuntos -= 1
        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)

    def count(self):
        return self.conjuntos

    def size(self, x):
        return self.tam[self.find(x)]

    def grupos(self):
        por_raiz = {}
        for x in range(len(self.parent)):
            raiz = self.find(x)
            if raiz not in por_raiz:
                por_raiz[raiz] = []
            por_raiz[raiz].append(x)
        return list(por_raiz.values())

    def __str__(self):
        return f"parent={self.parent}"
