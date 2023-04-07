from exec import Lexer, Parser, Interpreter
from resources import Context, SymbolTable, Number

if __name__ == "__main__":
    global_symbol_table = SymbolTable()
    global_symbol_table.set("null", Number(0))

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
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)

        if result.error:
            print(result.error.as_string())
            break

        print(result.value)
