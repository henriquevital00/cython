from Lexer.Lexer import Lexer
from Tests.SymbolTableInitialTest import test

# Step by step
# Lexer -> Syntax Analyzer -> Symbols Table

def main():

    test.addSymbolsToTableTest()

    test.shouldTableFindSymbol('number2')

    with open("program.txt", "r") as input:
        Lexer(input.read()).readTokens()


if __name__ == "__main__":
    main()