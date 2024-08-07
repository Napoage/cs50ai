from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."

#1.A is either a knight xor a knave 
#2.Knight implies truth
#3.Knave implies falsehood
#A contridicts 1 thus statement is a false
#if statement is false then A lied
#thuse a is a knave

knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight,And(AKnight, AKnave)),
    Implication(AKnight,Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.

#1.A person is either a knight xor a knave 
#2.Knight implies truth
#3.Knave implies falsehood
#A says we are both knaves
#if a is a knight it must tell the true
#thus we are both knaves is a contradiction and a cant be a knight
#if a is a knave the statement must be false
#aknave ^ bknave one must be false
#aknave is true thuse bknave is false
#if b is not a knave he must be aknight

knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight,And(AKnave, BKnave)),
    Implication(AKnave,Not(And(AKnave,BKnave))),
    Implication(Implication(AKnave,Not(And(AKnave,BKnave))),Or(AKnight,BKnight))     
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

#1.A person is either a knight xor a knave 
#2.Knight implies truth
#3.Knave implies falsehood
#A says we are the same kind thus aknight ^ bknight or aknave ^ bknave
#aknave ^ bknave cant be true because then a would have to b lying
#B says they are different thus Aknave ^ bknight or b is lying and is a knave
#aknave ^ bknave cant be true if b is true thus a is lying thus b is telling the truth aknave and bknight
#~(Aknight^BKnight)
#~Aknight or ~Bknight
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, Or(And(AKnight, BKnight),And(AKnave,BKnave))),
    Implication(AKnave, Not(Or(And(AKnight, BKnight),And(AKnave,BKnave)))),
    Implication(BKnave, Or(And(AKnight, BKnight),And(AKnave,BKnave))),
    Implication(BKnight, Not(Or(And(AKnight, BKnight),And(AKnave,BKnave))))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

#b said a said i am a knave whihc a did not say thus b is a knave
#b says c is a knave since b is a knave it must be false and c must be a knight
#since c is a knight his statement must be true thus a is a knight
#a statement is true

knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnave, AKnight)),

    Or(BKnight, BKnave),
    Not(And(BKnave, BKnight)),

    Or(CKnight, CKnave),
    Not(And(CKnave, CKnight)),

    Implication(BKnave, CKnight),
    Implication(BKnight, CKnave),

    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),

    Implication(BKnight, Biconditional(AKnight,AKnave)),
    Implication(BKnave, Not(Biconditional(AKnight, AKnave))),

)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
