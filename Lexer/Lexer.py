from Utils.Patterns import *
from Lexer.Validators.Validator.Validator import TokenValidator
from Tokens.Token import Token

class Lexer:
    """
        Class responsible for validate all tokens types
    """
    _tokensList: list = []
    _resultWord: str = ''
    _position: int = 0
    _text: str

    def __init__(self, text: str):
        """
            Constructor

            :param text: The main text that will be compiled
        """
        self._text: str = text

    def prettyTokensPrint(self):
        """
            Responsible for printing the tokens

            :return None
        """
        for token in [[token.toString()] for token in self._tokensList]:
            print(token)


    def getNextToken(self, position = 0) -> Token:
        """
            Get the next token and returns it

            :return Returns the token at a specific position
        """
        return self._tokensList[position]


    def lookAhead(self):
        """
            :return Returns a cursor for the next position if it exists. Otherwise it returns End Of File statement.
        """
        next = self._position + 1
        return 'EOF' if next >= len(self._text) else self._text[next]

    def curr_char(self):
        """
            Responsible for returning the current character

            :return Returns the char at current position
        """
        return self._text[self._position]

    def advance(self):
        """
            Increments position

            :return None
        """
        self._position += 1

    def appendToResultWord(self, char):
        """
            Appends a char into result word

            :param char: A simple char

            :return None
        """
        self._resultWord += char
        self.advance()

    def clearResultWord(self):
        """
            Clears the result word

            :return None
        """
        self._resultWord = ""

    def isComparisonOperator(self, char):
        """
            Check if the token is a comparison operator

            :param char: A simple char

            :return boolean
        """

        if isComparisonStarter(char):
            if isEquals(self.lookAhead()):
                self.appendToResultWord(char)
                self.appendToResultWord(self.curr_char())
                return True

            self.appendToResultWord(char)
            return True

        return False

    def isString(self, char):
        """
            Check if the token is a string

            :param char: A simple char

            :return boolean
        """

        if isQuote(char):

            quote = char
            self.appendToResultWord(quote)

            if self.curr_char() == quote:
                self.appendToResultWord(quote)
                return True

            while True:
                if self.lookAhead() == 'EOF':
                    if self.curr_char() != quote:
                        return False

                elif self.lookAhead() == quote:
                    self.appendToResultWord(self.curr_char())
                    self.appendToResultWord(quote)
                    return True

                self.appendToResultWord(self.curr_char())

        return False

    def isIdentifierOrKeyword(self, char):
        """
            Check if the token is an identifier or a keyword

            :param char: A simple char

            :return boolean
        """

        if isLetter(char) or isUnderscore(char):

            isValidTerminator = lambda c: isSeparator(c) or isOperator(c) or isOpener(c) or isEquals(c) or isCloser(c)

            if self.lookAhead() == 'EOF' or isValidTerminator(self.lookAhead()):
                self.appendToResultWord(char)
                return True

            self.appendToResultWord(char)

            while True:
                if self.lookAhead() == 'EOF' or isValidTerminator(self.lookAhead()):
                    if not (isLetterOrNumber(self.curr_char()) or isUnderscore(self.curr_char())):
                        return False

                    self.appendToResultWord(self.curr_char())
                    return True

                if isLetterOrNumber(self.curr_char()) or isUnderscore(char):
                    self.appendToResultWord(self.curr_char())
                else:
                    return False

        return False

    def isNumber(self, char):
        """
            Validates if the token is a number.

            :param char: A simple char

            :return boolean
        """

        if char.isdigit():
            hasPoint = False
            isValidTerminator = lambda c: isOpener(c) or isCloser(c) or isSeparator(c) or isOperator(c)

            if self.lookAhead() == 'EOF' or isValidTerminator(self.lookAhead()):
                self.appendToResultWord(char)
                return True

            self.appendToResultWord(char)

            while True:
                if self.lookAhead() == 'EOF' or isValidTerminator(self.lookAhead()):
                    if not self.curr_char().isdigit():
                        return False

                    self.appendToResultWord(self.curr_char())
                    return True

                elif isPoint(self.lookAhead()):
                    if hasPoint:
                        return False

                    self.appendToResultWord(self.curr_char())

                elif self.lookAhead().isdigit():
                    if isPoint(self.curr_char()):
                        hasPoint = True

                    self.appendToResultWord(self.curr_char())

        return False

    def readTokens(self):
        """
            Reads and validates the token type.

            :return None
        """

        readers = [self.isString, self.isNumber, self.isComparisonOperator, self.isIdentifierOrKeyword]

        for reader in readers:
            if reader(self.curr_char()):
                return

        # if current char has not passed in any reader, just advance and set result word as the char
        self.appendToResultWord(self.curr_char())

    def readInput(self):
        """
            Read user's input

            :return None
        """
        while True:
            if self._position == len(self._text):
                self._tokensList.append(Token("EOF", "eof"))
                break

            char = self.curr_char()

            if isWhitespace(char):
                self.advance()
                continue

            self.readTokens()

            TokenValidator.validateToken(char, self._resultWord, self._tokensList)

            self.clearResultWord()
