"""
Ce fichier est une implémentation d'un argument
Besoin de la classe Literal

@author: KOMLENOVIC Emilien, SEN Aburrahman, MARREL Pierre-Emmanuel
"""
from ape.Literal import Literal

class Argument:
    """
    Représentation d'un argument :
    - name : nom de l'argument (souvent : Arg1, Arg2)
    - leaves : ensemble des prémisses de l'argument (sous forme de __littéraux__)
    - claim : conclusion de l'argument (sous forme de __littéral__)
    """

    def __init__(self, claim:Literal, name:str = None, leaves:set[Literal] = None):
        self.name:str = name
        self.leaves:set[Literal] = leaves if leaves is not None else []
        self.claim:Literal = claim

    def __str__(self) -> str:
        return f"{self.name} : " + "{" + ', '.join(map(str, self.leaves)) + "}" + f" ⊢ {self.claim}"

    def __eq__(self, other:object) -> bool:
        return self.leaves == other.leaves and self.claim == other.claim

    def __hash__(self) -> int:
        return hash(str(self.leaves) + str(self.claim))

    def __repr__(self) -> str:
        return str(self)
