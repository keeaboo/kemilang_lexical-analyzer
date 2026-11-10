import os
import sys
from lexer import Lexer
from tokens import TokenType

DEFAULT_SAMPLE = """
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


def print_token_table(tokens):
    """Renders scanned tokens in a formatted ASCII table."""
    header_line = f"+{'-'*32}+{'-'*25}+{'-'*8}+{'-'*8}+"
    print("\n" + header_line)
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

    print(header_line + "\n")


def get_typed_input() -> str:
    """Collects multi-line KemiLang source code from standard terminal input."""
    print("\n--- Enter KemiLang Code ---")
    print("Type or paste your code below.")
    print("Type 'RUN' on a new line and press Enter when finished:\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "RUN":
                break
            lines.append(line)
        except EOFError:
            break
            
    return "\n".join(lines)


def get_file_input() -> str:
    """Prompts for a file path and reads its content."""
    print("\n--- Load KemiLang Code File ---")
    file_path = input("Enter file path (e.g., test.txt or script.kemi): ").strip()
    
    # Remove quotes if user drag-and-dropped the file path
    file_path = file_path.strip("'\"")

    if not os.path.exists(file_path):
        print(f"\n[Error] File '{file_path}' not found.")
        return ""
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"\n[Error] Failed to read file: {e}")
        return ""


def main():
    while True:
        print("=" * 45)
        print("      KEMILANG LEXICAL ANALYZER MENU")
        print("=" * 45)
        print("[1] Type / Paste KemiLang Code")
        print("[2] Load Code from File")
        print("[3] Run Default Sample Code")
        print("[4] Exit")
        print("=" * 45)

        choice = input("Select an option (1-4): ").strip()

        code = ""
        if choice == "1":
            code = get_typed_input()
        elif choice == "2":
            code = get_file_input()
        elif choice == "3":
            print("\n--- Running Default KemiLang Sample Input ---")
            code = DEFAULT_SAMPLE
        elif choice == "4":
            print("\nExiting KemiLang Lexical Analyzer. Goodbye!")
            sys.exit(0)
        else:
            print("\n[Invalid Selection] Please choose 1, 2, 3, or 4.\n")
            continue

        if not code.strip():
            print("[Notice] Input code is empty. Returning to main menu.\n")
            continue

        # Execute Lexer scanning
        lexer = Lexer(code)
        tokens = lexer.scan_tokens()
        print_token_table(tokens)


if __name__ == "__main__":
    main()