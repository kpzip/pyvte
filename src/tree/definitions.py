from context.context import ReturnValues
from context.context_stack import ContextStack
from tree.expression import Identifier
from tree.statements import Statement, StatementList
from value.value import Value


class FuncDefinition(Statement):

    def __init__(self, name: Identifier, arguments: list[Identifier], code: StatementList):
        super().__init__()
        self.name = name
        self.arguments = arguments
        self.code = code

    def __str__(self):
        return "def " + str(self.name) + "(" + ", ".join(map(str, self.arguments)) + "):\n\t" + str(self.code).replace(
            "\n", "\n\t")

    def execute_internal(self, context_stack: ContextStack) -> bool:
        if not self.code.execute(context_stack):
            context_stack.push(ReturnValues(Value(None, None)))
        return False

    def execute(self, context_stack: ContextStack) -> bool:
        context_stack.peek().defined_values[self.name.name] = Value("func", self)
        return False
