import ply.yacc as yacc
from Lexer import LexicalScanner
import logging
from AbstractSyntaxTree import ASTNode
class Parser(object):
    tokens = LexicalScanner.tokens
    def __init__(self, parserCache = "parserCache", lexicalCache = "lexicalScannerCache"):
        self.scanner = LexicalScanner(lexicalCache)
        self.scanner.build()
        self.cache = parserCache
        self.parser = None
        self.start = 'Start'
        self.compare = {
            '>': ASTNode.GT,
            '<': ASTNode.LT,
            '>=': ASTNode.GTE,
            '<=': ASTNode.LTE,
            '==': ASTNode.EQ,
            '!=': ASTNode.NE
        }
    def createBinaryNode(self, value, type, left, right):
        node = ASTNode(value, type)
        node.append(left)
        node.append(right)
        return node
    def p_start_string(self, p):
        r'''Start : Undefined
                | Array
                | Enumeration
                '''
        p[0] = p[1]
    def p_enum(self, p):
        'Enumeration : ENUM'
        p[0] = ASTNode(p[1], ASTNode.ENUM)
    def p_array_multiple(self, p):
        'Array : Array COMMA BooleanExpr'
        p[0] = self.createBinaryNode(ASTNode.COMMA, ASTNode.ARRAY_SEPARATOR, p[1], p[3])
    def p_array_one(self, p):
        'Array : BooleanExpr'
        p[0] = p[1]
    def p_boolexpr_or(self, p):
        'BooleanExpr : BooleanExpr OR BooleanTerm'
        p[0] = self.createBinaryNode('or', ASTNode.OR, p[1], p[3])
    def p_boolexpr_term(self, p):
        'BooleanExpr : BooleanTerm'
        p[0] = p[1]
    def p_boolterm_and(self, p):
        'BooleanTerm : BooleanTerm AND BooleanFactor'
        p[0] = self.createBinaryNode('and', ASTNode.AND, p[1], p[3])
    def p_boolterm_factor(self, p):
        'BooleanTerm : BooleanFactor'
        p[0] = p[1]
    def p_logical_op(self, p):
        '''LogicalOp : GE
                     | LE
                     | LTE
                     | GTE
                     | EQUAL
                     | NE
        '''
        p[0] = (p[1], self.compare[p[1]])
    def p_booleanfactor_compare(self, p):
        'BooleanFactor : BooleanFactor LogicalOp BoolBase'
        p[0] = self.createBinaryNode(p[2][0], p[2][1], p[1], p[3])
    def p_booleanfactor_boolbase(self,p):
        'BooleanFactor : BoolBase'
        p[0] = p[1]
    def p_boolbase_stringexp(self, p):
        'BoolBase : String'
        p[0] = p[1]
    def p_boolbase_not(self, p):
        'BoolBase : NOT BoolBase'
        node = ASTNode('not', ASTNode.NOT)
        node.append(p[2])
        p[0] = node

    def p_boolbase_const(self, p):
        '''BoolBase : TRUE
                    | FALSE'''
        value = (True, ASTNode.TRUE) if p[1].lower() == 'true' else (False, ASTNode.FALSE)
        p[0] = ASTNode(*value)
    def p_string_concat(self, p):
        'String : String PLUS StringBase'
        p[0] = self.createBinaryNode('+', ASTNode.PLUS, p[1], p[3])
    def p_undefined(self, p):
        "Undefined : UNDEFINED"
        p[0] = ASTNode(p[1], ASTNode.UNDEFINED)
    def p_string_stringbase(self, p):
        'String : StringBase'
        p[0] = p[1]
    def p_stringbase_var(self, p):
        'StringBase : expression'
        p[0] = p[1]
    def p_stringbase_reverse(self, p):
        'StringBase : REVERSE StringBase'
        node = ASTNode('~' , ASTNode.REVERSE_STRING)
        node.append(p[2])
        p[0] = node
    def p_stringbase_str(self, p):
        'StringBase : STR'
        p[0] = ASTNode(p[1], ASTNode.STR)
    def p_expression_sub(self, p):
        'expression : expression SUB term'

        p[0] = self.createBinaryNode('-', ASTNode.SUB, p[1], p[3])
    def p_expression_term(self, p):
        'expression : term'
        p[0] = p[1]
    def p_term_mult(self, p):
        'term : term MULT term2'
        p[0] = self.createBinaryNode('*', ASTNode.MULT, p[1], p[3])

    def p_term_div(self, p):
        'term : term DIV term2'
        p[0] = self.createBinaryNode('/', ASTNode.DIV, p[1], p[3])
    def p_term_term2(self, p):
        'term : term2'
        p[0] = p[1]
    def p_term2_exp(self,p):
        'term2 : term2 EXP factor'
        p[0] = self.createBinaryNode('^', ASTNode.EXP, p[1], p[3])
    def p_term2_factor(self, p):
        'term2 : factor'
        p[0] = p[1]
    def p_factor_num(self, p):
        'factor : INTEGER'
        node = ASTNode(p[1], ASTNode.INTEGER)
        p[0] = node
    def p_factor_neg(self, p):
        'factor : SUB factor'
        node = ASTNode('-', ASTNode.NEGATE)
        node.append(p[2])
        p[0] = node
    def p_factor_var(self, p):
        'factor : VAR'
        node = ASTNode(p[1], ASTNode.VAR)
        p[0] = node
    def p_factor_paren(self, p):
        'factor : LPAREN BooleanExpr RPAREN'
        p[0]= p[2]

    def p_error(self, p):
        if p is None:
            raise SyntaxError("Syntax Error detected possibly at the end of expression")
        raise SyntaxError(f"Syntax Error on line {p.lineno} at char {p.lexpos}")
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, optimize=1,debug=True, tabmodule=self.cache, start=self.start, **kwargs)
    def parse(self, input):
        if self.parser is None:
            return
        log = logging.getLogger()
        res = self.parser.parse(input, lexer = self.scanner.lexer, debug = log)
        return res

