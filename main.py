import lexer

# source_code = input("Enter KemiLang code: ")
# sample_code = "calc total = 10 g + 5 g;"

sample_code = "calc"

tokens = lexer.tokenize(sample_code)

print(f"Lexeme: {sample_code} \t Token: {tokens}")