from AbstractSyntaxTree import ASTNode
from SemanticRules import SemanticRules
from NodeTypeSystem import ASTNodeDataType as TypeChecker
from DataTypes import DataTypeHierarchy, DataType
class SemanticAnalyzer:
    def __init__(self, node: ASTNode, assignType ):
        self.node = node
        self.env = self.getEnv()
        self.assignType = assignType
        self.hierarchy  = DataTypeHierarchy.build()

    def getEnv(self):
        def getEnvFunc(node: ASTNode):
            cache = {
                'a': TypeChecker.NUMERIC,
                'b': TypeChecker.BOOLEAN,
                'c': TypeChecker.STRING,
                'd': 'Dword',
                'e': 'Enumeration'
            }
            dtype = cache[node.value]
            if dtype == 'Enumeration': return TypeChecker.NUMERIC
            return dtype
        return getEnvFunc
    def analyze(self):
        self.__analyze(self.node)
        dataType: DataType = self.hierarchy.nodesCache[self.assignType]
        if self.node.dataType not in dataType.acceptableTypes:
            raise TypeError(f"Expression with type {self.node.dataType} cannot be assigned to {self.assignType}")


    def __analyze(self, node: ASTNode):
        if not node:
            return
        else:
            for child in node.children:
                self.__analyze(child)
            SemanticRules.apply(node, env = self.env)
            return

