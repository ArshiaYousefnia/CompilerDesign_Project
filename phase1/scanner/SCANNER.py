import DFA


class Scanner:
    def __init__(self, input_file_name, tokens_file_name, errors_file_name, symbol_table_file_name):
        self.input_file_name = input_file_name
        self.tokens_file_name = tokens_file_name
        self.errors_file_name = errors_file_name
        self.symbol_table_file_name = symbol_table_file_name
        try:
            self.input_text = open(input_file_name, "r").read()
        except:
            raise FileNotFoundError(f"c-- scanner error: File {input_file_name} not found")

        self.dfa = DFA.DFA()
        self.pointer = 0
        self.eof_pointer = len(self.input_text)
        self.input_text.join("")
        self.line_number = 1
        self.tokens_list = []
        self.identifiers_list = []
        self.tokens_table = ""
        self.errors_table = ""
        self.symbols_table = "\n".join([f"{i + 1} {self.dfa.get_keywords_list()[i]}" for i in range(0, 8)]) + "\n"


    def get_next_token(self, ):
        self.dfa.make_transition(self.input_text[self.pointer])

        if self.input_text[self.pointer] == "\n" and not self.dfa.lookahead:
            self.line_number += 1
            try:
                int(self.tokens_table[-1])
                self.tokens_table = self.tokens_table[:-1]
                self.tokens_table += f"{self.line_number}"
            except:
                self.tokens_table += f"\n{self.line_number}"

        if self.dfa.is_final:
            token = self.dfa.get_token()
            if token != None:
                if token[0] == "ID" and token[1] in self.dfa.get_keywords_list():
                    token = ("KEYWORD", token[1])

                if token[0] != "WHITESPACE":
                    self.tokens_table += f" ({token[0]}, {token[1]})"
                    self.tokens_list.append(token)
                
                if token[0] == "ID" and token[1] not in self.identifiers_list:
                    self.symbols_table += f"{len(self.identifiers_list) + 9} {token[1]}\n"
                    self.identifiers_list.append(token[1])
                
                if not self.dfa.lookahead:
                    self.pointer += 1
                self.dfa.reset()
                return 1

            #error has occurred
            self.errors_table += f"{self.line_number}\t{self.input_text}\n"
            self.pointer += 1
            self.dfa.reset()
            return 0
        
        self.pointer += 1
        return 0

    def scan(self):
        self.tokens_table += f"{self.line_number}"
        while self.pointer < self.eof_pointer:
            self.get_next_token()

        try:
            self.tokens_file = open(self.tokens_file_name, "w")
            self.tokens_file.write(self.tokens_table)
            self.tokens_file.close()

            self.errors_file = open(self.errors_file_name, "w")
            self.errors_file.write(self.errors_table)
            self.errors_file.close()

            self.symbols_file = open(self.symbol_table_file_name, "w")
            self.symbols_file.write(self.symbols_table)
            self.symbols_file.close()
        except:
            raise FileNotFoundError(f"c-- scanner error: Could not write to files")
