import pytest
from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Argument import Argument
from ape.Aba import Aba

def test_td4_1():
    """
    Test the generation of attacks for the TD4_1 example
    must return 10 attacks
    """
    a = Literal("a", False)
    b = Literal("b", False)
    c = Literal("c", False)
    q = Literal("q", False)
    p = Literal("p", False)
    r = Literal("r", False)
    s = Literal("s", False)
    t = Literal("t", False)

    TD4_1 = Aba(
        language={a, b, c, q, p, r, s, t},
        rules={Rule(p, {q, a}), Rule(q, {}), Rule(r, {b, c}), Rule(t, {p, c}), Rule(s, {t})},
        assumptions={a, b, c},
        contraries={Contrary(a, r), Contrary(b, s), Contrary(c, t)}
    )

    TD4_1.generate_arguments()
    TD4_1.generate_attacks()

    assert len(TD4_1.attacks) == 10, "Incorrect number of attacks generated for TD4_1"

def test_cour_1():
    """
    Test the generation of attacks for the Cour_1 example
    """
    a = Literal("a", False)
    b = Literal("b", False)
    c = Literal("c", False)
    q = Literal("q", False)
    p = Literal("p", False)
    r = Literal("r", False)
    s = Literal("s", False)
    t = Literal("t", False)

    Cour_1 = Aba(
        language={a, b, c, q, p, r, s, t},
        rules={Rule(p, {q, a}), Rule(q, {}), Rule(r, {b, c})},
        assumptions={a, b, c},
        contraries={Contrary(a, r), Contrary(b, s), Contrary(c, t)}
    )

    Cour_1.generate_arguments()
    Cour_1.generate_attacks()

    assert len(Cour_1.attacks) == 2, "Incorrect number of attacks generated for Cour_1"
