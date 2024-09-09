from tokens import *
from general import *
#######################################
# LEXER
#######################################

# The my_Lexer class is responsible for tokenizing the input text.
# It reads the source code character by character and converts it into a series of tokens.
# This lexer handles numbers, identifiers, keywords, operators, and special symbols.
# It also manages error detection for illegal characters and invalid tokens.


class MyLexer:
    def __init__(self, fn, text):
        # Initialize the lexer with file name (fn) and the input text
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text) # Track the position in the input text
        self.current_char = None
        self.advance() # Advance to the first character

    def advance(self):
        # Move the position one step ahead and update the current character
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        # Tokenize the input text, returning a list of tokens
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance() # Ignore whitespace
            elif self.current_char == '#':
                self.skip_comment() # Handle comments (skip them)
            elif self.current_char in DIGITS:
                tokens.append(self.make_number()) # Handle numbers
            elif self.current_char == '-' and self.next_char() in DIGITS:
                tokens.append(self.make_negative_number()) # Handle negative numbers
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier()) # Handle identifiers
            elif self.current_char == '@':
                token = self.make_keyword()  # Check if it's a keyword
                if token:
                    tokens.append(token)
                else:
                    token = self.make_operator() # If not, check if it's an operator
                    if token:
                        tokens.append(token)
                    else:
                        # If no valid token, raise an illegal character error
                        pos_start = self.pos.copy()
                        self.advance()
                        return [], IllegalCharError(pos_start, self.pos, "Invalid token starting with '@'")
            elif self.current_char == '(':
                tokens.append(my_Token(T_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(my_Token(T_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(my_Token(T_COMMA, pos_start=self.pos))
                self.advance()
            else:
                # If an unrecognized character is encountered, raise an error
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        return tokens, None

    def skip_comment(self):
        #Skips characters until the end of the line (single-line comment).
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()

    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return my_Token(T_INT, int(num_str), pos_start, self.pos)

    def make_negative_number(self):
        num_str = '-'
        pos_start = self.pos.copy()
        self.advance()
        while self.current_char is not None and self.current_char in DIGITS:
            num_str += self.current_char
            self.advance()
        return my_Token(T_INT, int(num_str), pos_start, self.pos)

    def make_identifier(self):
        _str = ''
        pos_start = self.pos.copy()
        while self.current_char is not None and self.current_char in LETTERS:
            _str += self.current_char
            self.advance()
        return my_Token(T_IDENTIFIER, _str, pos_start=pos_start)

    def next_char(self):
        pos = self.pos.idx + 1
        if pos < len(self.text):
            return self.text[pos]
        return None

    def make_keyword(self):
        id_str = '@'
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char is not None and self.current_char != '@':
            id_str += self.current_char
            self.advance()

        if self.current_char == '@':
            id_str += '@'
            self.advance()

            if id_str == '@TRUE@':
                return my_Token(T_BOOLEAN, True, pos_start, self.pos)
            elif id_str == '@FALSE@':
                return my_Token(T_BOOLEAN, False, pos_start, self.pos)
            elif id_str == '@DEF@':
                return my_Token(T_DEF, pos_start=pos_start)
            elif id_str == '@IS@':
                return my_Token(T_IS, pos_start=pos_start)
            elif id_str == '@END@':
                return my_Token(T_END, pos_start=pos_start)
            elif id_str == '@LAMBDA@':
                return my_Token(T_LAMBDA, pos_start=pos_start)
            elif id_str == '@:@':
                return my_Token(T_COLON, pos_start=pos_start)
            elif id_str == '@IF@':
                return my_Token(T_IF, pos_start=pos_start)
            elif id_str == '@THEN@':
                return my_Token(T_THEN, pos_start=pos_start)
            elif id_str == '@ELSEIF@':
                return my_Token(T_ELSEIF, pos_start=pos_start)
            elif id_str == '@ELSE@':
                return my_Token(T_ELSE, pos_start=pos_start)
            elif id_str == '@FOR@':
                return my_Token(T_FOR, pos_start=pos_start)
            elif id_str == '@IN@':
                return my_Token(T_IN, pos_start=pos_start)
            elif id_str == '@RANGE@':
                return my_Token(T_RANGE, pos_start=pos_start)
            elif id_str == '@DO@':
                return my_Token(T_DO, pos_start=pos_start)
            else:
                self.pos = pos_start
        else:
            return None  # This is not a valid keyword

    def make_operator(self):
        op_str = '@'
        pos_start = self.pos.copy()
        self.advance()

        while self.current_char is not None and self.current_char != '@':
            op_str += self.current_char
            self.advance()

        if self.current_char == '@':
            op_str += '@'
            self.advance()

            if op_str == '@+@':
                return my_Token(T_PLUS, pos_start=pos_start)
            elif op_str == '@-@':
                return my_Token(T_SUB, pos_start=pos_start)
            elif op_str == '@*@':
                return my_Token(T_MUL, pos_start=pos_start)
            elif op_str == '@/@':
                return my_Token(T_DIV, pos_start=pos_start)
            elif op_str == '@%@':
                return my_Token(T_MODULO, pos_start=pos_start)
            elif op_str == '@==@':
                return my_Token(T_EQEQ, pos_start=pos_start)
            elif op_str == '@!=@':
                return my_Token(T_NEQ, pos_start=pos_start)
            elif op_str == '@NOT@':
                return my_Token(T_NOT, pos_start=pos_start)
            elif op_str == '@<@':
                return my_Token(T_LESSTHAN, pos_start=pos_start)
            elif op_str == '@<=@':
                return my_Token(T_EQLESSTHAN, pos_start=pos_start)
            elif op_str == '@>@':
                return my_Token(T_GREATERTHAN, pos_start=pos_start)
            elif op_str == '@>=@':
                return my_Token(T_EQGREATERTHAN, pos_start=pos_start)
            elif op_str == '@&@':
                return my_Token(T_AND, pos_start=pos_start)
            elif op_str == '@|@':
                return my_Token(T_OR, pos_start=pos_start)

        return None  # This is not a valid operator
