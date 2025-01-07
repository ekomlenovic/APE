"""
Ce fichier représente les "contraries"

@author: KOMLENOVIC Emilien, SEN Aburrahman, MARREL Pierre-Emmanuel
"""

from ape.Literal import Literal

class Contrary:
    """
    Représentation de la notion de "contrary" :
    - target : cible du "contrary"
    - attacker : attaquant du "contrary"
    """
    def __init__(self, target:Literal, attacker:Literal):
        self.target = target
        self.attacker = attacker

    def __str__(self) -> str:
        return str(self.target) + '\u0304' + f" = {self.attacker}"

    def __eq__(self, other:object) -> bool:
        return self.target == other.target and self.attacker == other.attacker

    def __hash__(self) -> int:
        return hash(str(self))

    def __repr__(self) -> str:
        return str(self)

    def get_target(self) -> Literal:
        """
        Cette méthode permet de retourner la cible de la règle
        
        :return: la cible de la règle
        """
        return self.target

    def get_attacker(self) -> Literal:
        """
        Cette méthode permet de retourner l'attaquant de la règle
        
        :return: l'attaquant de la règle
        """
        return self.attacker
    
    def set_target(self, target:Literal) -> None:
        """
        Cette méthode permet de définir la cible de la règle
        
        :param target: la cible de la règle
        """
        self.target = target

    def set_attacker(self, attacker:Literal) -> None:
        """
        Cette méthode permet de définir l'attaquant de la règle
        
        :param attacker: l'attaquant de la règle
        """
        self.attacker = attacker
