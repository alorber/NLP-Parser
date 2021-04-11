# Andrew Lorber
# NLP Project 2 - Parser

# Imports grammar files and stores grammar rules
def importGrammar():
    # Gets grammar file
    grammar_file_name = input("Please enter name of file containing CFG in CNF:\n")
    grammar_file = open(grammar_file_name, 'r')

    # Builds dictionary from grammar rules
    # { LHS : [RHS,RHS,...] }
    grammar_rules = {}
    for rule in grammar_file.read().split("\n"):
        if rule != "":  # Ignores empty lines
            lhs, rhs = rule.split(" --> ")
            if lhs in grammar_rules:
                grammar_rules[lhs].append(rhs.split(" "))
            else:
                grammar_rules[lhs] = [rhs.split(" ")]

    return grammar_rules



# Main
# ----
if __name__ == "__main__":
    grammar_rules = importGrammar()
    print(grammar_rules)