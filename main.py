import tokenizer
import parser
import evaluator

def main():
    source_code = """  
    print 6
    """

    tokens = tokenizer.tokenize(source_code)
    # print("Tokens length: ", len(tokens))
    # print("Tokens: ", tokens)
    statements = parser.parse_program(tokens)
    # print("Statements: ", statements[1].left.value)
    result = evaluator.evaluate(statements)
    # print("Result: ", result)

    # source_code_one_line = "\nvar x = 5\nloop 10\nx = x + 2\nend\n"
    # tokens = tokenizer.tokenize(source_code)
    # tokens_array = []
    # for token in tokens:
    #     tokens_array.append(token.type)
    # print(tokens_array)
    #
    # tokens2 = tokenizer.tokenize(source_code_one_line)
    # tokens2_array = []
    # for token in tokens2:
    #     tokens2_array.append(token.type)
    # print(tokens2_array)

main()