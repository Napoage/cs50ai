import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP
NP -> N | Det N | Det AP N | N PP | NP Conj NP
VP -> V | V NP | V NP PP | VP Conj VP | VP Conj S | VP PP | VP AdvP | VP NP AdvP | AdvP VP
AP -> Adj | Adj AP
AdvP -> Adv | Adv AdvP
PP -> P NP
"""
# NEED TO ADD MORE NONTERMINALS

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.

    The preprocess function should accept a sentence as input and return a lowercased list of its words.
    You may assume that sentence will be a string.
    You should use nltk’s word_tokenize function to perform tokenization.
    Your function should return a list of words, where each word is a lowercased string.
    Any word that doesn’t contain at least one alphabetic character (e.g. . or 28) should be excluded from the returned list.
    """
    words = nltk.word_tokenize(sentence)
    processed = []
    for i in range(len(words)):
        if words[i].isalpha():
            processed.append(words[i].lower())
    return processed


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    The np_chunk function should accept a tree representing the syntax of a sentence, and return a list of all of the noun phrase chunks in that sentence.
    For this problem, a “noun phrase chunk” is defined as a noun phrase that doesn’t contain other noun phrases within it. Put more formally, a noun phrase chunk is a subtree of the original tree whose label is NP and that does not itself contain other noun phrases as subtrees.
    For example, if "the home" is a noun phrase chunk, then "the armchair in the home" is not a noun phrase chunk, because the latter contains the former as a subtree.
    You may assume that the input will be a nltk.tree object whose label is S (that is to say, the input will be a tree representing a sentence).
    Your function should return a list of nltk.tree objects, where each element has the label NP.
    You will likely find the documentation for nltk.tree helpful for identifying how to manipulate a nltk.tree object.
    """
    # can use label to test if it is a NP
    # ex tree.label() == "NP"
    nps = []
    """for node in tree:
        print("nodes: ", node)
        if node.label() == "NP":
            #print("NP: ", node)
            if node.subtrees() != "NP":
                nps.append(node)
                #print("NP: with no subtree", node)
                """
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            if subtree.subtrees() != "NP":
                nps.append(subtree)
    #doesnt check all subtrees subtrees       
        #print(subtree)
    
    return nps


if __name__ == "__main__":
    main()
