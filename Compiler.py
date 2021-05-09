from AbstractSyntaxTree import  ASTNode
from Lexer import LexicalScanner
from Parser import Parser
from SemanticAnalyzer import SemanticAnalyzer
class Compiler:
    SCANNER = 'scan'
    PARSER = 'parse'
    SCANNER_PARSER = 'scan and parse'
    SCANNER_PARSER_SEMANTIC_ANALYZER = 'scan and parse and sa'
    PARSER_SEMANTIC_ANALYZER = 'parse and sa'
    def __init__(self,  compileUsing, assignType):
        self.compileUsing = compileUsing
        self.assignType = assignType
    def compile(self, input: str):
        return self.compileUsing(input, self.assignType)
    @classmethod
    def create(cls, assignType,  mode: str = SCANNER_PARSER_SEMANTIC_ANALYZER):
        def scan(input: str, _):
            scanner = LexicalScanner()
            scanner.build()
            result = scanner.scan(input)
            return result
        def parse(input: str, _):
            parser = Parser()
            parser.build()
            return parser.parse(input)
        def semanticAnalysis(input: ASTNode, assignType):
            semanticAnalyzer = SemanticAnalyzer(input, assignType)
            semanticAnalyzer.analyze()

        if mode == cls.SCANNER:
            return Compiler(scan, assignType)

        elif mode == cls.PARSER:
            return Compiler(parse, assignType)

        elif mode == cls.SCANNER_PARSER_SEMANTIC_ANALYZER:
            def scan_parse_analyze(input: str, assignType):
                result = scan(input, None)
                tree = parse(input, None)
                semanticAnalysis(tree, assignType)
                return result, tree
            return Compiler(scan_parse_analyze, assignType)
        elif mode == cls.SCANNER_PARSER:
            def scan_parse(input: str, _):
                return scan(input, None), parse(input, None)
            return Compiler(scan_parse, assignType)
        elif mode == cls.PARSER_SEMANTIC_ANALYZER:
            def parse_analyze(input: str, assignType):
                tree = parse(input, None)
                semanticAnalysis(tree, assignType)
                return tree
            return Compiler(parse_analyze, assignType)
        else:
            raise ValueError('Compiler cannot be created with this mode')
