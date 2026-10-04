from language_types.tokens import Token, TokenType

def parse_word(tokens_arr, code, i):
    name = ""
    while (i < len(code)) and (code[i].isalnum() or code[i] == '_'):
        name += code[i]
        i += 1
    match name:
        case "var":
            tokens_arr.append(Token(TokenType.VAR, name))
        case "loop":
            tokens_arr.append(Token(TokenType.LOOP, name))
        case "end":
            tokens_arr.append(Token(TokenType.END, name))
        case "if":
            tokens_arr.append(Token(TokenType.IF, name))
        case "else":
             tokens_arr.append(Token(TokenType.ELSE, name))
        case "function":
            tokens_arr.append(Token(TokenType.FUNCTION, name))
        case "jumpback":
            tokens_arr.append(Token(TokenType.JUMPBACK, name))
        case "print":
            tokens_arr.append(Token(TokenType.PRINT, name))
        case "true":
            tokens_arr.append(Token(TokenType.TRUE, name))
        case "false":
            tokens_arr.append(Token(TokenType.FALSE, name))
        case _:
            tokens_arr.append(Token(TokenType.IDENTIFIER, name))
    return i

def parse_number(tokens_arr, code, i):
    number = ""
    while i < len(code) and code[i].isdigit():
        number += code[i]
        i += 1
    num = Token(TokenType.NUMBER, number)
    tokens_arr.append(num)
    return i

def parse_character(tokens_arr, token_type, code, i):
    character = Token(token_type, code[i])
    tokens_arr.append(character)
    return i + 1

def parse_operator(tokens_arr, code, i):
    if i + 1 < len(code) and code[i + 1] == '=':
        operator = ""
        operator += code[i] + code[i + 1]
        character = Token(TokenType.OPERATOR, operator)
        tokens_arr.append(character)
        return i + 2
    else:
        character = Token(TokenType.OPERATOR, code[i])
        tokens_arr.append(character)
        return i + 1

def tokenize(code):
    tokens_arr = []
    i = 0
    while i < len(code):
        if code[i] == '\n':
            i = parse_character(tokens_arr, TokenType.NEWLINE, code, i)
            continue
        if code[i].isspace():
            i += 1
            continue
        if code[i].isdigit():
            i = parse_number(tokens_arr, code, i)
            continue
        if is_binop(code[i]):
            i = parse_operator(tokens_arr, code, i)
            continue
        if code[i].isalpha():
            i = parse_word(tokens_arr, code, i)
            continue
        if code[i] == '=':
            if code[i+1] == '=':
                i = parse_operator(tokens_arr, code, i)
            else:
                i = parse_character(tokens_arr, TokenType.EQUALS, code, i)
            continue
        if code[i] == '[':
            i = parse_character(tokens_arr, TokenType.LEFT_BRACKET, code, i)
            continue
        if code[i] == ']':
            i = parse_character(tokens_arr, TokenType.RIGHT_BRACKET, code, i)
            continue
        if code[i] == ',':
            i = parse_character(tokens_arr, TokenType.COMMA, code, i)
            continue
        if code[i] == '(':
            i = parse_character(tokens_arr, TokenType.LEFT_PARENTHESES, code, i)
            continue
        if code[i] == ')':
            i = parse_character(tokens_arr, TokenType.RIGHT_PARENTHESES, code, i)
            continue

    return tokens_arr

def is_binop(character):
    if (character == '+' or character == '-' or character == '*' or character == '/'
            or character == '>' or character == '<'):
        return True
    return False

def is_arithmetic_binop(character):
    if (character == '+' or character == '-' or character == '*' or character == '/'):
        return True
    return False