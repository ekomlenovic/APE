from ape.Literal import Literal
from ape.Rule import Rule
from ape.Contrary import Contrary
from ape.Argument import Argument
from ape.Aba import Aba



def main():
    print(Literal("A", False))
    print(Argument("Arg1", {Literal("B", False)}, Literal("C", False)))
    print(Contrary(Literal("A", True), Literal("B", False)))
    print(Literal("A", False) == Literal("A", False))
    print(Aba(
        language={Literal("A", False), Literal("B", False)},
        rules={Rule(Literal("A", False), {Literal("B", False)})},
        assumptions={Literal("A", False)},
        contraries={Contrary(Literal("A", False), Literal("B", False))}))
    A = Literal("A", False)
    B = Literal("B", False)
    X = Literal("X", False)
    Y = Literal("Y", False)
    ABA = Aba(
        language={A, B, X, Y},
        rules={Rule(X, {A}), Rule(X, {X}), Rule(Y, {Y}), Rule(Y, {B})},
        assumptions={A, B},
        contraries={Contrary(A, B), Contrary(B, X)})
    print(ABA)
    print(ABA.is_circular())
    ABA2 = Aba(
        language={A, B, X, Y},
        rules={Rule(X, {A}), Rule(Y, {B})},
        assumptions={A, B},
        contraries={Contrary(A, B), Contrary(B, Y)})
    print(ABA2)
    print(ABA2.is_circular())
    ABA3 = Aba(
        language={A, B, X, Y},
        rules={Rule(X, {A}), Rule(Y, {X}), Rule(X, {Y, A}), Rule(Y, {B})},
        assumptions={A, B},
        contraries={Contrary(A, B), Contrary(B, X)})
    print(ABA3)     
    print(ABA3.is_circular())

    ABA2.add_preference(A, B)
    ABA2.add_preference(B, X)
    if ABA2.is_preferred(A, X):
        print("transitivité ok")
    ABA2.add_preference(X, A)

if __name__ == "__main__":     
    main()

