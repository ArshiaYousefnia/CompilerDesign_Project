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
        self.symbols_table = "\n".join([f"{i + 1}.\t{self.dfa.get_keywords_list()[i]}" for i in range(len(self.dfa.get_keywords_list()))]) + "\n"
        
        self.last_open_comment_line = -1


    def advance_reading(self):
        if self.input_text[self.pointer] == "آ":
            self.pointer += 1
            return 1, None
        
        self.dfa.make_transition(self.input_text[self.pointer])

        if self.dfa.entered_comment:
            self.last_open_comment_line = self.line_number
            self.dfa.entered_comment = False
        
        if self.input_text[self.pointer] == "\n" and not self.dfa.lookahead:
            self.line_number += 1
            if len(self.tokens_table) != 0 and self.tokens_table[-1] == '\t':
                self.tokens_table = self.tokens_table[:-(len(str(self.line_number - 1)) + 2)]
                self.tokens_table += f"{self.line_number}.\t"
            else:
                self.tokens_table += f"\n{self.line_number}.\t"
            
            if len(self.errors_table) != 0 and self.errors_table[-1] == '\t':
                self.errors_table = self.errors_table[:-(len(str(self.line_number - 1)) + 2)]
                self.errors_table += f"{self.line_number}.\t"
            else:
                self.errors_table += f"\n{self.line_number}.\t"
        
        if self.dfa.is_final:
            token = self.dfa.get_token()
            if token != None:
                if self.dfa.error_flag:
                    self.errors_table += f"({token[1]}, {token[0]}) "
                    self.pointer += 1
                    self.dfa.reset()
                    return 1
                if token[0] == "ID" and token[1] in self.dfa.get_keywords_list():
                    token = ("KEYWORD", token[1])

                if token[0] != "WHITESPACE" and token[0] != "COMMENT":
                    self.tokens_table += f"({token[0]}, {token[1]}) "
                    self.tokens_list.append(token)
                
                if token[0] == "ID" and token[1] not in self.identifiers_list:
                    self.symbols_table += f"{len(self.identifiers_list) + len(self.dfa.get_keywords_list()) + 1}.\t{token[1]}\n"
                    self.identifiers_list.append(token[1])
                
                if not self.dfa.lookahead:
                    self.pointer += 1
                self.dfa.reset()
                if token[0] == "WHITESPACE" or token[0] == "COMMENT":
                    return 1, None
                return 1, token

            #error has occurred

        
        self.pointer += 1
        return 0, None
    
    def get_next_token(self):
        if (self.pointer == self.eof_pointer):
            return "$"
        
        output = self.advance_reading()
        while (output[1] == None and self.pointer < self.eof_pointer):
            output = self.advance_reading()
        
        if (output[1] == None):
            return "$"
        
        return output[1]
    

    def scan(self):
        self.tokens_table += f"{self.line_number}.\t"

        self.errors_table += f"{self.line_number}.\t"

        while self.pointer < self.eof_pointer:
            final_status = self.advance_reading()[0]
        if final_status == 0:
            if self.errors_table[-1] == '\t':
                self.errors_table = self.errors_table[:-(len(str(self.line_number - 1)) + 2)]
                self.errors_table += f"\n{self.last_open_comment_line}.\t"
            
            if len(self.dfa.input_string) > 7:
                self.errors_table += f"({self.dfa.input_string[0:7]}..., Unclosed comment) "
            else:
                self.errors_table += f"({self.dfa.input_string}, Unclosed comment) "
        
        if self.tokens_table[-1] == '\t':
            self.tokens_table = self.tokens_table[:-(len(str(self.line_number - 1)) + 2)]

    
        if self.errors_table[-1] == '\t':
            self.errors_table = self.errors_table[:-(len(str(self.line_number - 1)) + 2)]
        if len(self.errors_table) == 0:
            self.errors_table = "There is no lexical error."

        try:
            try:
                self.tokens_file = open(self.tokens_file_name, "w")
            except:
                self.tokens_file = open(self.tokens_file_name, "x")
            self.tokens_file.write(self.tokens_table)
            self.tokens_file.close()

            try:
                self.errors_file = open(self.errors_file_name, "w")
            except:
                self.errors_file = open(self.errors_file_name, "x")
            self.errors_file.write(self.errors_table)
            self.errors_file.close()

            try:
                self.symbols_file = open(self.symbol_table_file_name, "w")

            except:
                self.symbols_file = open(self.symbol_table_file_name, "x")
            self.symbols_file.write(self.symbols_table)
            self.symbols_file.close()
        except:
            print("could not write to files")
