import tree

global_context = None


class Value:

    def __init__(self, ty: str | None, val: None | str | bool | int | float | list | dict | set | tuple):
        self.ty = ty
        self.val = val

    def __str__(self):
        return "Value(type: '" + str(self.ty) + "', value: " + str(self.val) + ")"

    def __call__(self, *args, **kwargs):
        if self.ty == "func":
            arguments = list(map(lambda v: tree.expression.NumericLiteral(v), args))
            call = tree.expression.CallExpression(self.val.name, arguments)
            return call.evaluate(global_context).val
        else:
            raise Exception("Cannot Call Non-Function")

    def is_truthy(self):
        return self.ty == "bool" and self.val and self.ty is not None

    def __eq__(self, other):
        return self.ty == other.ty and self.val == other.val

    def __add__(self, other):
        if self.ty == "int" and other.ty == "int":
            return Value("int", self.val + other.val)
        else:
            raise Exception("Unimplemented")

    def __sub__(self, other):
        if self.ty == "int" and other.ty == "int":
            return Value("int", self.val - other.val)
