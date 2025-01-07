"""
Ce fichier représente les littéraux
"""
class Literal:
    """
    Representation d'un litéral :
    - name : le nom du litéral (souvent une lettre en maj)
    - is_negated : booléen qui indique si le litéral est négatif
    """
    def __init__(self, name:str, is_negated:bool=False):
        self.name: str = name
        self.is_negated:bool = is_negated

    def __str__(self)->str:
        return f"{'¬' if self.is_negated else ''}{self.name}"

    def __eq__(self, other:object)->bool:
        return self.name == other.name and self.is_negated == other.is_negated

    def __hash__(self)->int:
        return hash(str(self))

    def __repr__(self)->str:
        return str(self)
    