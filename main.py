"""
CLI Driver & Formatting Table Output for KemiLang Lexical Analyzer.
"""

import sys
from lexer import Lexer
from tokens import TokenType

def print_token_table(tokens):
    header_line = f"+{'-'*32}+{'-'*25}+{'-'*8}+{'-'*8}+"
    print(header_line)
    print(f"| {'LEXEME':<30} | {'TOKEN TYPE':<23} | {'LINE':<6} | {'COL':<6} |")
    print(header_line)

    for token in tokens:
        if token.type == TokenType.EOF:
            continue
        lexeme_disp = token.lexeme.replace('\n', '\\n').replace('\t', '\\t')
        if len(lexeme_disp) > 30:
            lexeme_disp = lexeme_disp[:27] + "..."
        type_disp = token.type.name
        print(f"| {lexeme_disp:<30} | {type_disp:<23} | {token.line:<6} | {token.column:<6} |")

    print(header_line)

def main():
    sample_code = """
# Chemical Mass Calculation Sample
mass sample_mass = 36 g;
compound water = H2O;

when (sample_mass > 20 g) {
    show sample_mass;
    show atoms(water);
    show molar_mass(water);
} otherwise {
    show "Below threshold";
}
*# Multi-line
   reaction check #*
react water_form = H2 + O2 yield H2O;
convert 500 mL to L into liquid_vol;
"""

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    else:
        print("--- Running Default KemiLang Sample Input ---\n")
        code = sample_code

    lexer = Lexer(code)
    tokens = lexer.scan_tokens()
    print_token_table(tokens)

if __name__ == "__main__":
    main()