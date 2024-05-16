#TEAM MEMBERS:
#Arshia Yousefnia
#Ruzbeh Moeini

import SCANNER, parser

newScanner = SCANNER.Scanner("input.txt", "tokens.txt", "lexical_errors.txt", "symbol_table.txt")
# newScanner.scan()
newParser = parser.parser("syntax_errors.txt", "parse_tree.txt", "grammar_data.json", scanner=newScanner)
newParser.analyze()
