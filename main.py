import tokenizer
import parser
import evaluator

def main():
    source_code = """  
        function add(a, b)
            jumpback a + b
        end
        print add(2, 3)
        
        var total = 0
        var i = 1
        loop 5
            total = total + i
            i = i + 1
        end
        print total
    
        var nums = [10, 20, 30]
        print nums[1]
    """

    tokens = tokenizer.tokenize(source_code)
    statements = parser.parse_program(tokens)
    result = evaluator.evaluate(statements)


main()