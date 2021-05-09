from AbstractSyntaxTree import ASTNode
from EvaluatorRoutines import EvaluationRoutines
from DataTypes import DataTypeHierarchy
class Evaluator:
    def __init__(self, root: ASTNode, use = dict()):
        self.root = root
        self.use = use
        self.hierarchy = DataTypeHierarchy.build()
        self.env = self.__getEnv()
    def __getEnv(self):
        def env(node: ASTNode):
            if node.nodeType == ASTNode.VAR:
                val, type = self.use[node.value]
                return val, self.hierarchy.nodesCache[type].resolution
        return env
    def evaluate(self):
        self.__evaluate(self.root)
        
    def __evaluate(self, node: ASTNode):
        if not node: return
        for child in node.children:
            self.__evaluate(child)
        EvaluationRoutines.apply(node, self.env)