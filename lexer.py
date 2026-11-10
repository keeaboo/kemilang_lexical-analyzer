# ==========================================
# KEMILANG LEXICAL SPECIFICATIONS
# ==========================================

KemiLang_Character_Set = {
    "UPPERCASE_LETTERS": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "LOWERCASE_LETTERS": list("abcdefghijklmnopqrstuvwxyz"),
    "DIGITS": list("0123456789"),
    "WHITESPACE": [' ', '\t', '\n', '\r']
}


KemiLang_Symbols = {
    "COMMENT": ['#*', '*#', '#'],

    "ASSIGNMENT_OPERATOR": ['='],

    "MATHEMATICAL_OPERATOR": [
        '^', '+', '-', '*', '/', '%'
    ],

    "LOGICAL_OPERATOR": [
        '!', '&&', '||'
    ],

    "RELATIONAL_OPERATOR": [
        '>', '<', '>=', '<=', '==', '!='
    ],

    "DELIMITER": [
        '[', ']', '{', '}', '(', ')'
    ],

    "PUNCTUATION": [
        '.', ';'
    ],

    "STRING_DELIMITER": ['"']
}


KemiLang_Keywords = {
    "PROGRAM_STATEMENT": [
        'calc', 'show', 'set',
        'increase', 'decrease', 'scale'
    ],

    "DECLARATION_KEYWORD": [
        'number', 'mass', 'vol', 'mole',
        'conc', 'temp', 'element',
        'compound', 'sample'
    ],

    "CONTROL_FLOW": [
        'when', 'otherwise', 'repeat', 'until'
    ],

    "CHEM_OPERATOR": [
        'react', 'yield', 'bal',
        'convert', 'to', 'into', 'by'
    ]
}


KemiLang_Reserved_Words = {
    "FUNCTION": [
        'formula', 'atoms', 'molar_mass',
        'check', 'roundup', 'rounddown'
    ],

    "MEASUREMENT_SYMBOL": [
        'g', 'kg', 'mg', 'L', 'mL',
        'mol', 'mol/L', 'K', '°C', 'kPa'
    ]
}

