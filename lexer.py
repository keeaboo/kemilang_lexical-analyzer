from tokens import Token, TokenType, KEMILANG_KEYWORDS, KEMILANG_RESERVED, KEMILANG_BOOLEANS

class Lexer:
    def __init__(self, source_code: str):
        self.source = source_code
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.column = 1
        self.start_column = 1

    def scan_tokens(self) -> list[Token]:
        while not self._is_at_end():
            self.start = self.current
            self.start_column = self.column
            self._scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line, self.column))
        return self.tokens

    def _scan_token(self):
        c = self._advance()

        # Whitespace
        if c in [' ', '\r', '\t']:
            return
        elif c == '\n':
            self.line += 1
            self.column = 1
            return

        # Delimiters
        if c in ['(', ')', '[', ']', '{', '}']:
            self._add_token(TokenType.DELIMITER)
            return

        # Punctuation
        if c in [';', '.', '°']:
            self._add_token(TokenType.PUNCTUATION)
            return
        elif c == ',':
            self._add_token(TokenType.PUNCTUATION)
            return

        # Arithmetic Operators
        if c in ['+', '*', '%', '^']:
            self._add_token(TokenType.ARITHMETIC_OPERATOR)
            return
        elif c == '-':
            self._add_token(TokenType.ARITHMETIC_OPERATOR)
            return
        elif c == '/':
            self._add_token(TokenType.ARITHMETIC_OPERATOR)
            return

        # Logical & Relational & Assignment Operators
        if c == '=':
            if self._match('='):
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            else:
                self._add_token(TokenType.ASSIGNMENT_OPERATOR)
            return
        elif c == '!':
            if self._match('='):
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            else:
                self._add_token(TokenType.LOGICAL_OPERATOR)
            return
        elif c == '<':
            if self._match('='):
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            else:
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            return
        elif c == '>':
            if self._match('='):
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            else:
                self._add_token(TokenType.RELATIONAL_OPERATOR)
            return
        elif c == '&':
            if self._match('&'):
                self._add_token(TokenType.LOGICAL_OPERATOR)
            else:
                self._add_token(TokenType.ERROR, f"Unexpected single '&'")
            return
        elif c == '|':
            if self._match('|'):
                self._add_token(TokenType.LOGICAL_OPERATOR)
            else:
                self._add_token(TokenType.ERROR, f"Unexpected single '|'")
            return

        # Comments (# line comment, #* block comment *#)
        if c == '#':
            if self._match('*'):
                self._block_comment()
            else:
                self._line_comment()
            return

        # String Literals
        if c == '"':
            self._string()
            return

        # Numeric Literals
        if c.isdigit():
            self._number()
            return

        # Identifiers / Keywords / Composite Units
        if c.isalpha() or c == '_':
            self._identifier_or_keyword()
            return

        # Unrecognized Character
        self._add_token(TokenType.ERROR, f"Unrecognized character '{c}'")

    # Helper methods for scanning complex tokens
    def _identifier_or_keyword(self):
        while (self._peek().isalnum() or self._peek() in ['_', '/', '°']) and not self._is_at_end():
            # Special check for compound measurement units like mol/L or g/mol
            if self._peek() == '/' and not self._peek_next().isalpha():
                break
            self._advance()

        lexeme = self.source[self.start:self.current]

        # Categorize
        if lexeme in KEMILANG_KEYWORDS:
            self._add_token(KEMILANG_KEYWORDS[lexeme])
        elif lexeme in KEMILANG_RESERVED:
            self._add_token(KEMILANG_RESERVED[lexeme])
        elif lexeme in KEMILANG_BOOLEANS:
            self._add_token(KEMILANG_BOOLEANS[lexeme], lexeme == "true")
        else:
            if len(lexeme) > 30:
                self._add_token(TokenType.ERROR, f"Identifier '{lexeme}' exceeds max length of 30 characters")
            else:
                self._add_token(TokenType.IDENTIFIER)

    def _number(self):
        while self._peek().isdigit():
            self._advance()

        # Check for fractional part
        if self._peek() == '.' and self._peek_next().isdigit():
            self._advance()  # Consume the '.'
            while self._peek().isdigit():
                self._advance()

        lexeme = self.source[self.start:self.current]
        val = float(lexeme) if '.' in lexeme else int(lexeme)
        self._add_token(TokenType.NUMERIC_LITERAL, val)

    def _string(self):
        while self._peek() != '"' and not self._is_at_end():
            if self._peek() == '\n':
                self.line += 1
                self.column = 1
            self._advance()

        if self._is_at_end():
            self._add_token(TokenType.ERROR, "Unterminated string literal")
            return

        self._advance()  # Closing "
        lexeme = self.source[self.start:self.current]
        literal = self.source[self.start + 1:self.current - 1]
        self._add_token(TokenType.STRING_LITERAL, literal)

    def _line_comment(self):
        while self._peek() != '\n' and not self._is_at_end():
            self._advance()
        lexeme = self.source[self.start:self.current]
        self._add_token(TokenType.COMMENT, lexeme)

    def _block_comment(self):
        while not (self._peek() == '*' and self._peek_next() == '#') and not self._is_at_end():
            if self._peek() == '\n':
                self.line += 1
                self.column = 1
            self._advance()

        if self._is_at_end():
            self._add_token(TokenType.ERROR, "Unterminated block comment")
            return

        self._advance()  # consume '*'
        self._advance()  # consume '#'
        lexeme = self.source[self.start:self.current]
        self._add_token(TokenType.COMMENT, lexeme)

    # Pointer Navigation Helpers
    def _advance(self) -> str:
        ch = self.source[self.current]
        self.current += 1
        self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._is_at_end() or self.source[self.current] != expected:
            return False
        self.current += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        if self._is_at_end():
            return '\0'
        return self.source[self.current]

    def _peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def _is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def _add_token(self, token_type: TokenType, literal: object = None):
        lexeme = self.source[self.start:self.current]
        self.tokens.append(Token(token_type, lexeme, literal, self.line, self.start_column))