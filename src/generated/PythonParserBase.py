from antlr4.Parser import Parser


class PythonParserBase(Parser):

    def isEqualCurrentTokenText(self, token_text):
        return self.getCurrentToken().text == token_text

    def isnotEqualCurrentTokenText(self, token_text):
        return not self.isEqualCurrentTokenText(token_text)