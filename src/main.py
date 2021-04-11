# Andrew Lorber
# NLP Project 2 - Parser

import string

# Class to store information in each cell
# Allows retrieval of possible parses
class CellNode:
    def __init__(self, lhs, rhs1, rhs2):
        self.lhs = lhs
        self.rhs1 = rhs1
        self.rhs2 = rhs2

# Imports grammar files and stores grammar rules
def import_grammar():
    # Gets grammar file
    # grammar_file_name = input("Please enter name of file containing CFG in CNF:\n")
    grammar_file_name = "../Grammars/CNF Sample Grammar.txt"  # Hardcoded for now
    grammar_file = open(grammar_file_name, 'r')

    # Builds dictionary from grammar rules
    grammar_rules = {}  # { LHS : [RHS,RHS,...] }
    reverse_grammar_rules = {}  # { RHS : [LHS,LHS,...] }
    for rule in grammar_file.read().split("\n"):
        if rule != "":  # Ignores empty lines
            lhs, rhs = rule.split(" --> ")
            if lhs in grammar_rules:
                grammar_rules[lhs].append(rhs.split())
            else:
                grammar_rules[lhs] = [rhs.split()]
            if rhs in reverse_grammar_rules:
                reverse_grammar_rules[rhs].append(lhs)
            else:
                reverse_grammar_rules[rhs] = [lhs]

    return grammar_rules, reverse_grammar_rules


# Parses sentence using CKY Algorithm
def parse_sentence(sentence, reversed_grammar_rules):
    # Splits sentence into tokens
    tokens = sentence.split()

    cky_chart = [[]*(len(tokens)+1)]*(len(tokens)+1)

    # Following pseudocode from textbook
    for j in range(1, len(tokens)+1):
        curr_token = tokens[j-1]

        for lhs in reversed_grammar_rules[curr_token]:
            cky_chart[j-1][j].append(CellNode(lhs, CellNode(curr_token)))

        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                for b in cky_chart[i][k]:
                    for c in cky_chart[k][j]:
                        for lhs in reversed_grammar_rules[" ".join([b.lhs, c.lhs])]:
                            cky_chart[i][j].append(CellNode(lhs, b, c))

    return cky_chart


# Main
# ----
if __name__ == "__main__":
    grammar_rules, reversed_grammar_rules = import_grammar()
    print(grammar_rules,"\n")
    print(reversed_grammar_rules,"\n")

    while True:
        # Reads in sentence
        sentence = input("Please enter a sentence:\n")
        # Removes punctuation and converts to lowercase
        sentence = sentence.translate(str.maketrans('','',string.punctuation)).lower()

        # Checks for quit
        if sentence == "quit":
            break

        parse_sentence(sentence, reversed_grammar_rules)
