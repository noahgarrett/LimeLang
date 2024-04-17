from Lexer import Lexer
from Parser import Parser
from Compiler import Compiler
from AST import Program
import json
import time
from argparse import ArgumentParser, Namespace, ArgumentError

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float

# pyinstaller --onefile --name lime main.py

def parse_arguments() -> Namespace:
    arg_parser: ArgumentParser = ArgumentParser(
        description="LimeLang v0.0.1-alpha"
    )
    # Required Arguments
    arg_parser.add_argument("file_path", type=str, help="Path to your entry point lime file (ex. `main.lime`)")

    return arg_parser.parse_args()


LEXER_DEBUG: bool = False
PARSER_DEBUG: bool = False
COMPILER_DEBUG: bool = False
RUN_CODE: bool = True

if __name__ == '__main__':
    args = parse_arguments()

    # Read from input file
    with open(args.file_path, "r") as f:
        code: str = f.read()

    if LEXER_DEBUG:
        print("===== LEXER DEBUG =====")
        debug_lex: Lexer = Lexer(source=code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())

    l: Lexer = Lexer(source=code)
    p: Parser = Parser(lexer=l)

    program: Program = p.parse_program()
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)

    if PARSER_DEBUG:
        print("===== PARSER DEBUG =====")
        with open("debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent=4)
        print("Wrote AST to debug/ast.json successfully")

    c: Compiler = Compiler()
    c.compile(node=program)

    # Output steps
    module: ir.Module = c.module
    module.triple = llvm.get_default_triple()

    if COMPILER_DEBUG:
        with open("debug/ir.ll", "w") as f:
            f.write(str(module))

    if len(c.errors) > 0:
        print(f"==== COMPILER ERRORS ====")
        for err in c.errors:
            print(err)
        exit(1)

    if RUN_CODE:
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        try:
            llvm_ir_parsed = llvm.parse_assembly(str(module))
            llvm_ir_parsed.verify()
        except Exception as e:
            print(e)
            raise

        target_machine = llvm.Target.from_default_triple().create_target_machine()

        engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
        engine.finalize_object()

        # Run the function with the name 'main'. This is the entry point function of the entire program
        entry = engine.get_function_address('main')
        cfunc = CFUNCTYPE(c_int)(entry)

        st = time.time()

        result = cfunc()

        et = time.time()

        print(f'\n\nProgram returned: {result}\n=== Executed in {round((et - st) * 1000, 6)} ms. ===')
