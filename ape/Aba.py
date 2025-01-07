"""
Impléementation de la classe Aba

@author: KOMLENOVIC Emilien, SEN Aburrahman, MARREL Pierre-Emmanuel
"""
from itertools import combinations
from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Argument import Argument
from ape.Attacks import Attack, SetAttack

class Aba:
    """
    Représentation d'un système Aba :
    - name : nom du système
    - language : ensemble des littéraux du système
    - rules : ensemble des règles du système
    
    """
    def __init__(self, name:str=None,
                language:set[Literal]=None,
                rules:set[Rule]=None,
                assumptions:set[Literal]=None,
                contraries:set[Contrary]=None,
                preferences:dict[Literal, set[Literal]]=None) -> None:
        self.name:str = name if name is not None else "aba"
        self.language:set[Literal] = language if language is not None else set()
        self.rules:set[Rule] = rules if rules is not None else set()
        self.assumptions:set[Literal] = assumptions if assumptions is not None else set()
        self.contraries:set[Contrary] = contraries if contraries is not None else set()
        self.arguments:set[Argument] = set()
        self.normal_attacks:set[SetAttack] = set ()
        self.reverse_attacks:set[SetAttack] = set ()
        self.attacks:set[Attack] = set()
        self.preferences:dict[Literal, set[Literal]] = preferences if preferences is not None else{}

    def __str__(self) -> str:
        return f"{self.name} : \n\
    L: {', '.join(map(str, self.language))}\n\
    R: {', '.join(map(str, self.rules))}\n\
    A: {', '.join(map(str, self.assumptions))}\n\
    C: {', '.join(map(str, self.contraries))}\n\
    PREF: {', '.join(f'{k} > {v}' for k, v in self.preferences.items())}\n\
    ARGS: {', '.join(map(str, self.arguments))},\n\
    ATKS: {', '.join(map(str, self.attacks))},\n\
    NORM_ATKS: {'; '.join(map(str, self.normal_attacks))}\n\
    REV_ATKS: {'; '.join(map(str, self.reverse_attacks))}\n"

    def __repr__(self) -> str:
        return f"{self.name} :\
L: {', '.join(map(str, self.language))}\
R: {', '.join(map(str, self.rules))}\
A: {', '.join(map(str, self.assumptions))}\
C: {', '.join(map(str, self.contraries))},\
PREF: {', '.join(f'{k} > {v}' for k, v in self.preferences.items())},\
ARGS: {', '.join(map(str, self.arguments))},\
ATKS: {', '.join(map(str, self.attacks))},\
NORM_ATKS: {', '.join(map(str, self.normal_attacks))},\
REV_ATKS: {', '.join(map(str, self.reverse_attacks))}"

    def __eq__(self, other:object) -> bool:
        return self.name == other.name and\
            self.language == other.language and\
            self.rules == other.rules and\
            self.assumptions == other.assumptions and\
            self.contraries == other.contraries

    def get_arg_by_claim(self, claim:Literal) -> Argument:
        """
        Permet de récupérer un argument en fonction de sa claim

        :param claim: la claim de l'argument
        :return: l'argument, si il existe, None sinon
        """
        return next((arg for arg in self.arguments if arg.claim == claim), None)

    def get_all_args_by_claim(self, claim:Literal) -> set[Argument]:
        """
        Permet de récupérer tous les arguments en fonction de leur claim

        :param claim: la claim des arguments
        :return: l'ensemble des arguments, si il existe, {} sinon
        """
        return {arg for arg in self.arguments if arg.claim == claim}

    def generate_arguments(self):
        """
        Génère les arguments du système
        """
        for assumption in self.assumptions:
            argument = Argument(name="A" + str(len(self.arguments) + 1),
                                leaves={assumption}, claim=assumption)
            if argument not in self.arguments:
                self.arguments.add(argument)
        for rule in self.rules:
            leaves = set()
            stack = list(rule.body)
            while stack:
                literal = stack.pop()
                if literal in self.assumptions:
                    leaves.add(literal)
                else:
                    for r in self.rules:
                        if r.head == literal:
                            stack.extend(r.body)
            argument = Argument(name="A" + str(len(self.arguments) + 1),
                                leaves=leaves, claim=rule.head)
            if argument not in self.arguments:
                self.arguments.add(argument)

    def generate_attacks(self):
        """
        Génère les attaques du système
        """
        for arg1 in self.arguments:
            for arg2 in self.arguments:
                if any(contrary.attacker == arg1.claim
                       for contrary in self.contraries if contrary.target in arg2.leaves):
                    self.attacks.add(Attack(attacker=arg1, attacked=arg2))


    def generate_aba_framework(self):
        """
        Permet de générer plus d'infos sur l'aba :
        - arguments
        - attacks
        """
        self.generate_arguments()
        self.generate_attacks()

    def __hash__(self) -> int:
        return hash(str(self))

    def set_name(self, name:str) -> None:
        """
        Cette méthode permet de définir le nom du système

        :param name: le nom du système
        """
        self.name = name

    def add_literal(self, lit:Literal) -> None:
        """
        Cette méthode permet d'ajouter un littéral au langage du système

        :param lit: le littéral à ajouter
        """
        self.language.add(lit)

    def add_rule(self, rule:Rule) -> None:
        """
        Cette méthode permet d'ajouter une règle au système

        :param rule: la règle à ajouter
        """
        self.rules.add(rule)

    def add_assumption(self, lit:Literal) -> None:
        """
        Cette méthode permet d'ajouter une assumption au système

        :param lit: l'assumption à ajouter
        """
        self.assumptions.add(lit)

    def add_contrary(self, contr:Contrary) -> None:
        """
        Cette méthode permet d'ajouter une contrariété au système

        :param contr: la contrariété à ajouter
        """
        self.contraries.add(contr)

    def add_preference(self, preferred: Literal, over: Literal) -> None:
        """Ajoute une préférence et calcule la fermeture transitive.
        
        :param preferred: Le litéral préféré
        :param over: Le litéral non préférer
        """
        if preferred not in self.preferences:
            self.preferences[preferred] = set()
        if self.is_preferred(over, preferred):
            raise ValueError(f"Adding preference {preferred} > {over} would create a cycle")
        self.preferences[preferred].add(over)

    def is_preferred(self, lit1: Literal, lit2: Literal) -> bool:
        """Vérifie si `lit1` est préféré à `lit2`, en tenant compte de la transitivité.
        - lit1 > * > lit2
        
        :param lit1: Le préférer
        :param lit2: Le dominé    
        :return: True Si lit1 > lit2 False sinon
        """
        if lit1 not in self.preferences or self.preferences[lit1] is None:
            return False
        return lit2 in self.preferences[lit1] or \
                   any(self.is_preferred(dominate, lit2) for dominate in self.preferences[lit1])

    def is_atomic(self) -> bool:
        """
        Cette méthode permet de savoir si un l'aba est atomique

        :return: True si l'aba est atomique, False sinon
        """
        return all(rule.is_fact or (rule.body in self.assumptions) for rule in self.rules)

    def is_rule_atomic(self, rule:Rule) -> bool:
        """
        Cette méthode permet de savoir si une règle est atomique

        :return: True si le littéral est atomique, False sinon
        """
        return rule.is_fact or (rule.body in self.assumptions)

    def find_rule(self, subset:set[Literal]) -> set[Rule]:
        """
        Cette méthode permet de trouver toutes les regles qui peuvent s'appliquer 
        grâce à un sous ensemble de Literals

        :param subset set[Literal]: le sous ensemble de littéraux à partir duquel 
        on cherche les règles
        :return set[Rule]: les règles trouvées
        """
        set_rule = set()
        for rule in self.rules:
            if rule.body.issubset(subset):
                set_rule.add(rule)
        return set_rule

    def is_circular(self,
                    rules_alerdy_find:set[Rule]=None,
                    literals_find:set[Literal]=None,
                    rule_to_travers:Rule=None) -> bool:
        """
        Cette méthode permet de savoir si un l'aba est circulaire

        :return: True si le aba est circulaire, False sinon
        """
        if not rule_to_travers:
            if not self.rules:
                return False
            rules_start = self.find_rule(self.assumptions)
            rules_alerdy_find = rules_start
            literals_find = {lit for lit in self.assumptions}
            return any(self.is_circular(
                rules_alerdy_find=rules_alerdy_find,
                literals_find=literals_find,
                rule_to_travers=rule) for rule in rules_start)

        rules_alerdy_find.add(rule_to_travers)
        literals_find.add(rule_to_travers.head)
        new_rules:set[Rule] = self.find_rule(literals_find)
        new_rules = {rule for rule in new_rules if rule_to_travers.head in rule.body}
        if any(rule in rules_alerdy_find for rule in new_rules):
            return True
        return any(self.is_circular(rules_alerdy_find, literals_find, rule) for rule in new_rules)

    def aba_to_atomic(self) -> None:
        """
        Cette méthode permet de se transformer en un aba atomique
        - Chaque Literal qui ne fait pas partie des asomptions est remplacé par deux nouveaux 
        littéraux sd et snd
        - Chaque regle est alors adaptée pour prendre en compte ces nouveaux littéraux
        - Les contrariétés sont également adaptées
        """
        if self.is_atomic():
            return

        if self.is_circular():
            self.to_non_circular()

        new_asses:set[Literal] = self.assumptions.copy()
        new_contraries:set[Contrary] = self.contraries.copy()
        # Dict from lit to sd version of the same lit
        literal_to_sd:dict[Literal, Literal] = {}

        # Create new assumptions and contraries
        for literal in self.language:
            if literal not in self.assumptions:
                sd = Literal(f"{literal.name}_d", False)
                snd = Literal(f"{literal.name}_nd", False)
                new_asses.add(sd)
                new_asses.add(snd)
                new_contraries.add(Contrary(sd, snd))
                new_contraries.add(Contrary(snd, literal))
                literal_to_sd[literal] = sd

        # Create new language with the added literals
        new_language = self.language.union(new_asses)
        # Create new rules
        new_rules = set()
        for rule in self.rules:
            if rule.is_fact or rule.body.issubset(self.assumptions):
                new_rules.add(rule)
                continue
            # If the rule is not atomic :
            new_rule_body = set()
            for lit in rule.body:
                if lit in self.assumptions:
                    new_rule_body.add(lit)
                else:
                    new_rule_body.add(literal_to_sd[lit])
            new_rules.add(Rule(rule.head, new_rule_body))

        # Update the framework with new language, rules, assumptions and contraries
        self.language = new_language
        self.rules = new_rules
        self.assumptions = new_asses
        self.contraries = new_contraries

    def to_non_circular(self) -> None:
        """
        Cette méthode permet de se transformer en un aba non-circulaire
        - Chaque regle est alors adaptée pour utiliser différents nouveaux littéraux en tête et en corps de règle
        - Les contrariétés et les assomptions sont inchangées
        """
        if not self.is_circular():
            return
        k = len(self.language - self.assumptions)

        # Create new rules
        new_rules = set()
        new_lits = set()
        for rule in self.rules:
            if rule.is_fact:
                new_rules.add(rule)
                
            # If the rule is atomic :
            elif rule.body.issubset(self.assumptions):
                for i in range(1, k+1):
                    if i == k:
                        # s^k = s
                        new_head = rule.head
                    else:
                        imoins1 = [ e for e in new_lits if e.name == f"{rule.head.name}_{i}" ]
                        if imoins1:
                            new_head = imoins1[0]
                        else:
                            # create the i-1 version of the literal
                            new_head = Literal(f"{rule.head.name}_{i}", rule.head.is_negated)
                            new_lits.add(new_head)
                    new_rules.add(Rule(new_head, rule.body))
                    
            # If the rule is not atomic :
            else :
                for i in range (2, k+1):
                    new_rule_body = set()
                    if i == k :
                        # s^k = s
                        new_head = rule.head
                    else:
                        new_head = Literal(f"{rule.head.name}_{i}", rule.head.is_negated)
                        new_lits.add(new_head)
                    for lit in rule.body:
                        if lit in self.assumptions:
                            new_rule_body.add(lit)
                        else:
                            # find the i-1 version of the literal from new_lits if it exists
                            imoins1 = [ e for e in new_lits if e.name == f"{lit.name}_{i-1}" ]
                            if imoins1:
                                new_rule_body.add(imoins1[0])
                            else:
                                # no i-1 version of the literal, create it and add it
                                imoins1 = Literal(f"{lit.name}_{i-1}", lit.is_negated)
                                new_lits.add(imoins1)
                                new_rule_body.add(imoins1)
                    new_rules.add(Rule(new_head, new_rule_body))

        # Update the framework with new rules
        self.rules = new_rules
        self.language = self.language.union(new_lits)

    def _generate_combinations(self, s:set) -> list[set]:
        """
        Permet de générer toutes les combinaisons possibles d'un ensemble
        :return: une liste de combinaisons
        """
        all_combinations = []
        for r in range(1, len(s) + 1):
            comb = combinations(s, r)
            all_combinations.extend(comb)
        return [set(c) for c in all_combinations]


    def computing_normal_and_reverse_attack(self):
        """
        Cette méthode permet reprends les attaques et calculer les attaques normales et inverse
        """
        if self.arguments == set():
            self.generate_arguments()
            if self.arguments == set():
                return

        arg:Argument
        all_combi:list[set[Literal]] = self._generate_combinations(self.assumptions)
        contrary:Contrary

        for contrary in self.contraries:
            if not contrary.target in self.assumptions:
                continue
            all_args = self.get_all_args_by_claim(contrary.attacker)
            for arg in all_args:
                if not arg.leaves.issubset(self.assumptions):
                    continue
                if all(not self.is_preferred(contrary.target, lit) for lit in arg.leaves):
                    for one_combi in all_combi:
                        for two_combi in all_combi:
                            self.normal_attacks.add(SetAttack(
                                attacker=one_combi.union(arg.leaves),
                                attacked=two_combi.union({contrary.target})
                                ))

                if any(self.is_preferred(contrary.target, lit) for lit in arg.leaves):
                    for one_combi in all_combi:
                        for two_combi in all_combi:
                            self.reverse_attacks.add(SetAttack(
                                attacker=one_combi.union({contrary.target}),
                                attacked=two_combi.union(arg.leaves)
                                ))
