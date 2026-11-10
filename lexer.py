# Step 1: Read source code
# Step 2: Initialize the scanner
# Step 3: Examine the current character
# Step 4: Identify the complete lexeme
# Step 5: Classify the lexeme and token
# Step 6: Store the token
# Step 7: Repeat until the end of the source code

KemiLang_Character_Set = {
    "UPPERCASE_LETTERS": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
    "LOWERCASE_LETTERS": list("abcdefghijklmnopqrstuvwxyz"),
    "DIGITS": list("0123456789"),
    "WHITESPACE": [' ', '\t', '\n', '\r']
}

KemiLang_Symbols = {
    "COMMENT": ['#', '#*', '*#'],
    "ASSIGNMENT_OPERATOR": ['='],
    "MATHEMATICAL_OPERATOR": ['(', ')', '^', '+', '-', '*', '/', '%'],
    "LOGICAL_OPERATOR": ['!', '&&', '||'],
    "RELATIONAL_OPERATOR": ['>', '<', '>=', '<=', '==', '!='],
    "DELIMITER": ['[', ']', '{', '}', '(', ')'],
    "PUNCTUATION": ['.', ';','"', "°"] # hindi ba delimiter ang semicolon?
}

KemiLang_Keywords = {
    "PROGRAM_STATEMENT": ['calc', 'show', 'set', 'increase', 'decrease', 'scale'],
    "DECLARATION_KEYWORD": ['number', 'mass', 'vol', 'mole', 'conc', 'temp', 'element', 'compound', 'sample'],
    "CONTROL_FLOW": ['when', 'otherwise', 'repeat', 'until'],
    "CHEM_OPERATOR": ['react', 'yield', 'bal', 'convert', 'to', 'into', 'by']
}
KemiLang_Reserved_Words = {
    "FUNCTION": ['formula', 'atoms', 'molar_mass', 'check', 'roundup', 'rounddown'],
    "MEASUREMENT_SYMBOL": ['g', 'kg', 'mg', 'L', 'mL', 'mol', 'mol/L', 'K', '°C', 'kPa'],
}

# PROGRAM_STATEMENT = ['calc', 'show', 'set', 'increase', 'decrease', 'scale']

# def tokenize(word):
#     if word in PROGRAM_STATEMENT:
#         return "PROGRAM_STATEMENT"

