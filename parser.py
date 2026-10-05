from language_types.tokens import TokenType
from language_types.nodes import NodeTypes, ASTNode

def parse_program(tokens_arr):
    statements = []
    i = 0
    while i < len(tokens_arr):
        match tokens_arr[i].type:
            case TokenType.NEWLINE:
                i += 1
                continue
            case TokenType.VAR:
                end = find_token_type(tokens_arr, TokenType.NEWLINE, i) - 1
                statement = parse_assignment(tokens_arr, i, end, NodeTypes.ASSIGNMENT)
                statements.append(statement)
                i = end + 1
                continue
            case TokenType.IDENTIFIER:
                end = find_token_type(tokens_arr, TokenType.NEWLINE, i) - 1
                if tokens_arr[i + 1].type != TokenType.LEFT_PARENTHESES:
                    statements.append(parse_assignment(tokens_arr, i - 1, end, NodeTypes.REASSIGNMENT))
                else:
                    statements.append(parse_expression(tokens_arr, i, end))
                i = end + 1
                continue
            case TokenType.LOOP:
                end = find_matching_end(tokens_arr, i)
                statement = parse_loop(tokens_arr, i, end)
                statements.append(statement)
                i = end + 1
            case TokenType.IF:
                end = find_matching_end(tokens_arr, i)
                statement = parse_if_statement(tokens_arr, i, end)
                statements.append(statement)
                i = end + 1
            case TokenType.FUNCTION:
                end = find_matching_end(tokens_arr, i)
                statement = parse_function(tokens_arr, i, end)
                statements.append(statement)
                i = end + 1
            case TokenType.JUMPBACK:
                end = find_token_type(tokens_arr, TokenType.NEWLINE, i) - 1
                statement = parse_jumpback(tokens_arr, i, end)
                statements.append(statement)
                i = end + 1
            case TokenType.PRINT:
                end = find_token_type(tokens_arr, TokenType.NEWLINE, i) - 1
                statement = parse_print(tokens_arr, i, end)
                statements.append(statement)
                i = end + 1
                continue
            #INTERNAL USE CASE
            case TokenType.NUMBER:
                statements.append(parse_expression(tokens_arr, i, len(tokens_arr) - 1))
                break

    return statements

def parse_jumpback(tokens_arr, start, end):
    jumpback_expr = parse_expression(tokens_arr, start + 1, end)
    return ASTNode(NodeTypes.JUMPBACK, tokens_arr[start].value, None, jumpback_expr)

def find_matching_end(tokens_arr, start):
    depth = 1
    i = start + 1
    while i < len(tokens_arr):
        if tokens_arr[i].type == TokenType.IF or tokens_arr[i].type == TokenType.LOOP or tokens_arr[i].type == TokenType.FUNCTION:
            depth += 1
        if tokens_arr[i].type == TokenType.END:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None

def find_matching_else(tokens_arr, start, end):
    depth = 0
    for i in range(start + 1, end):
        t = tokens_arr[i].type
        if tokens_arr[i].type == TokenType.IF or tokens_arr[i].type == TokenType.LOOP or tokens_arr[i].type == TokenType.FUNCTION:
            depth += 1
        elif t == TokenType.END:
            depth -= 1
        elif t == TokenType.ELSE and depth == 0:
            return i
    return None

def find_token_type(tokens_arr, token_type, start, end=None):
    i = start
    if not end:
        end = len(tokens_arr)
    while i < end:
        if tokens_arr[i].type == token_type:
            return i
        i += 1
    return None

def parse_assignment(tokens_arr, start, end, node_type):
    left = ASTNode(NodeTypes.IDENTIFIER, tokens_arr[start + 1].value, None, None)

    right = parse_expression(tokens_arr, start + 3, end)
    node = ASTNode(node_type, tokens_arr[start + 2].value, left, right)
    return node

def parse_print(tokens_arr, start, end):
    right = parse_expression(tokens_arr, start + 1, end)
    return ASTNode(NodeTypes.PRINT, None, None, right)

def parse_if_statement(tokens_arr, start, end):
    new_line_token = find_token_type(tokens_arr, TokenType.NEWLINE, start)
    if_expr = parse_expression(tokens_arr, start + 1, new_line_token - 1)
    body_start = new_line_token + 1
    else_token = find_matching_else(tokens_arr, start, end)

    if else_token is None:
        if_statement = parse_program(tokens_arr[body_start:end])
        return ASTNode(NodeTypes.IF, if_expr, if_statement, None)

    if_statement = parse_program(tokens_arr[body_start:else_token])
    else_statement = parse_program(tokens_arr[else_token + 1:end])
    return ASTNode(NodeTypes.IF, if_expr, if_statement, else_statement)

