from dataclasses import dataclass

@dataclass
class Classificazione:
    id_gene: str
    localizzazione: str


    def __eq__(self, other):
        return isinstance(other, Classificazione) and self.id == other.id

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"{self.id}"