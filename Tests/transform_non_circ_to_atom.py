from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Argument import Argument
from ape.Aba import Aba


def test_cours():
    a = Literal("a", False)
    b = Literal("b", False)
    p = Literal("p", False)
    q = Literal("q", False)
    r = Literal("r", False)

    ABA_cours = Aba(
        language={a, b, p, q, r,},
        rules={Rule(p, {q}), Rule(q, {a}), Rule(r, {b}), },
        assumptions={a, b,},
        contraries={Contrary(a, r), Contrary(b, p),}

    )
    print(ABA_cours)

    ABA_cours.aba_to_atomic()

    print(ABA_cours)


test_cours()
