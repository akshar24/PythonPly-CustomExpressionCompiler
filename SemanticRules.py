from AbstractSyntaxTree import ASTNode
from NodeTypeSystem import ASTNodeDataType as TypeChecker
class SemanticRuleMappings:
    rulesMapping = dict()
class Result:
    def __init__(self, status, error = ""):
        self.status = status
        self.error = error
    def isSuccess(self):
        return self.status


def mapRule(nodeType: str):
    def map_rule_deco(func):
        SemanticRuleMappings.rulesMapping[nodeType] = func
        return func
    return map_rule_deco
def getBinaryOpTypeErr(node: ASTNode):
    return f"unsupported operand types for {node.value}: {node.left.dataType} and {node.right.dataType}"
def getUniaryOpTypeErr(node: ASTNode):
    return f"unsupported operand type for {node.value}: {node.left.dataType}"

class SemanticRules:

    @staticmethod
    @mapRule(nodeType=ASTNode.ENUM)
    def enum(node: ASTNode, env):
        node.dataType = TypeChecker.ENUM
        return Result(True)
    @staticmethod
    @mapRule(nodeType= ASTNode.VAR)
    def var(node: ASTNode, env):
        #DATABASE QUERY THAT CHECKS IF VAR EXISTS
        node.dataType = env(node)
        return Result(True)

    @staticmethod
    @mapRule(nodeType=ASTNode.UNDEFINED)
    def undefined(node:ASTNode):
        node.dataType = TypeChecker.UNDEFINED
        return Result(True)
    @staticmethod
    @mapRule(nodeType=ASTNode.ARRAY_SEPARATOR)
    def array_sep(node: ASTNode):
        left, right = node.left, node.right
        status, err = None, None
        isLooselyNumeric = lambda type: type == TypeChecker.NUMERICARRAY or type == TypeChecker.INTARRAY
        isNumericBool =lambda  type: type == TypeChecker.INTARRAY or type == TypeChecker.NUMERICARRAY or type == TypeChecker.BOOLEANARRAY or type == TypeChecker.NUMERIC_BOOL_ARR
        if TypeChecker.isAtomic(left): ltype = TypeChecker.getArrayTypeBasedOnAtomic(left)
        else: ltype = left.dataType
        rtype = TypeChecker.getArrayTypeBasedOnAtomic(right)
        if ltype == rtype:
            node.dataType = ltype
            status = True
        elif isLooselyNumeric(ltype) and isLooselyNumeric(rtype):
            node.dataType = TypeChecker.NUMERICARRAY
            status = True
        elif isNumericBool(ltype) and isNumericBool(rtype):
            node.dataType = TypeChecker.NUMERIC_BOOL_ARR
            status= True
        else:
            status = False
            err = f"Array cannot hold different types: {TypeChecker.getAtomicTypeBasedOnArray(ltype)} and {TypeChecker.getAtomicTypeBasedOnArray(rtype)}"
        return Result(status, err)
    @staticmethod
    @mapRule(nodeType=ASTNode.AND)
    @mapRule(nodeType=ASTNode.OR)
    def logical_op(node: ASTNode):
        left = node.left
        right = node.right
        valid = lambda node: TypeChecker.isStrictlyBoolean(node) or TypeChecker.isLooselyNumeric(node)
        if valid(left) and valid(right):
            node.dataType = TypeChecker.BOOLEAN
            return Result(True)

        else:
            return Result(False, getBinaryOpTypeErr(node))



    @staticmethod
    @mapRule(nodeType=ASTNode.NEGATE)
    def negate(node: ASTNode):
        left = node.left
        if TypeChecker.isLooselyNumeric(left):
            node.dataType = TypeChecker.NUMERIC
            return Result(True)
        else: return Result(False, getUniaryOpTypeErr(node))
    @staticmethod
    @mapRule(nodeType=ASTNode.REVERSE_STRING)
    def reverse_string(node:ASTNode):
        left = node.left
        if TypeChecker.isStrictlyString(left):
            node.dataType = TypeChecker.STRING
            return Result(True)
        else:
            return Result(False, getUniaryOpTypeErr(node))

    @staticmethod
    @mapRule(nodeType=ASTNode.NOT)
    def not_op(node: ASTNode):
        left = node.left
        if TypeChecker.isLooselyNumeric(left) or TypeChecker.isStrictlyBoolean(left):
            node.dataType = TypeChecker.BOOLEAN
            return Result(True)
        else:
            return Result(False, getUniaryOpTypeErr(node))

    @staticmethod
    @mapRule(nodeType=ASTNode.GT)
    @mapRule(nodeType=ASTNode.LT)
    @mapRule(nodeType=ASTNode.EQ)
    @mapRule(nodeType=ASTNode.NE)
    @mapRule(nodeType=ASTNode.GTE)
    @mapRule(nodeType=ASTNode.LTE)
    def relationOp(node: ASTNode):
        left = node.left
        right = node.right
        if not TypeChecker.isEqual(left, right):
            return Result(False, f'incomparables types: {left.dataType} and {right.dataType}')
        else:
            node.dataType = TypeChecker.BOOLEAN
            return Result(True)

    @staticmethod
    @mapRule(nodeType = ASTNode.MULT)
    @mapRule(nodeType=ASTNode.SUB)
    @mapRule(nodeType=ASTNode.DIV)
    @mapRule(nodeType=ASTNode.EXP)
    def strictArithmeticBinaryOp(node: ASTNode):
        """
         Apply type system rules for '*', '/', '-', '^'
        :param node:
        :return:
        """
        left = node.left
        right = node.right
        if TypeChecker.isLooselyNumeric(left) and TypeChecker.isLooselyNumeric(right):
            node.dataType = TypeChecker.NUMERIC
            return Result(True)
        else:
            return Result(False, getBinaryOpTypeErr(node))
        
   

    @staticmethod
    @mapRule(nodeType=ASTNode.PLUS)
    def hybridAdd(node: ASTNode):
        left = node.left
        right = node.right
        validType = lambda node: TypeChecker.isStrictlyString(node) or TypeChecker.isLooselyNumeric(node)
        if validType(left) and validType(right):
            node.dataType =TypeChecker.NUMERIC if TypeChecker.isLooselyNumeric(left) and TypeChecker.isLooselyNumeric(right) else TypeChecker.STRING
            return Result(True)
        else:
            return Result(False, getBinaryOpTypeErr(node))

    @staticmethod
    @mapRule(nodeType=ASTNode.FALSE)
    @mapRule(nodeType=ASTNode.TRUE)
    def boolconstant(node: ASTNode):
        node.dataType = TypeChecker.BOOLEAN
        return Result(True)

    @staticmethod
    @mapRule(nodeType=ASTNode.INTEGER)
    def integer(node: ASTNode):

        node.dataType = TypeChecker.INTEGER
        return Result(True)

    @staticmethod
    @mapRule(nodeType=ASTNode.STR)
    def string(node: ASTNode):
        node.dataType = TypeChecker.STRING
        return Result(True)

    
    @staticmethod
    def apply(node: ASTNode, **kwargs):
        rule = SemanticRuleMappings.rulesMapping[node.nodeType]
        arguments = set(rule.__code__.co_varnames)
        argsToPass = {key:val for key, val in kwargs.items() if key in arguments}
        result: Result = rule(node, **argsToPass)
        if not result.isSuccess():
            raise TypeError(result.error)


