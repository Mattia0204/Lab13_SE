from dataclasses import dataclass

@dataclass
class Interazione:
    id_gene1: str
    id_gene2: str
    tipo: str
    correlazione: float

    def __eq__(self, other):
        return isinstance(other, Interazione) and self.id_gene1 == other.id_gene1 and self.id_gene2 == other.id_gene2

    def __str__(self):
        return f"{self.id_gene1} {self.id_gene2}"

    def __repr__(self):
        return f"{self.id_gene1} {self.id_gene2}"