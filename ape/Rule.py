"""
Ce fichier représentes les règles

"""
from ape.Literal import Literal

class Rule:
    """
    Cette classe représente les règles
    """
    def __init__(self, head: Literal, body: set[Literal] = None) -> None:
        self.head: Literal = head
        self.body: set[Literal] = body if body is not None else set()
        self.is_fact: bool = False

    def __str__(self) -> str:
        return f"{self.head} ← ({', '.join(map(str, self.body))})"

    def __eq__(self, other:object) -> bool:
        return self.head == other.head and self.body == other.body

    def __hash__(self) -> int:
        return hash((self.head, frozenset(self.body)))

    def __repr__(self) -> str:
        return str(self)

    def set_head(self, lit:Literal) -> None:
        """
        Cette méthode permet de définir la tête de la règle

        :param lit: le littéral qui sera la tête de la règle
        """
        self.head = lit

    def add_body(self, lit:Literal) -> None:
        """
        Cette méthode permet d'ajouter un littéral au corps de la règle

        :param lit: le littéral à ajouter
        """
        self.body.add(lit)

    def set_body(self, body:set[Literal]) -> None:
        """
        Cette méthode permet de definir le corps de la règle

        :param body: le nouveau corps de la règle
        """
        self.body = body

    def get_head(self) -> Literal:
        """
        Cette méthode permet de retourner la tête de la règle

        :return: la tête de la règle
        """
        return self.head

    def get_body(self) -> set[Literal]:
        """
        Cette méthode permet de retourner le corps de la règle

        :return: le corps de la règle
        """
        return self.body
