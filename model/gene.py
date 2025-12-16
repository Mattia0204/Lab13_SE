from dataclasses import dataclass

@dataclass
class Gene:
    id: str
    funzione: str
    essenziale: str
    cromosoma: int

    def __eq__(self, other):
        return isinstance(other, Gene) and self.id == other.id

    def __str__(self):
        return f"{self.id}"

    def __repr__(self):
        return f"{self.id}"