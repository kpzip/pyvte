from context.context import Context


class ContextStack:

    def __init__(self, initial=None):
        if initial is None:
            initial = []
        self.stack: list[Context] = initial

    def push(self, new_context: Context):
        self.stack.append(new_context)

    def pop(self) -> Context:
        return self.stack.pop()

    def peek(self) -> Context:
        return self.stack[-1]

    def traverse(self):
        return reversed(self.stack)
