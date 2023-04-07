from exec import Lexer, Parser, Interpreter
from resources import Context

if __name__ == "__main__":
    while True:
        text = input("LimeLang > ")

        # Generate Tokens
        lexer: Lexer = Lexer(filename="<stdin>", text=text)
        tokens, error = lexer.make_tokens()

        if error:
            print(error.as_string())
            break

        # Generate AST
        parser: Parser = Parser(tokens)
        ast = parser.parse()

        if ast.error:
            print(ast.error.as_string())
            break

        # Run Program
        interpreter: Interpreter = Interpreter()
        context: Context = Context("<program>")
        result = interpreter.visit(ast.node, context)

        if result.error:
            print(result.error.as_string())
            break

        print(result.value)
