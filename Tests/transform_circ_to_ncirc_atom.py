from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Argument import Argument
from ape.Aba import Aba


def test_cours():
    a = Literal("a", False)
    p = Literal("p", False)
    q = Literal("q", False)

    ABA_cours = Aba(
        language={a, p, q, },
        rules={Rule(p, {a}), Rule(p, {q}), Rule(q, {p}), },
        assumptions={a},
        contraries={}

    )
    print(ABA_cours)

    ABA_cours.aba_to_non_circular_and_atomic()

    print(ABA_cours)

def test_TD4():
    a = Literal("a", False)
    b = Literal("b", False)
    x = Literal("x", False)
    y = Literal("y", False)
    z = Literal("z", False)

    ABA_cours = Aba(
        language={a, b, x, y, z},
        rules={Rule(y, {b}), Rule(y, {y}), Rule(x, {x}), Rule(x, {a}), Rule(z, {x, y})},
        assumptions={a, b},
        contraries={Contrary(a, y), Contrary(b, x)}

    )
    print(ABA_cours)

    ABA_cours.aba_to_non_circular_and_atomic()

    print(ABA_cours)

test_cours()
print("\n\n")
test_TD4()
