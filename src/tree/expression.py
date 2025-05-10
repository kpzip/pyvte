from abc import ABC, abstractmethod

from context.context import Context, ReturnValues
from context.context_stack import ContextStack
from value.value import Value


class Expression(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self, context_stack: ContextStack) -> Value:
        pass


class TernaryExpression(Expression):

    def __init__(self, lhs: Expression, rhs: Expression, condition: Expression):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs
        self.condition = condition

    def __str__(self):
        return str(self.lhs) + " if " + str(self.condition) + " else " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        if self.condition.evaluate(context_stack).is_truthy():
            return self.lhs.evaluate(context_stack)
        else:
            return self.rhs.evaluate(context_stack)


class BinaryExpression(Expression, ABC):

    def __init__(self, lhs: Expression, rhs: Expression):
        super().__init__()
        self.lhs = lhs
        self.rhs = rhs


class UnaryExpression(Expression, ABC):

    def __init__(self, operand: Expression):
        super().__init__()
        self.operand = operand


class StarExpression(UnaryExpression):

    def __str__(self):
        return "*" + str(self.operand)


class StarExpressions:

    def __init__(self, exprs: list[StarExpression]):
        self.exprs = exprs

    def __str__(self):
        return ", ".join(map(str, self.exprs))


class OrExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " or " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool",
                     self.lhs.evaluate(context_stack).is_truthy() or self.rhs.evaluate(context_stack).is_truthy())


class AndExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " and " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool",
                     self.lhs.evaluate(context_stack).is_truthy() and self.rhs.evaluate(context_stack).is_truthy())


class NotExpression(UnaryExpression):

    def __str__(self):
        return "not " + str(self.operand)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool", not self.operand.evaluate(context_stack).is_truthy())


class BitOrExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " | " + str(self.rhs)


class BitAndExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " & " + str(self.rhs)


class BitXorExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " ^ " + str(self.rhs)


class ShrExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " >> " + str(self.rhs)


class ShlExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " << " + str(self.rhs)


class AddExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " + " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return self.lhs.evaluate(context_stack) + self.rhs.evaluate(context_stack)


class SubtractExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " - " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return self.lhs.evaluate(context_stack) - self.rhs.evaluate(context_stack)


class MultiplyExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " * " + str(self.rhs)


class DivideExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " / " + str(self.rhs)


class IntDivideExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " // " + str(self.rhs)


class RemainderExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " % " + str(self.rhs)


class MatmulExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " @ " + str(self.rhs)


class NegateExpression(UnaryExpression):

    def __str__(self):
        return "-" + str(self.operand)


class PositiveExpression(UnaryExpression):

    def __str__(self):
        return "+" + str(self.operand)


class BitNotExpression(UnaryExpression):

    def __str__(self):
        return "~" + str(self.operand)


class PowerExpression(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " ** " + str(self.rhs)


class TrueLiteral(Expression):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "True"

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool", True)


class FalseLiteral(Expression):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "False"

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool", False)


class NoneLiteral(Expression):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "None"

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value(None, None)


class Identifier(Expression):

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def evaluate(self, context_stack: ContextStack) -> Value:
        for frame in context_stack.traverse():
            if val := frame.defined_values.get(self.name):
                return val
        raise Exception(f"Attribute '{self.name}' Not Found! Call Stack:" + str(context_stack.stack[0].defined_values))


class StringLiteral(Expression):

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self):
        return f'"{self.value}"'


class NumericLiteral(Expression):

    def __init__(self, value: str):
        super().__init__()
        self.value = value

    def __str__(self):
        return str(self.value)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("int", int(self.value))


class EqComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " == " + str(self.rhs)

    def evaluate(self, context_stack: ContextStack) -> Value:
        return Value("bool", self.lhs.evaluate(context_stack) == self.rhs.evaluate(context_stack))


class NotEqComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " != " + str(self.rhs)


class LeComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " <= " + str(self.rhs)


class LtComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " < " + str(self.rhs)


class GeComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " >= " + str(self.rhs)


class GtComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " > " + str(self.rhs)


class NotInComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " not in " + str(self.rhs)


class InComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " in " + str(self.rhs)


class IsNotComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " is not " + str(self.rhs)


class IsComparison(BinaryExpression):

    def __str__(self):
        return str(self.lhs) + " is " + str(self.rhs)


class CallExpression(Expression):

    def __init__(self, name: Expression, params: list[Expression]):
        super().__init__()
        self.name = name
        self.params = params

    def __str__(self):
        return str(self.name) + "(" + ", ".join(map(str, self.params)) + ")"

    def evaluate(self, context_stack: ContextStack) -> Value:
        func: Value = self.name.evaluate(context_stack)
        if func.ty != "func":
            raise Exception("Cannot Call Non-Function!")
        func = func.val
        arguments = {}
        if len(self.params) != len(func.arguments):
            raise Exception("Too Many or Too Few Arguments")
        for i in range(len(func.arguments)):
            arguments[func.arguments[i].name] = self.params[i].evaluate(context_stack)

        context_stack.push(Context(defined_values=arguments))
        func.execute_internal(context_stack)
        ret: ReturnValues = context_stack.pop()
        context_stack.pop()
        return ret.value
