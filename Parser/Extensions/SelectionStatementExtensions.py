from Parser.Parser import Parser
from Parser.SyntaxMatcher.SyntaxMatcher import SyntaxMatcher
from Parser.SyntaxTypes.Expression.Expression import Expression
from Parser.SyntaxTypes.Statement.SelectionStatement.ElifStatement import ElifStatement
from Parser.SyntaxTypes.Statement.SelectionStatement.ElseStatement import ElseStatement
from Parser.SyntaxTypes.Statement.SelectionStatement.IfStatement import IfStatement
from Parser.SyntaxTypes.Statement.SelectionStatement.SelectionStatement import SelectionStatement
from Parser.SyntaxTypes.Statement.SelectionStatement.WhileStatement import WhileStatement
from Tokens.Constants.TokenConstants import TokenTypes

# SELECTION_STMT -> IF_STMT | ELIF_STMT | ELSE_STMT | WHILE_STMT
#
# WHILE_STMT -> WHILE CONDITIONAL_EXPR COMPOUND_STMT
#
# IF_STMT -> IF CONDITIONAL_EXPR COMPOUND_STMT
#
# ELIF_STMT -> ELIF CONDITIONAL_EXPR COMPOUND_STMT
#
# ELSE_STMT -> ELSE COMPOUND_STMT


def parseSelectionStatement(self) -> SelectionStatement:
    """
    Parse a selection statement

    :returns: SelectionStatement
    """
    keyword = None

    if self.current_token.type in (
            TokenTypes.IF,
            TokenTypes.ELIF,
            TokenTypes.ELSE,
            TokenTypes.WHILE
    ):
        keyword = self.current_token
        self.eat(keyword.type)

    if keyword:
        if keyword.type == TokenTypes.ELSE:
            return ElseStatement(keyword, self.parseCompoundStatement())

        #  IS EXPRESSION
        conditionalExpression = SyntaxMatcher.checkSyntax([
            [Expression, self.parseConditionalExpression],
        ], self)

        scope = self.parseCompoundStatement()

        if conditionalExpression:
            if keyword.type == TokenTypes.IF:
                return IfStatement(keyword, conditionalExpression, scope)
            elif keyword.type == TokenTypes.ELIF:
                return ElifStatement(keyword, conditionalExpression, scope)

            return WhileStatement(keyword, conditionalExpression, scope)

def addExtensions() -> None:
    """
        Add the extensions

        :returns: None
    """
    Parser.parseSelectionStatement = parseSelectionStatement
