import json

import SCANNER
from anytree import Node, RenderTree, ContStyle, PreOrderIter
# print(RenderTree(f, style=ContStyle()).by_attr())


class parser:

    def __init__(self, syntax_errors_file_name, parse_tree_file_name, grammar_data_file_name, scanner: SCANNER):
        self.syntax_errors_file_name = syntax_errors_file_name
        self.parse_tree_file_name = parse_tree_file_name
        self.grammar_data_file_name = grammar_data_file_name
        self.scanner = scanner
        data = open(self.grammar_data_file_name)
        data_table = json.load(data)
        self.terminals = data_table['terminals']
        self.non_terminals = data_table['non_terminals']
        self.predict = data_table['predict']
        self.grammar = data_table['grammar']
        self.root = Node("Program")
        self.current_node = self.root
        self.current_non_terminal = "Program"
        self.eof_pointer = scanner.eof_pointer
        self.lookahead = ()
        self.lookahead_terminal_equivalent = ""

    def next_non_terminal_handle(self):
        predict_sets = self.predict[self.current_non_terminal]
        for predict_set in predict_sets:
            if self.lookahead_terminal_equivalent in predict_set:
                rhs = self.grammar[int(predict_set[0])]
                nodes = rhs.split()
                # self.add_new_parse_tree_nodes(nodes)
                self.match(nodes)

    # def add_new_parse_tree_nodes(self, nodes):
    #     # nodes = nodes.split()
    #     # next_non_terminal = None
    #     for node in nodes:
    #         # if node in self.non_terminals and next_non_terminal is not None:
    #         #     next_non_terminal = Node(node,self.current_non_terminal)
    #         # else:
    #         Node(node, parent=self.current_node)
        # if next_non_terminal is not None
        #     self.current_node =

    def analyze(self):
        self.get_next_terminal()
        while self.lookahead[0] != "$":
            self.next_non_terminal_handle()
        print(RenderTree(self.root, style=ContStyle()))

    def get_next_terminal(self):
        for pre, _, node in RenderTree(self.root):
            print("%s%s" % (pre, node.name))
        self.lookahead = self.scanner.get_next_token()
        print(self.lookahead)
        # print(RenderTree(self.root, style=ContStyle()))
        if self.lookahead[0] == "SYMBOL" or self.lookahead[0] == "KEYWORD":
            self.lookahead_terminal_equivalent = self.lookahead[1]
        else:
            self.lookahead_terminal_equivalent = self.lookahead[0]

    def match(self, expected_tokens):
        parent_node = self.current_node
        for expected_token in expected_tokens:
            if expected_token in self.non_terminals:
                self.current_non_terminal = expected_token
                self.current_node = Node(expected_token, parent=parent_node)
                # self.get_next_terminal()
                self.next_non_terminal_handle()
            elif expected_token == self.lookahead_terminal_equivalent or expected_token == "epsilon":
                Node(expected_token, parent=parent_node)
                self.get_next_terminal()
            else:
                print("error") #toDo error handling



