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

# pyinstaller --onefile --name lime --icon=assets/lime_icon.ico main.py

def parse_arguments() -> Namespace:
    arg_parser: ArgumentParser = ArgumentParser(
        description="LimeLang v0.0.3-alpha"
    )
    # Required Arguments
    arg_parser.add_argument("file_path", type=str, help="Path to your entry point lime file (ex. `main.lime`)")
    arg_parser.add_argument("--debug", action="store_true", help="Prints internal debug information")

    return arg_parser.parse_args()


LEXER_DEBUG: bool = False
PARSER_DEBUG: bool = False
COMPILER_DEBUG: bool = False
RUN_CODE: bool = True

PROD_DEBUG: bool = False

if __name__ == '__main__':
    args = parse_arguments()

    if args.debug:
        PROD_DEBUG = True

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

    parse_st: float = time.time()
    program: Program = p.parse_program()
    parse_et: float = time.time()
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
    compiler_st: float = time.time()
    c.compile(node=program)
    compiler_et: float = time.time()

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

        if PROD_DEBUG:
            print(f"\n\n=== Parsed in: {round((parse_et - parse_st) * 1000, 6)} ms. ===")
            print(f"=== Compiled in: {round((compiler_et - compiler_st) * 1000, 6)} ms. ===")
        print(f'=== Executed in {round((et - st) * 1000, 6)} ms. ===\n\nProgram returned: {result}')
