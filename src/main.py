import importlib
import importlib.util
import re
import sys

from antlr4 import *

import value.value
from context.context import Context
from context.context_stack import ContextStack
from generated.PythonLexer import PythonLexer
from generated.PythonParser import PythonParser
from tree.tree import TreeVisitor


def main(test_file: str, file_to_test: str):
    spec = importlib.util.spec_from_file_location("tests", test_file)
    tests = importlib.util.module_from_spec(spec)
    sys.modules["tests"] = tests
    spec.loader.exec_module(tests)

    with open(file_to_test, "r") as file:
        filedata = file.read()
    input_data = InputStream(filedata)
    lexer = PythonLexer(input_data)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    tree = parser.file_input()
    visitor = TreeVisitor()
    syntaxtree = visitor.visitFile_input(tree)

    module_context = Context()
    context = ContextStack([module_context])
    syntaxtree.execute(context)
    value.value.global_context = context

    to_test_name = re.split(r"[\\/]", file_to_test.rsplit('.', 1)[0])[-1]

    test_funcs = []

    for n in dir(tests):
        if n.startswith("test") and type(getattr(tests, n)) == type(main):
            test_funcs.append(n)

    for k, v in module_context.defined_values.items():
        setattr(tests, k, v)

    passed = 0
    failed = 0
    for f in test_funcs:
        try:
            getattr(tests, f)()
            passed += 1
        except Exception:
            print()
            failed += 1

    print("Tests Run:    " + str(passed + failed))
    print("Tests Passed: " + str(passed))
    print("Tests Failed: " + str(failed))
    print("Exiting...")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: `python3 main.py <Path to test file> <Path to file to test>")
    else:
        main(sys.argv[1], sys.argv[2])
