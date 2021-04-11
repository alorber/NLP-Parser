# Andrew Lorber
# NLP Project 2 - Parser

import string


# Class to store information in each cell
# Allows retrieval of possible parses
class CellNode:
    def __init__(self, lhs, rhs1=None, rhs2=None):
        self.lhs = lhs  # Left-hand side
        self.rhs1 = rhs1  # Right-hand side 1
        self.rhs2 = rhs2  # Right-hand side 2


# Imports grammar files and stores grammar rules
def import_grammar():
    # Gets grammar file
    # grammar_file_name = input("Please enter name of file containing CFG in CNF:\n")
    grammar_file_name = "../Grammars/CNF Sample Grammar.txt"  # Hardcoded for now
    grammar_file = open(grammar_file_name, 'r')

    # Builds dictionary from grammar rules
    reverse_grammar_rules = {}  # { RHS : [LHS,LHS,...] }
    for rule in grammar_file.read().split("\n"):
        if rule != "":  # Ignores empty lines
            lhs, rhs = rule.split(" --> ")

            if rhs in reverse_grammar_rules:
                reverse_grammar_rules[rhs].append(lhs)
            else:
                reverse_grammar_rules[rhs] = [lhs]

    return reverse_grammar_rules


# Parses sentence using CKY Algorithm
def parse_sentence(sentence, reverse_grammar_rules):
    # Splits sentence into tokens
    tokens = sentence.split()

    # Table for CKY Algorithm
    cky_chart = [[[] for _ in range(len(tokens) + 1)] for _ in range(len(tokens) + 1)]

    # Following pseudocode from textbook
    for j in range(1, len(tokens) + 1):
        curr_token = tokens[j - 1]

        for lhs in reverse_grammar_rules.get(curr_token, []):
            cky_chart[j - 1][j].append(CellNode(lhs, CellNode(curr_token)))

        for i in range(j - 2, -1, -1):
            for k in range(i + 1, j):
                for b in cky_chart[i][k]:
                    for c in cky_chart[k][j]:
                        for lhs in reverse_grammar_rules.get(" ".join([b.lhs, c.lhs]), []):
                            cky_chart[i][j].append(CellNode(lhs, b, c))

    return cky_chart


# Recursively prints parse
def rec_print_parse(parse_node, print_tree, num_indents):
    divider = ("\n" + "\t" * num_indents) if print_tree else " "

    if num_indents > 0:
        print(divider, end="")

    if parse_node.rhs2 is None:
        print("[" + parse_node.lhs + " " + parse_node.rhs1.lhs + "]", end="")
    else:
        print("[" + parse_node.lhs, end="")
        rec_print_parse(parse_node.rhs1, print_tree, num_indents + 1)
        rec_print_parse(parse_node.rhs2, print_tree, num_indents + 1)
        if print_tree:
            print(divider, end="")
        print("]", end="")


# Prints valid parses
def print_parses(cky_chart):
    # Determines whether to print parse tree
    print_tree = True if input("Would you like to display the parse tree? (y/n)\n").lower() == "y" else False

    for parse_num, cell in enumerate(list(filter(lambda rule: rule.lhs == "S", cky_chart[0][-1])), 1):
        print(f"Valid parse #{parse_num}")
        rec_print_parse(cell, False, 0)
        print("\n")
        if print_tree:
            rec_print_parse(cell, True, 0)
            print("\n")


# Main
# ----
if __name__ == "__main__":
    reverse_grammar_rules = import_grammar()

    while True:
        # Reads in sentence
        sentence = input("Please enter a sentence:\n")
        # Removes punctuation and converts to lowercase
        sentence = sentence.translate(str.maketrans('', '', string.punctuation)).lower()

        # Checks for quit
        if sentence == "quit":
            break

        cky_chart = parse_sentence(sentence, reverse_grammar_rules)

        # Checks for valid parses
        num_parses = len(list(filter(lambda rule: rule.lhs == "S", cky_chart[0][-1])))

        if num_parses == 0:
            print("NO VALID PARSES\n")
        else:
            print_parses(cky_chart)
            print(f"Number of valid parses: {num_parses}\n")
