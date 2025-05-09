from antlr4 import *

from tree.tree import TreeVisitor
from generated.PythonLexer import PythonLexer
from generated.PythonParser import PythonParser
from generated.PythonParserListener import PythonParserListener


def test(data):
    input_data = InputStream(data)
    lexer = PythonLexer(input_data)
    stream = CommonTokenStream(lexer)
    parser = PythonParser(stream)
    tree = parser.file_input()
    visitor = TreeVisitor()
    return visitor.visit(tree)


if __name__ == '__main__':
    with open("./tests/test.py", 'r') as testfile:
        print(test(testfile.read()))
