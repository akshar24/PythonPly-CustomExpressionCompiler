import ply.lex as lex

class TokenizedInput(object):
    def __init__(self):
        self.tokens = list()
        self.errors = list()
    def addToken(self, token):
        self.tokens.append(token)
    def recoverErrors(self,errors):

        currError = None
        for index in range(len(errors)):
            if currError is None:
                currError = {
                    'indices': [errors[index].lexpos, errors[index].lexpos],
                    'token': errors[index].value[0]
                }
            else:
                currError['indices'][1] = errors[index].lexpos
                currError['token'] += errors[index].value[0]
            if index + 1 < len(errors):
                if abs(errors[index].lexpos - errors[index + 1].lexpos) != 1:
                    self.errors.append(currError)
                    currError= None

            else:
                self.errors.append(currError)

class LexicalScanner(object):
    tokens = [
        'INTEGER',
        'PLUS',
        'SUB',
        'MULT',
        'DIV',
        'LPAREN',
        'RPAREN',
        'EXP',
        'VAR',
        'EQUAL',
        'GE',
        'LE',
        'AND',
        'OR',
        'NE',
        'NOT',
        'GTE',
        'LTE',
        'TRUE',
        'FALSE',
        'STR',
        'COMMA',
        'UNDEFINED',
        'REVERSE',
        'ENUM',
    ]
    def __init__(self, lexicalCache = "lexicalScannerCache"):
        self.cache = lexicalCache
        self.t_PLUS = r'\+'
        self.t_COMMA = r','
        self.t_EXP = r'\*\* | \^'
        self.t_MULT = r'\*'
        self.t_DIV = r'/'
        self.t_LPAREN = r'\('
        self.t_RPAREN = r'\)'
        self.t_EQUAL = r'=='
        self.t_NE = r'!='
        self.t_NOT = r'!'
        self.t_GTE = r'>='
        self.t_LTE = r'<='
        self.t_GE = r'>'
        self.t_LE = r'<'
        self.t_REVERSE = r'~'
        self.t_AND = r'&&'
        self.t_OR = r'\|\|'
        self.t_ignore = ' \t'
        self.lexer = None
        self.errors = list()
        self.keywords = {
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'true': 'TRUE',
            'false': 'FALSE',
            'True': 'TRUE',
            'False': 'FALSE',
            'Undefined': 'UNDEFINED'
        }
    

    def t_ENUM(self, token):
        r'([a-zA-Z_][a-zA-Z0-9_]*)\$([a-zA-Z_][a-zA-Z0-9_]*)'
        token.value = token.value.split("$")
        return token

    def t_VAR(self, token):

        r'[a-zA-Z_][a-zA-Z0-9_]*'
        if self.isKeyword(token.value):
            token.type = self.keywords[token.value]
        return token
    def t_STR(self, token):
        r'\"(.*?)\"'
        token.value = token.value.strip('"')
        return token
    def isKeyword(self,value):
        return value in self.keywords
    def t_INTEGER(self, token):
        r'\d+'
        token.value = int(token.value)
        return token
    def t_SUB(self, t):
        r'-'
        return t
    def t_newline(self, token):
        r'\n+'
        token.lexer.lineno += len(token.value)

    def t_error(self, token):
        self.errors.append(token)
        token.lexer.skip(1)
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, optimize = 1, lextab = self.cache, **kwargs)
    def scan(self, input):
        self.errors = list()
        if self.lexer is None:
            return None

        tokenizedInput = TokenizedInput()
        self.lexer.input(input)
        for token in self.lexer:
            tokenizedInput.addToken(token)
        tokenizedInput.recoverErrors(self.errors)
        self.errors = list()
        return tokenizedInput

