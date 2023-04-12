from exec import Lexer, Parser, Interpreter
from resources import Context, SymbolTable
from values import Number, BuiltInFunction
import time
import sys
import os

# pyinstaller --onefile -n lime main.py

if __name__ == "__main__":
    global_symbol_table = SymbolTable()
    global_symbol_table.set("null", Number(0))
    global_symbol_table.set("True", Number(1))
    global_symbol_table.set("False", Number(0))

    global_symbol_table.set("print", BuiltInFunction("print"))
    global_symbol_table.set("print_ret", BuiltInFunction("print_ret"))
    global_symbol_table.set("input", BuiltInFunction("input"))
    global_symbol_table.set("input_int", BuiltInFunction("int_input"))
    global_symbol_table.set("clear", BuiltInFunction("clear"))
    global_symbol_table.set("is_num", BuiltInFunction("is_number"))
    global_symbol_table.set("is_str", BuiltInFunction("is_string"))
    global_symbol_table.set("is_list", BuiltInFunction("is_list"))
    global_symbol_table.set("is_fun", BuiltInFunction("is_function"))
    global_symbol_table.set("append", BuiltInFunction("append"))
    global_symbol_table.set("pop", BuiltInFunction("pop"))
    global_symbol_table.set("extend", BuiltInFunction("extend"))
    global_symbol_table.set("len", BuiltInFunction("len"))

    def run():
        filename = "test.ll"
        if len(sys.argv) > 1:
            filename = sys.argv[1]

        with open(os.path.abspath(filename), "r") as f:
            script = f.read()

        st = time.time()
        lexer: Lexer = Lexer(filename=filename, text=script)
        tokens, error = lexer.make_tokens()
        if error:
            print(error.as_string())
            return

        parser: Parser = Parser(tokens)
        ast = parser.parse()

        if ast.error:
            print(ast.error.as_string())
            return

        interpreter: Interpreter = Interpreter()
        context: Context = Context("<program>")
        context.symbol_table = global_symbol_table
        result = interpreter.visit(ast.node, context)

        if result.error:
            print(result.error.as_string())

        print(f"\nExecuted in: {time.time() - st} sec.")

    run()
