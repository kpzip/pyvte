# Responsible for turning antlr parse trees into an actuall useful AST
from functools import reduce

from generated.PythonParser import PythonParser
from generated.PythonParserVisitor import PythonParserVisitor
from tree.assignment_target import SingleAssignmentTarget
from tree.definitions import FuncDefinition
from tree.expression import TernaryExpression, OrExpression, AndExpression, NotExpression, EqComparison, \
    NotEqComparison, LeComparison, LtComparison, GeComparison, GtComparison, NotInComparison, InComparison, \
    IsNotComparison, IsComparison, BitOrExpression, BitXorExpression, BitAndExpression, ShlExpression, ShrExpression, \
    AddExpression, SubtractExpression, MultiplyExpression, DivideExpression, IntDivideExpression, RemainderExpression, \
    MatmulExpression, NegateExpression, PositiveExpression, BitNotExpression, PowerExpression, Identifier, \
    NumericLiteral, TrueLiteral, NoneLiteral, StarExpression, StarExpressions, CallExpression
from tree.statements import StatementList, SimpleStatementList, AssertStatement, AssignmentStatement, IfStatement, \
    ReturnStatement


class TreeVisitor(PythonParserVisitor):

    def visitFile_input(self, ctx: PythonParser.File_inputContext):
        if statements := ctx.statements():
            return self.visitStatements(statements)

    def visitStatements(self, ctx: PythonParser.StatementsContext):
        statement_list = []
        i = 0
        while statement := ctx.statement(i):
            statement_list.append(self.visitStatement(statement))
            i += 1
        return StatementList(statement_list)

    def visitStatement(self, ctx: PythonParser.StatementContext):
        if simple := ctx.simple_stmts():
            return self.visitSimple_stmts(simple)
        if compound := ctx.compound_stmt():
            return self.visitCompound_stmt(compound)

    def visitCompound_stmt(self, ctx: PythonParser.Compound_stmtContext):
        if fdef := ctx.function_def():
            return self.visitFunction_def(fdef)
        elif ifstmt := ctx.if_stmt():
            return self.visitIf_stmt(ifstmt)
        else:
            raise Exception("Not implemented yet")

    def visitIf_stmt(self, ctx: PythonParser.If_stmtContext):
        cond = self.visitNamed_expression(ctx.named_expression())
        code = self.visitBlock(ctx.block())
        return IfStatement(cond, code)

    def visitNamed_expression(self, ctx: PythonParser.Named_expressionContext):
        if expr := ctx.expression():
            return self.visitExpression(expr)
        else:
            raise Exception("Not Implemented")

    def visitFunction_def(self, ctx: PythonParser.Function_defContext):
        return self.visitFunction_def_raw(ctx.function_def_raw())

    def visitFunction_def_raw(self, ctx: PythonParser.Function_def_rawContext):
        name = ctx.NAME()
        params = self.visitParams(ctx.params())
        block = self.visitBlock(ctx.block())
        return FuncDefinition(Identifier(name.getText()), params, block)

    def visitBlock(self, ctx: PythonParser.BlockContext):
        return self.visitStatements(ctx.statements())

    def visitParams(self, ctx: PythonParser.ParamsContext):
        return self.visitParameters(ctx.parameters())

    def visitParameters(self, ctx: PythonParser.ParametersContext):
        if param_nd := ctx.param_no_default():
            return list(map(lambda p: self.visitParam_no_default(p), param_nd))
        else:
            raise Exception("Unimplemented")

    def visitParam_no_default(self, ctx: PythonParser.Param_no_defaultContext):
        return self.visitParam(ctx.param())

    def visitParam(self, ctx: PythonParser.ParamContext):
        return Identifier(ctx.NAME().getText())

    def visitSimple_stmts(self, ctx: PythonParser.Simple_stmtsContext):
        statement_list = []
        i = 0
        while statement := ctx.simple_stmt(i):
            statement_list.append(self.visitSimple_stmt(statement))
            i += 1
        if len(statement_list) == 1:
            return statement_list[0]
        return SimpleStatementList(statement_list)

    def visitSimple_stmt(self, ctx: PythonParser.Simple_stmtContext):
        if assert_stmt := ctx.assert_stmt():
            return self.visitAssert_stmt(assert_stmt)
        if assign_stmt := ctx.assignment():
            return self.visitAssignment(assign_stmt)
        if ret_stmt := ctx.return_stmt():
            return self.visitReturn_stmt(ret_stmt)
        else:
            raise Exception("Not Implemented yet")

    def visitReturn_stmt(self, ctx: PythonParser.Return_stmtContext):
        expr = self.visitStar_expressions(ctx.star_expressions())
        return ReturnStatement(expr)

    def visitAssert_stmt(self, ctx: PythonParser.Assert_stmtContext):
        exprs = []
        i = 0
        while expr := ctx.expression(i):
            exprs.append(self.visitExpression(expr))
            i += 1
        return AssertStatement(exprs)

    def visitAssignment(self, ctx: PythonParser.AssignmentContext):
        if name := ctx.NAME():
            name = Identifier(name.getText())
            rhs = self.visitAnnotated_rhs(ctx.annotated_rhs())
            return AssignmentStatement(SingleAssignmentTarget(name), rhs)
        elif sts := ctx.star_targets():
            if ses := ctx.star_expressions():
                ses = self.visitStar_expressions(ses)
                if False:  # TODO
                    raise Exception("Cannot assign targets to a different number of variables!")
                elif len(sts) == 1:
                    return AssignmentStatement(SingleAssignmentTarget(self.visitStar_targets(sts[0])),
                                               ses)
            else:
                raise Exception("Yield exprs are not implemented yet")
        else:
            raise Exception("Not implemented yet")

    def visitAnnotated_rhs(self, ctx: PythonParser.Annotated_rhsContext):
        if se := ctx.star_expressions():
            return self.visitStar_expressions(se)
        else:
            raise Exception("Not implemented yet")

    def visitStar_targets(self, ctx: PythonParser.Star_targetsContext):
        sts = ctx.star_target()
        if len(sts) == 1:
            return self.visitStar_target(sts[0])
        else:
            raise Exception("Not implemented yet")

    def visitStar_target(self, ctx: PythonParser.Star_targetContext):
        if stgt := ctx.star_target():
            return StarExpression(self.visitStar_target(stgt))
        else:
            return self.visitTarget_with_star_atom(ctx.target_with_star_atom())

    def visitTarget_with_star_atom(self, ctx: PythonParser.Target_with_star_atomContext):
        if atom := ctx.star_atom():
            return self.visitStar_atom(atom)
        else:
            raise Exception("Array index assignment is not yet implemented")

    def visitStar_atom(self, ctx: PythonParser.Star_atomContext):
        if name := ctx.NAME():
            return Identifier(name.getText())
        else:
            raise Exception("Multiple assignment is not yet implemented")

    def visitStar_expressions(self, ctx: PythonParser.Star_expressionsContext):
        inner = ctx.star_expression()
        if len(inner) == 1:
            return self.visitStar_expression(inner[0])
        return StarExpressions(list(map(lambda expr: self.visitStar_expression(expr), inner)))

    def visitStar_expression(self, ctx: PythonParser.Star_expressionContext):
        if expr := ctx.expression():
            return self.visitExpression(expr)
        bor = ctx.bitwise_or()
        return StarExpression(self.visitBitwise_or(bor))

    def visitExpression(self, ctx: PythonParser.ExpressionContext):
        # top level is a potential ternary expression
        lhs = self.visitDisjunction(ctx.disjunction(0))
        if condition := ctx.disjunction(1):
            condition = self.visitDisjunction(condition)
            rhs = self.visitExpression(ctx.expression())
            return TernaryExpression(lhs, rhs, condition)
        return lhs

    def visitDisjunction(self, ctx: PythonParser.DisjunctionContext):
        # top level is a logical or statement
        conditions = []
        i = 0
        while condition := ctx.conjunction(i):
            conditions.append(self.visitConjunction(condition))
            i += 1
        if len(conditions) == 1:
            return conditions[0]
        return reduce(lambda lhs, rhs: OrExpression(lhs, rhs), conditions)

    def visitConjunction(self, ctx: PythonParser.ConjunctionContext):
        # top level is a logical or statement
        conditions = []
        i = 0
        while condition := ctx.inversion(i):
            conditions.append(self.visitInversion(condition))
            i += 1
        if len(conditions) == 1:
            return conditions[0]
        return reduce(lambda lhs, rhs: AndExpression(lhs, rhs), conditions)

    def visitInversion(self, ctx: PythonParser.InversionContext):
        if inversion := ctx.inversion():
            return NotExpression(self.visitInversion(inversion))
        return self.visitComparison(ctx.comparison())

    def visitComparison(self, ctx: PythonParser.ComparisonContext):
        first = self.visitBitwise_or(ctx.bitwise_or())
        comparisons: list[PythonParser.Compare_op_bitwise_or_pairContext] = []
        i = 0
        while comparison := ctx.compare_op_bitwise_or_pair(i):
            comparisons.append(comparison)
            i += 1
        if len(comparisons) == 0:
            return first
        cmp_exprs = []
        for i in range(len(comparisons)):
            if eq := comparisons[i].eq_bitwise_or():
                cmp_exprs.append(
                    EqComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].noteq_bitwise_or():
                cmp_exprs.append(
                    NotEqComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].lte_bitwise_or():
                cmp_exprs.append(
                    LeComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].lt_bitwise_or():
                cmp_exprs.append(
                    LtComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].gte_bitwise_or():
                cmp_exprs.append(
                    GeComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].gt_bitwise_or():
                cmp_exprs.append(
                    GtComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].notin_bitwise_or():
                cmp_exprs.append(
                    NotInComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].in_bitwise_or():
                cmp_exprs.append(
                    InComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].isnot_bitwise_or():
                cmp_exprs.append(
                    IsNotComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            elif eq := comparisons[i].is_bitwise_or():
                cmp_exprs.append(
                    IsComparison(first if i == 0 else cmp_exprs[i - 1].rhs, self.visitBitwise_or(eq.bitwise_or())))
            else:
                raise Exception("Bruh")
        return reduce(lambda lhs, rhs: AndExpression(lhs, rhs), cmp_exprs)

    def visitBitwise_or(self, ctx: PythonParser.Bitwise_orContext):
        rhs = self.visitBitwise_xor(ctx.bitwise_xor())
        if lhs := ctx.bitwise_or():
            return BitOrExpression(self.visitBitwise_or(lhs), rhs)
        return rhs

    def visitBitwise_xor(self, ctx: PythonParser.Bitwise_xorContext):
        rhs = self.visitBitwise_and(ctx.bitwise_and())
        if lhs := ctx.bitwise_xor():
            return BitXorExpression(self.visitBitwise_xor(lhs), rhs)
        return rhs

    def visitBitwise_and(self, ctx: PythonParser.Bitwise_andContext):
        rhs = self.visitShift_expr(ctx.shift_expr())
        if lhs := ctx.bitwise_and():
            return BitAndExpression(self.visitBitwise_and(lhs), rhs)
        return rhs

    def visitShift_expr(self, ctx: PythonParser.Shift_exprContext):
        rhs = self.visitSum(ctx.sum_())
        if lhs := ctx.shift_expr():
            if ctx.LEFTSHIFT():
                return ShlExpression(self.visitShift_expr(lhs), rhs)
            return ShrExpression(self.visitShift_expr(lhs), rhs)
        return rhs

    def visitSum(self, ctx: PythonParser.SumContext):
        rhs = self.visitTerm(ctx.term())
        if lhs := ctx.sum_():
            if ctx.PLUS():
                return AddExpression(self.visitSum(lhs), rhs)
            return SubtractExpression(self.visitSum(lhs), rhs)
        return rhs

    def visitTerm(self, ctx: PythonParser.TermContext):
        rhs = self.visitFactor(ctx.factor())
        if lhs := ctx.term():
            if ctx.STAR():
                return MultiplyExpression(self.visitTerm(lhs), rhs)
            elif ctx.SLASH():
                return DivideExpression(self.visitTerm(lhs), rhs)
            elif ctx.DOUBLESLASH():
                return IntDivideExpression(self.visitTerm(lhs), rhs)
            elif ctx.PERCENT():
                return RemainderExpression(self.visitTerm(lhs), rhs)
            else:
                return MatmulExpression(self.visitTerm(lhs), rhs)
        return rhs

    def visitFactor(self, ctx: PythonParser.FactorContext):
        if pow := ctx.power():
            return self.visitPower(pow)
        f = ctx.factor()
        if ctx.PLUS():
            return PositiveExpression(self.visitFactor(f))
        elif ctx.MINUS():
            return NegateExpression(self.visitFactor(f))
        else:
            return BitNotExpression(self.visitFactor(f))

    def visitPower(self, ctx: PythonParser.PowerContext):
        lhs = self.visitAwait_primary(ctx.await_primary())
        if rhs := ctx.factor():
            return PowerExpression(lhs, self.visitFactor(rhs))
        return lhs

    def visitAwait_primary(self, ctx: PythonParser.Await_primaryContext):
        p = ctx.primary()
        if ctx.AWAIT():
            raise Exception("Async is Unimplemented")
        return self.visitPrimary(p)

    def visitPrimary(self, ctx: PythonParser.PrimaryContext):
        if p := ctx.primary():
            if ctx.LPAR():
                args = ctx.arguments()
                astargs = [] if args is None else self.visitArguments(args)
                p = self.visitPrimary(p)
                return CallExpression(p, astargs)
            raise Exception("Function calls / indexing is unimplemented")
        return self.visitAtom(ctx.atom())

    def visitArguments(self, ctx: PythonParser.ArgumentsContext):
        return self.visitArgs(ctx.args())

    def visitArgs(self, ctx: PythonParser.ArgsContext):
        return list(map(self.visitExpression, ctx.expression()))

    def visitAtom(self, ctx: PythonParser.AtomContext):
        if name := ctx.NAME():
            return Identifier(name.getText())
        elif num := ctx.NUMBER():
            return NumericLiteral(num.getText())
        elif ctx.TRUE():
            return TrueLiteral()
        elif ctx.FALSE():
            return TrueLiteral()
        elif ctx.NONE():
            return NoneLiteral()
        else:
            raise Exception("Currently Unimplemented")
