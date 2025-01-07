from ape.Literal import Literal
from ape.Argument import Argument

class Attack:
    """
    Classe représentant une attaque entre deux arguments.
    """
    def __init__(self, attacker: Argument, attacked: Argument):
        """
        Constructeur de la classe Attack.

        :param attacker: L'argument attaquant.
        :param attacked: L'argument attaqué.
        """
        self.attacker:Argument = attacker
        self.attacked:Argument = attacked

    def __str__(self) -> str:
        """
        Méthode permettant d'afficher une attaque.

        :return: Une chaîne de caractères représentant l'attaque.
        """
        return f"{self.attacker} -> {self.attacked}"

    def __eq__(self, other: object) -> bool:
        """
        Méthode permettant de comparer deux attaques.
        :param other: L'attaque à comparer.
        :return: True si les attaques sont égales, False sinon.
        """
        if not isinstance(other, Attack):
            return False
        return self.attacker == other.attacker and self.attacked == other.attacked

    def __hash__(self) -> int:
        """
        Méthode permettant de hasher une attaque.
        :return: Le hash de l'attaque.
        """
        return hash((self.attacker, self.attacked))

class SetAttack(Attack):
    """
    Classe représentant une attaque normale entre deux set de litéraux
    
    """

    def __init__(self, attacker: set[Literal], attacked: set[Literal]):
        """
        Constructeur de la classe NormalAttack.

        :param attacker: L'ensemble attaquant.
        :param attacked: L'ensemble attaqué.
        """
        self.attacker:frozenset[Literal] = frozenset(attacker)
        self.attacked:frozenset[Literal] = frozenset(attacked)

    def __str__(self) -> str:
        """
        Méthode permettant d'afficher une attaque.

        :return: Une chaîne de caractères représentant l'attaque.
        """
        return f"({', '.join([str(lit) for lit in self.attacker])}) -> ({', '.join([str(lit) for lit in self.attacked])})"
    
    def __eq__(self, other: object) -> bool:
        """
        Méthode permettant de comparer deux attaques.
        :param other: L'attaque à comparer.
        :return: True si les attaques sont égales, False sinon.
        """
        if not isinstance(other, SetAttack):
            return False
        return self.attacker == other.attacker and self.attacked == other.attacked
    
    def __hash__(self) -> int:
        """
        Méthode permettant de hasher une attaque.
        :return: Le hash de l'attaque.
        """
        return hash((self.attacker, self.attacked))
