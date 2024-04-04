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
        
        self.dfa = DFA()
        self.pointer = 0
        self.eof_pointer = len(self.input_text)
        self.input_text.append("")
        self.line_number = 1
        self.tokens_list = []
        self.identifiers_list = []
        self.tokens_table = ""
        self.errors_table = ""
        self.symbols_table = "\n".join([f"{i + 1}.\t{self.dfa.get_keywords_list()[i]}"]) + "\n"
    
    def get_next_token(self, ):
        self.dfa.make_transition(self.input_text[self.pointer])

        if self.input_text[self.pointer] == "\n":
            self.line_number += 1

        if self.dfa.is_final:
            token = self.dfa.get_token()
            if token:
                self.tokens_table += f"{token[0]}\t{token[1]}\t{self.line_number}\n"
                self.tokens_list.append(token)
                self.pointer += 1
                self.dfa.reset()
                return 1
            
            if token[0] == "IDENTIFIER":
                if (token[0] not in self.identifiers_list):
                    self.symbols_table += f"{len(self.identifiers_list) + 1}.\t{token[0]}\t{token[1]}\n"
                self.identifiers_list.append(token[1])
        self.pointer += 1
        return 0
    
    def scan(self):
        while self.pointer <= self.eof_pointer:
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
        