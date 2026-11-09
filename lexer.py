# def tokenize(source_code):
#     # Tokenization logic goes here
#     tokens = []
#     # Example tokenization (this is just a placeholder)
#     for word in source_code.split():
#         tokens.append(word)
#     return tokens


# def tokenize(word):
#     token = []
#     for char in word:
#         if char.isalpha():
#             token
#         elif char.isdigit():
#             print(f"Token: {char} (Digit)")
#         else:
#             print(f"Token: {char} (Other)")


# Step 1: Read source code
# Step 2: Initialize the scanner
# Step 3: Examine the current character
# Step 4: Identify the complete lexeme
# Step 5: Classify the lexeme and token
# Step 6: Store the token
# Step 7: Repeat until the end of the source code


PROGRAM_STATEMENT = ['calc', 'show', 'set', 'increase', 'decrease', 'scale']



def tokenize(word):
    if word in PROGRAM_STATEMENT:
        return "PROGRAM_STATEMENT"