# Lexer
class Lexer:

    def __init__(self, source_code):

        self.source = source_code

        self.position = 0
        self.line = 1
        self.column = 1

        self.tokens = []
        self.errors = []

    # --------------------------------------
    # BASIC SCANNER FUNCTIONS
    # --------------------------------------

    def current_char(self):

        if self.position >= len(self.source):
            return None

        return self.source[self.position]


    def peek(self, offset=1):

        position = self.position + offset

        if position >= len(self.source):
            return None

        return self.source[position]


    def advance(self):

        char = self.current_char()

        if char is None:
            return None

        self.position += 1

        if char == '\n':
            self.line += 1
            self.column = 1

        else:
            self.column += 1

        return char


    def create_token(self, token_type, value, line, column):

        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }


    def add_token(self, token_type, value, line, column):

        token = self.create_token(
            token_type, value, line, column
        )

        self.tokens.append(token)
    
    # --------------------------------------
    # CHARACTER RECOGNITION
    # --------------------------------------

    def is_letter(self, char):

        return (
            char in KemiLang_Character_Set["UPPERCASE_LETTERS"]
            or
            char in KemiLang_Character_Set["LOWERCASE_LETTERS"]
        )


    def is_digit(self, char):

        return char in KemiLang_Character_Set["DIGITS"]


    def is_whitespace(self, char):

        return char in KemiLang_Character_Set["WHITESPACE"]


    def is_identifier_char(self, char):

        return (
            self.is_letter(char)
            or self.is_digit(char)
            or char == '_'
        )
    
    # --------------------------------------
    # GENERAL TOKEN RECOGNITION
    # --------------------------------------

    def scan_identifier(self):

        start_line = self.line
        start_column = self.column

        lexeme = ""

        while (
            self.current_char() is not None
            and self.is_identifier_char(self.current_char())
        ):

            lexeme += self.advance()

        # Check reserved keywords

        for category, words in KemiLang_Keywords.items():

            if lexeme in words:

                self.add_token(
                    category,
                    lexeme,
                    start_line,
                    start_column
                )

                return

        # Check reserved functions

        if lexeme in KemiLang_Reserved_Words["FUNCTION"]:

            self.add_token(
                "FUNCTION",
                lexeme,
                start_line,
                start_column
            )

            return

        # Check chemical formula or element symbol

        if self.is_valid_chemical_formula(lexeme):

            if self.is_element_symbol(lexeme):

                token_type = "ELEMENT_SYMBOL"

            else:

                token_type = "CHEMICAL_FORMULA"

            self.add_token(
                token_type,
                lexeme,
                start_line,
                start_column
            )

            return

        # Otherwise, classify as identifier

        self.add_token(
            "IDENTIFIER",
            lexeme,
            start_line,
            start_column
        )

    def scan_number(self):

        start_line = self.line
        start_column = self.column

        lexeme = ""

        has_decimal = False

        while (
            self.current_char() is not None
            and self.is_digit(self.current_char())
        ):

            lexeme += self.advance()

        # Check for decimal point

        if (
            self.current_char() == '.'
            and self.peek() is not None
            and self.is_digit(self.peek())
        ):

            has_decimal = True

            lexeme += self.advance()

            while (
                self.current_char() is not None
                and self.is_digit(self.current_char())
            ):

                lexeme += self.advance()

        if has_decimal:

            token_type = "FLOAT_LITERAL"

        else:

            token_type = "INTEGER_LITERAL"

        self.add_token(
            token_type,
            lexeme,
            start_line,
            start_column
        )

    # --------------------------------------
    # CHEMISTRY-SPECIFIC RECOGNITION
    # --------------------------------------

    ELEMENT_SYMBOLS = {
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O',
        'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S',
        'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr',
        'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',
        'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr',
        'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh',
        'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te',
        'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr',
        'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
        'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
        'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr',
        'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu',
        'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md',
        'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs',
        'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
        'Lv', 'Ts', 'Og'
    }


    def is_element_symbol(self, lexeme):

        return lexeme in self.ELEMENT_SYMBOLS


    def is_valid_chemical_formula(self, lexeme):

        if not lexeme:
            return False

        i = 0

        while i < len(lexeme):

            # Every element must start with uppercase

            if not (
                'A' <= lexeme[i] <= 'Z'
            ):

                return False

            symbol = lexeme[i]

            i += 1


            # Check for optional lowercase letter

            if (
                i < len(lexeme)
                and 'a' <= lexeme[i] <= 'z'
            ):

                symbol += lexeme[i]

                i += 1


            # Validate element symbol

            if symbol not in self.ELEMENT_SYMBOLS:

                return False


            # Check optional numerical subscript

            while (
                i < len(lexeme)
                and self.is_digit(lexeme[i])
            ):

                i += 1


        return True


    def scan_unit(self):

        start_line = self.line
        start_column = self.column

        units = KemiLang_Reserved_Words["MEASUREMENT_SYMBOL"]

        # Check longer units before shorter ones

        for unit in sorted(units, key=len, reverse=True):

            if self.source.startswith(unit, self.position):

                end_position = self.position + len(unit)

                # Ensure the unit is not part of a longer identifier

                if (
                    end_position < len(self.source)
                    and self.is_identifier_char(self.source[end_position])
                ):

                    continue

                for _ in unit:
                    self.advance()

                self.add_token(
                    "MEASUREMENT_SYMBOL",
                    unit,
                    start_line,
                    start_column
                )

                return True

        return False

    # --------------------------------------
    # OPERATORS AND SYMBOLS
    # --------------------------------------

    def scan_operator(self):

        start_line = self.line
        start_column = self.column

        operators = []

        for category, symbols in KemiLang_Symbols.items():

            if category.endswith("_OPERATOR"):

                for symbol in symbols:

                    operators.append((symbol, category))


        # Recognize longer operators first

        operators.sort(
            key=lambda item: len(item[0]),
            reverse=True
        )


        for operator, category in operators:

            if self.source.startswith(operator, self.position):

                for _ in operator:
                    self.advance()

                self.add_token(
                    category,
                    operator,
                    start_line,
                    start_column
                )

                return True

        return False


    def scan_symbol(self):

        char = self.current_char()

        start_line = self.line
        start_column = self.column

        for category in ["DELIMITER", "PUNCTUATION"]:

            if char in KemiLang_Symbols[category]:

                self.advance()

                self.add_token(
                    category,
                    char,
                    start_line,
                    start_column
                )

                return True

        return False


    # --------------------------------------
    # STRING RECOGNITION
    # --------------------------------------

    def scan_string(self):

        start_line = self.line
        start_column = self.column

        lexeme = ""

        # Consume opening quotation mark

        lexeme += self.advance()

        while self.current_char() is not None:

            char = self.current_char()

            # Closing quotation mark

            if char == '"':

                lexeme += self.advance()

                self.add_token(
                    "STRING_LITERAL",
                    lexeme,
                    start_line,
                    start_column
                )

                return


            # Handle escaped characters

            if char == '\\':

                lexeme += self.advance()

                if self.current_char() is not None:

                    lexeme += self.advance()

                continue


            # Multiline strings are not supported yet

            if char == '\n':

                break


            lexeme += self.advance()


        self.errors.append({
            "value": lexeme,
            "line": start_line,
            "column": start_column,
            "message": "Unterminated string literal"
        })


    # --------------------------------------
    # COMMENT RECOGNITION
    # --------------------------------------

    def scan_comment(self):

        start_line = self.line
        start_column = self.column

        # Block comment: #* ... *#

        if self.source.startswith('#*', self.position):

            self.advance()
            self.advance()

            while self.current_char() is not None:

                if self.source.startswith('*#', self.position):

                    self.advance()
                    self.advance()

                    return

                self.advance()


            self.errors.append({
                "value": "#*",
                "line": start_line,
                "column": start_column,
                "message": "Unterminated block comment"
            })

            return


        # Single-line comment: # ...

        if self.current_char() == '#':

            while (
                self.current_char() is not None
                and self.current_char() != '\n'
            ):

                self.advance()

            return

        return
    
    # --------------------------------------
    # MAIN SCANNING LOOP
    # --------------------------------------

    def scan_tokens(self):

        while self.current_char() is not None:

            char = self.current_char()


            # 1. Skip whitespace

            if self.is_whitespace(char):

                self.advance()

                continue


            # 2. Recognize comments

            if char == '#':

                self.scan_comment()

                continue


            # 3. Recognize strings

            if char == '"':

                self.scan_string()

                continue


            # 4. Recognize measurement units

            if self.scan_unit():

                continue


            # 5. Recognize identifiers, keywords, and formulas

            if self.is_letter(char) or char == '_':

                self.scan_identifier()

                continue


            # 6. Recognize numbers

            if self.is_digit(char):

                self.scan_number()

                continue


            # 7. Recognize operators

            if self.scan_operator():

                continue


            # 8. Recognize delimiters and punctuation

            if self.scan_symbol():

                continue


            # 9. Handle unexpected characters

            start_line = self.line
            start_column = self.column

            invalid_char = self.advance()

            self.errors.append({
                "value": invalid_char,
                "line": start_line,
                "column": start_column,
                "message": "Unrecognized character"
            })


        return self.tokens, self.errors
   
    
# ==========================================
# TOKEN TABLE DISPLAY
# ==========================================

def display_tokens(tokens):

    headers = ["LEXEME", "TOKEN", "LINE", "COLUMN"]

    rows = []

    for token in tokens:

        rows.append([
            token["value"],
            token["type"],
            token["line"],
            token["column"]
        ])


    # Determine column widths

    widths = []

    for i, header in enumerate(headers):

        max_width = max(
            [len(str(row[i])) for row in rows] + [len(header)]
        )

        widths.append(max_width)


    # Print header

    header_row = " | ".join(
        headers[i].ljust(widths[i])
        for i in range(len(headers))
    )

    separator = "-+-".join(
        "-" * width for width in widths
    )

    print("\n" + header_row)

    print(separator)


    # Print token rows

    for row in rows:

        print(
            " | ".join(
                str(row[i]).ljust(widths[i])
                for i in range(len(row))
            )
        )


    if not tokens:

        print("No tokens found.")


def display_errors(errors):

    if not errors:
        print("\nNo lexical errors found.")
        return

    print("\nLEXICAL ERRORS")
    print("-" * 65)

    for error in errors:

        print(
            f"[Line {error['line']}, "
            f"Column {error['column']}] "
            f"{error['message']}: {error['value']}"
        )