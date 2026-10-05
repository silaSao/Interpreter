from language_types.nodes import NodeTypes, ASTNode

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

scope_stack = [{}]

def evaluate(statements):
    for ast_node in statements:
        evaluate_node(ast_node)

def evaluate_node(ast_node):
    match ast_node.type:
        case NodeTypes.ASSIGNMENT | NodeTypes.REASSIGNMENT:
            name = ast_node.left.value
            value = evaluate_node(ast_node.right)
            scope_stack[-1][name] = value
            return scope_stack[-1][name]
        case NodeTypes.IDENTIFIER:
            if ast_node.value in scope_stack[-1]:
                return scope_stack[-1][ast_node.value]
            return scope_stack[0].get(ast_node.value)
        case NodeTypes.NUMBER:
            return int(ast_node.value)
        case NodeTypes.ARRAY:
            elements = []
            for element in ast_node.right:
                elements.append(evaluate_node(element))
            return elements
        case NodeTypes.INDEX:
            value = evaluate_node(ast_node.left)
            index = evaluate_node(ast_node.value)
            return value[index - 1]
        case NodeTypes.BINOP:
            left = evaluate_node(ast_node.left)
            right = evaluate_node(ast_node.right)
            match ast_node.value:
                case '+':
                    return left + right
                case '-':
                    return left - right
                case '*':
                    return left * right
                case '/':
                    return left / right
                case '>':
                    return left > right
                case '<':
                    return left < right
                case '>=':
                    return left >= right
                case '<=':
                    return left <= right
                case '==':
                    return left == right
        case NodeTypes.LOOP:
            i = evaluate_node(ast_node.value)
            if type(i) == int or type(i) == float:
                for x in range(int(i)):
                    for statement in ast_node.right:
                        evaluate_node(statement)
            else:
                while(evaluate_node(ast_node.value)):
                    for statement in ast_node.right:
                        evaluate_node(statement)
        case NodeTypes.IF:
            boolean = evaluate_node(ast_node.value)
            if boolean:
                for statement in ast_node.left:
                    evaluate_node(statement)
            else:
                if ast_node.right:
                    for statement in ast_node.right:
                        evaluate_node(statement)
        case NodeTypes.FUNCTION:
            name = ast_node.left.value
            scope_stack[0][name] = ast_node
            return scope_stack[0][name]
        case NodeTypes.FUNCTION_CALL:
            args = evaluate_node(ast_node.value)
            node = evaluate_node(ast_node.left)
            params = node.value.right
            scope_stack.append({})
            for i in range(len(args)):
                param_identifier = params[i].value
                scope_stack[-1][param_identifier] = args[i]

            return_value = None
            try:
                for statement in node.right:
                    evaluate_node(statement)
            except ReturnValue as ret:
                return_value = ret.value

            scope_stack.pop()
            return return_value
        case NodeTypes.JUMPBACK:
            value = evaluate_node(ast_node.right) if ast_node.right else None
            raise ReturnValue(value)
        case NodeTypes.PRINT:
            value = evaluate_node(ast_node.right)
            print(value)
        case NodeTypes.TRUE:
            return True
        case NodeTypes.FALSE:
            return False