def parse_function(tokens_arr, start, end):
    left_parentheses = find_token_type(tokens_arr, TokenType.LEFT_PARENTHESES, start)
    right_parentheses = find_token_type(tokens_arr, TokenType.RIGHT_PARENTHESES, start)
    statements = parse_program(tokens_arr[right_parentheses + 1:end])
    func_identifier = ASTNode(NodeTypes.IDENTIFIER, tokens_arr[start + 1].value, None, None)
    parameters = parse_list(tokens_arr, left_parentheses + 1, right_parentheses, TokenType.RIGHT_PARENTHESES)

    return ASTNode(NodeTypes.FUNCTION, parameters, func_identifier, statements)

def parse_list(tokens_arr, start, end, stop_token_condition):
    # Inclusive start, inclusive end
    elements = []
    i = start
    while i < end and tokens_arr[i].type != stop_token_condition:
        comma_index = i
        while (tokens_arr[comma_index].type != TokenType.COMMA) and (
                tokens_arr[comma_index].type != stop_token_condition):
            comma_index += 1
        elements.append(parse_expression(tokens_arr, i, comma_index - 1))
        i = comma_index + 1
    return ASTNode(NodeTypes.ARRAY, None, None, elements)

def parse_loop(tokens_arr, start, end):
    new_line = find_token_type(tokens_arr, TokenType.NEWLINE, start)
    loop_expr = parse_expression(tokens_arr, start + 1, new_line - 1)
    body_start = new_line + 1
    statements = parse_program(tokens_arr[body_start:end])

    return ASTNode(NodeTypes.LOOP, loop_expr, None, statements)

def parse_expression(tokens_arr, start, end):
    #inclusive end, inclusive start
    for i in range(end, start - 1, -1):
        if (tokens_arr[i].type == TokenType.OPERATOR) and (tokens_arr[i].value == '>' or tokens_arr[i].value == '<'
                                                           or tokens_arr[i].value == '>=' or tokens_arr[i].value == '<=' or tokens_arr[i].value == '=='):
            left = parse_expression(tokens_arr, start, i - 1)
            right = parse_expression(tokens_arr, i + 1, end)
            return ASTNode(NodeTypes.BINOP, tokens_arr[i].value, left, right)

    for i in range(end, start - 1, -1):
        if (tokens_arr[i].type == TokenType.OPERATOR) and (tokens_arr[i].value == '+' or tokens_arr[i].value == '-'):
            left = parse_expression(tokens_arr, start, i - 1)
            right = parse_expression(tokens_arr, i + 1, end)
            return ASTNode(NodeTypes.BINOP, tokens_arr[i].value, left, right)
    for i in range(end, start - 1, -1):
        if (tokens_arr[i].type == TokenType.OPERATOR) and (tokens_arr[i].value == '*' or tokens_arr[i].value == '/'):
            left = parse_expression(tokens_arr, start, i - 1)
            right = parse_expression(tokens_arr, i + 1, end)
            return ASTNode(NodeTypes.BINOP, tokens_arr[i].value, left, right)

    if tokens_arr[start].type == TokenType.NUMBER:
        return ASTNode(NodeTypes.NUMBER, tokens_arr[start].value, None, None)
    if tokens_arr[start].type == TokenType.IDENTIFIER:
        identifier_node = ASTNode(NodeTypes.IDENTIFIER, tokens_arr[start].value, None, None)
        return parse_postfix(identifier_node, tokens_arr, start + 1, end)
    if tokens_arr[start].type == TokenType.LEFT_BRACKET:
        right_bracket_index = start
        while right_bracket_index < end:
            if tokens_arr[right_bracket_index].type != TokenType.RIGHT_BRACKET:
                right_bracket_index += 1
            else:
                break
        array_node = parse_list(tokens_arr, start + 1, end, TokenType.RIGHT_BRACKET)
        return parse_postfix(array_node, tokens_arr, right_bracket_index + 1, end)
    if tokens_arr[start].type == TokenType.TRUE:
        return ASTNode(NodeTypes.TRUE, None, None, None)
    if tokens_arr[start].type == TokenType.FALSE:
        return ASTNode(NodeTypes.FALSE, None, None, None)

def parse_postfix(node, tokens_arr, start, end):
    #The start parameter starts at the first left bracket
    i = start
    while i < end:
        if tokens_arr[i].type == TokenType.LEFT_BRACKET:
            right_bracket = i
            while (tokens_arr[right_bracket].type != TokenType.RIGHT_BRACKET):
                right_bracket += 1
            node = ASTNode(NodeTypes.INDEX, parse_expression(tokens_arr, i + 1, right_bracket - 1), node, None)
            i = right_bracket + 1
            continue
        if tokens_arr[i].type == TokenType.LEFT_PARENTHESES:
            right_parentheses = i
            while (tokens_arr[right_parentheses].type != TokenType.RIGHT_PARENTHESES):
                right_parentheses += 1
            node = ASTNode(NodeTypes.FUNCTION_CALL, parse_list(tokens_arr, i + 1, right_parentheses, TokenType.RIGHT_PARENTHESES), node, None)
            i = right_parentheses + 1
            continue
        break
    return node