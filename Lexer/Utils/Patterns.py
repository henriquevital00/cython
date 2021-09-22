import re

isSeparator = lambda char : re.match("^;|\\s|\\n$", char)

isWhitespace = lambda char : re.match("^ $", char)

isPoint = lambda char : char == "."

isEquals = lambda char : char == "="

isUnderscore = lambda char : char == "_"

isArithmeticOperator = lambda char : re.match("^\+|-|\*|/$", char)

isLogicalOperator = lambda char : re.match("^&|\|", char)

isComparisonStarter = lambda char : re.match("^<|>|=|!$", char)

isOperator = lambda char : isLogicalOperator(char) \
                           or isComparisonStarter(char)\
                           or isArithmeticOperator(char)

isBiggerOrLessOperator = lambda char : re.match("^<|>$", char)

isCloseParenthesis = lambda char : char == ")"

isOpenCurlyBracket = lambda char : char == "{"

isLetterOrNumber = lambda char : re.match("^\w$", char)

isQuote = lambda char : re.match("^\"|'$", char)

isMinus = lambda char : char == "-"
