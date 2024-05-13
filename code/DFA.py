class DFA:
    def __init__(self,):
        self.state = 0
        self.is_final = False
        self.output = None
        self.input_string = ""
        self.current_input = None
        self.token_type = None
        self.lookahead = False
        self.lexical_error = None
        self.error_flag = False
        self.entered_comment = False

        self.digits = [str(i) for i in range(10)]

        self.keywords = ["if", "else", "void", "int", "for", "break", "return", "endif"]
        #self.keywords = ["break", "else", "if", "int", "while", "return", "void"]
        
        self.symbols = [";", ":", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", ","]
        self.whitespaces = [" ", "\n", "\t", "\r", "\v", "\f"]
        self.letters = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]
    
    def get_keywords_list(self):
        return self.keywords

    def reset(self):
        self.state = 0
        self.is_final = False
        self.output = None
        self.lexical_error = ""
        self.error_flag = False
        if self.lookahead:
            self.lookahead = False
        self.input_string = ""
        self.token_type = None
        self.entered_comment = False

    def get_token(self):
        if not self.is_final:
            return None
        if not self.error_flag:
            if not self.lookahead:
                return (self.token_type, self.input_string)
            else:
                return (self.token_type, self.input_string[:-1])
        else:
            if not self.lookahead:
                return (self.lexical_error, self.input_string)
            else:
                return (self.lexical_error, self.input_string[:-1])

        # self.reset()
    
    def make_transition(self, input_char):
        
        if self.is_final:
            return
        self.input_string += input_char


        if self.state == 0:
            if input_char in self.whitespaces:
                self.state = 18
                self.is_final = True
                self.token_type = "WHITESPACE"
            elif input_char == "=":
                self.state = 16
            elif input_char == "*":
                self.state = 15
            elif input_char in self.symbols:
                self.state = 3
                self.is_final = True
                self.token_type = "SYMBOL"
                self.token_type = "SYMBOL"
            elif input_char in self.digits:
                self.state = 2
            elif input_char in self.letters:
                self.state = 1
            elif input_char == "/":
                self.state = 17
            else:
                self.is_final = True
                self.error_flag = True
                self.lexical_error = "Invalid input"
        

        elif self.state == 1:
            if input_char in self.whitespaces + self.symbols:
                self.state = 19
                self.is_final = True
                self.lookahead = True
                if self.input_string in self.keywords:
                    self.token_type = "KEYWORD"
                else:
                    self.token_type = "ID"
            elif input_char not in self.digits + self.letters:
                self.is_final = True
                self.error_flag = True
                self.lexical_error = "Invalid input"

        

        elif self.state == 2:
            if input_char in self.whitespaces + self.symbols:
                self.state = 20
                self.is_final = True
                self.lookahead = True
                self.token_type = "NUM"
            elif input_char not in self.digits:
                self.is_final = True
                self.error_flag = True
                self.lexical_error = "Invalid number"
        

        elif self.state == 16:
            if input_char == "=":
                self.state = 21
                self.is_final = True
                self.token_type = "SYMBOL"
            else:
                self.state = 22
                self.is_final = True
                self.lookahead = True
                self.token_type = "SYMBOL"

        elif self.state == 15:
            if input_char == "/":
                self.is_final = True
                self.error_flag = True
                self.lexical_error = "Unmatched comment"
            else:
                if input_char not in self.digits + self.letters + self.whitespaces + self.symbols:
                    self.error_flag = True
                    self.lexical_error = "Invalid input"
                    self.is_final = True
                else:
                    self.state = 3
                    self.is_final = True
                    self.lookahead = True
                    self.token_type = "SYMBOL"

        elif self.state == 17:
            #if input_char == "/":
            #    self.state = 25
            if input_char == "*":
                self.state = 24
                self.entered_comment = True
            else:
                self.state = 23
                self.is_final = True
                self.lookahead = True
                self.token_type = "SYMBOL"
        

        elif self.state == 24:
            if input_char == "*":
                self.state = 26
        

        elif self.state == 25:
            if input_char in ["\n", ""]:
                self.state = 27
                self.is_final = True
                self.token_type = "COMMENT"
        
        elif self.state == 26:
            if input_char == "/":
                self.state = 27
                self.is_final = True
                self.token_type = "COMMENT"
            elif input_char != "*":
                self.state = 24
