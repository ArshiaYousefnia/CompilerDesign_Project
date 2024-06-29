

class Codegen:
    def __init__(self, output_file, symbol_table, semantic_errors_file):
        self.program_block = []
        self.semantic_stack = []
        self.top = -1  # pointer for semantic stack
        self.PB_pointer = 0  # pointer for program block
        self.data_pointer = 200  # pointer for data block
        self.temp_pointer = 1000  # pointer for temporary block
        self.output_file = output_file
        self.semantic_errors_file = semantic_errors_file
        self.symbol_table = symbol_table
        self.data_block = dict()
        self.scope_pointer = 0
        self.while_switch_scope_stack = [0] * 100
        self.error_message = ''


    def generate(self, action, current_input):
        if action == "PID":
            pass
        # toDo add action functions