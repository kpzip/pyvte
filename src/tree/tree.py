from generated.PythonParser import PythonParser
from generated.PythonParserListener import PythonParserListener
from generated.PythonParserVisitor import PythonParserVisitor
from tree.statements import StatementList


class TreeVisitor(PythonParserVisitor):

    def visitFile_input(self, ctx: PythonParser.File_inputContext):
        if statements := ctx.statements() is not None:
            return self.visitStatements(statements)

    def visitStatements(self, ctx: PythonParser.StatementsContext):
        statement_list = []
        i = 0
        while statement := ctx.statement(i) is not None:
            statement_list.append(self.visitStatement(statement))
            i += 1
        return StatementList(statement_list)

    def visitStatement(self, ctx:PythonParser.StatementContext):
        if simple := ctx.simple_stmts() is not None:
            return self.visitSimple_stmts(simple)
        if compound := ctx.compound_stmt() is not None:
            return self.visitCompound_stmt(compound)

    def visitSimple_stmts(self, ctx:PythonParser.Simple_stmtsContext):
        statement_list = []
        i = 0
        while statement := ctx.simple_stmt(i) is not None:
            statement_list.append(self.visitSimple_stmt(statement))
            i += 1
        return SimpleStatementList(statement_list)

    def visitSimple_stmt(self, ctx:PythonParser.Simple_stmtContext):
        if assert_stmt := ctx.assert_stmt() is not None:
            return self.visitAssert_stmt(assert_stmt)

    def visitAssert_stmt(self, ctx:PythonParser.Assert_stmtContext):
        exprs = []
        i = 0
        while expr := ctx.expression(i) is not None:
            exprs.append(self.visitExpression(expr))
            i += 1
        return AssertStatement(exprs)