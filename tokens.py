"""
Token Definitions and Specifications for KemiLang Lexical Analyzer.
"""

from enum import Enum, auto

class TokenType(Enum):
    # Literals & Identifiers
    IDENTIFIER = auto()
    NUMERIC_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()

    # Keywords & Reserved Words
    PROGRAM_KEYWORD = auto()
    DECLARATION_KEYWORD = auto()
    CONTROL_FLOW_KEYWORD = auto()
    CHEM_OPERATOR_KEYWORD = auto()
    BUILTIN_FUNCTION = auto()
    MEASUREMENT_SYMBOL = auto()
    NOISE_WORD = auto()

    # Operators
    ARITHMETIC_OPERATOR = auto()
    RELATIONAL_OPERATOR = auto()
    LOGICAL_OPERATOR = auto()
    ASSIGNMENT_OPERATOR = auto()

    # Separators & Comments
    DELIMITER = auto()
    PUNCTUATION = auto()
    COMMENT = auto()

    # Special
    EOF = auto()
    ERROR = auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int, column: int):
        self.type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type.name}, '{self.lexeme}', Line:{self.line}, Col:{self.column})"


# Symbol and Keyword Lookup Tables
KEMILANG_KEYWORDS = {
    # Declarations
    "number": TokenType.DECLARATION_KEYWORD,
    "mass": TokenType.DECLARATION_KEYWORD,
    "vol": TokenType.DECLARATION_KEYWORD,
    "volume": TokenType.DECLARATION_KEYWORD,
    "mole": TokenType.DECLARATION_KEYWORD,
    "conc": TokenType.DECLARATION_KEYWORD,
    "concentration": TokenType.DECLARATION_KEYWORD,
    "temp": TokenType.DECLARATION_KEYWORD,
    "temperature": TokenType.DECLARATION_KEYWORD,
    "element": TokenType.DECLARATION_KEYWORD,
    "compound": TokenType.DECLARATION_KEYWORD,
    "sample": TokenType.DECLARATION_KEYWORD,
    "boolean": TokenType.DECLARATION_KEYWORD,

    # Program Statements
    "calc": TokenType.PROGRAM_KEYWORD,
    "calculate": TokenType.PROGRAM_KEYWORD,
    "show": TokenType.PROGRAM_KEYWORD,
    "set": TokenType.PROGRAM_KEYWORD,
    "increase": TokenType.PROGRAM_KEYWORD,
    "decrease": TokenType.PROGRAM_KEYWORD,
    "scale": TokenType.PROGRAM_KEYWORD,

    # Control Flow
    "when": TokenType.CONTROL_FLOW_KEYWORD,
    "otherwise": TokenType.CONTROL_FLOW_KEYWORD,
    "repeat": TokenType.CONTROL_FLOW_KEYWORD,
    "until": TokenType.CONTROL_FLOW_KEYWORD,

    # Chemistry Operators
    "react": TokenType.CHEM_OPERATOR_KEYWORD,
    "yield": TokenType.CHEM_OPERATOR_KEYWORD,
    "bal": TokenType.CHEM_OPERATOR_KEYWORD,
    "balance": TokenType.CHEM_OPERATOR_KEYWORD,
    "convert": TokenType.CHEM_OPERATOR_KEYWORD,
    "to": TokenType.CHEM_OPERATOR_KEYWORD,
    "into": TokenType.CHEM_OPERATOR_KEYWORD,
    "by": TokenType.CHEM_OPERATOR_KEYWORD,
}

KEMILANG_RESERVED = {
    # Built-in Functions
    "formula": TokenType.BUILTIN_FUNCTION,
    "atoms": TokenType.BUILTIN_FUNCTION,
    "molar_mass": TokenType.BUILTIN_FUNCTION,
    "check": TokenType.BUILTIN_FUNCTION,
    "roundup": TokenType.BUILTIN_FUNCTION,
    "rounddown": TokenType.BUILTIN_FUNCTION,

    # Measurement Symbols
    "g": TokenType.MEASUREMENT_SYMBOL,
    "kg": TokenType.MEASUREMENT_SYMBOL,
    "mg": TokenType.MEASUREMENT_SYMBOL,
    "L": TokenType.MEASUREMENT_SYMBOL,
    "mL": TokenType.MEASUREMENT_SYMBOL,
    "mol": TokenType.MEASUREMENT_SYMBOL,
    "mol/L": TokenType.MEASUREMENT_SYMBOL,
    "g/mol": TokenType.MEASUREMENT_SYMBOL,
    "K": TokenType.MEASUREMENT_SYMBOL,
    "°C": TokenType.MEASUREMENT_SYMBOL,
    "kPa": TokenType.MEASUREMENT_SYMBOL,

    # Noise Words
    "goto": TokenType.NOISE_WORD,
}

KEMILANG_BOOLEANS = {
    "true": TokenType.BOOLEAN_LITERAL,
    "false": TokenType.BOOLEAN_LITERAL,
}