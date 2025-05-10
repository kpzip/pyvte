from tree.expression import Expression


class Type(Expression):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name
