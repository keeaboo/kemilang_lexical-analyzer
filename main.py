from lexer import Lexer, display_tokens, display_errors


def main():

    print("====================================")
    print("       KEMILANG LEXICAL ANALYZER")
    print("====================================")

    print("[1] Enter source code")
    print("[2] Read source code from file")

    choice = input("\nSelect an option: ")


    # Direct user input

    if choice == "1":

        print("\nEnter your KemiLang code.")
        print("Type END on a separate line to finish.\n")

        lines = []

        while True:

            line = input()

            if line == "END":
                break

            lines.append(line)

        source_code = "\n".join(lines)


    # Read source file

    elif choice == "2":

        file_path = input("\nEnter file path: ")

        try:

            with open(file_path, "r", encoding="utf-8") as file:

                source_code = file.read()

        except FileNotFoundError:

            print("Error: File not found.")
            return

        except OSError as error:

            print(f"Error reading file: {error}")
            return


    else:

        print("Invalid option.")
        return


    # Perform lexical analysis

    lexer = Lexer(source_code)

    tokens, errors = lexer.scan_tokens()


    # Display results

    print("\n====================================")
    print("          SCANNING RESULTS")
    print("====================================")

    display_tokens(tokens)

    display_errors(errors)


if __name__ == "__main__":

    main()