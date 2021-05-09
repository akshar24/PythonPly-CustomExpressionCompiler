from AbstractSyntaxTree import ASTNode
from NodeTypeSystem import ASTNodeDataType as Types
class EvaluationRoutineMapping:
    routineMapping = dict()
def mapRoutine(nodeType):
    def map_routine_deco(func):
        EvaluationRoutineMapping.routineMapping[nodeType] = func
        return func
    return map_routine_deco

class EvaluationRoutines:
    @staticmethod
    @mapRoutine(nodeType = ASTNode.INTEGER)
    def integer(node: ASTNode, _):
        node.dataType = Types.INTEGER

    @staticmethod
    @mapRoutine(nodeType = ASTNode.STR)
    def string(node: ASTNode, _):
        node.dataType = Types.STRING
    
    @staticmethod
    @mapRoutine(nodeType = ASTNode.PLUS)
    def add(node: ASTNode, _):
        isatLeastOneString = Types.isStrictlyString(node.left) or Types.isStrictlyString(node.right)
        if isatLeastOneString:
            node.value = str(node.left.value) + str(node.right.value)
            node.dataType = Types.STRING
        else:
            node.value = node.left.value + node.right.value
            node.dataType = Types.NUMERIC   

    @staticmethod
    @mapRoutine(nodeType = ASTNode.MULT)
    @mapRoutine(nodeType = ASTNode.DIV)
    @mapRoutine(nodeType = ASTNode.SUB)
    @mapRoutine(nodeType = ASTNode.EXP)
    def binaryArithmeticOp(node: ASTNode, _):
        left=  node.left.value
        right = node.right.value
        if node.nodeType == ASTNode.MULT:
            node.value = left * right
        elif node.nodeType == ASTNode.SUB:
            node.value = left - right
        elif node.nodeType == ASTNode.DIV:
            if right == 0:
                raise ZeroDivisionError("cannot divide with zero")
            node.value = left / right
        else:
            node.value = left ** right
        node.dataType = Types.NUMERIC
            
    @staticmethod
    @mapRoutine(nodeType = ASTNode.NEGATE)
    def negate(node: ASTNode, _):
        node.value = -node.left.value
        node.dataType = Types.NUMERIC

    @staticmethod
    @mapRoutine(nodeType = ASTNode.REVERSE_STRING)
    def reverse_string(node: ASTNode, _):
        node.value = node.left.value[::-1]
        node.dataType = Types.STRING

    @staticmethod
    @mapRoutine(nodeType=ASTNode.NOT)
    def notOp(node: ASTNode, _):
        node.value = not node.left.value
        node.dataType = Types.BOOLEAN
    
    @staticmethod
    @mapRoutine(nodeType=ASTNode.EQ)
    @mapRoutine(nodeType=ASTNode.NE)
    @mapRoutine(nodeType=ASTNode.GT)
    @mapRoutine(nodeType=ASTNode.LT)
    @mapRoutine(nodeType=ASTNode.GTE)
    @mapRoutine(nodeType=ASTNode.LTE)
    def binaryComparisonOp(node:ASTNode, _):
        left = node.left.value
        right = node.right.value
        if node.nodeType == ASTNode.EQ:
            node.value = left == right
        elif node.nodeType == ASTNode.NE:
            node.value = left != right
        elif node.nodeType == ASTNode.GT:
            node.value = left > right
        elif node.nodeType == ASTNode.LT:
            node.value = left < right
        elif node.nodeType == ASTNode.GTE:
            node.value = left >= right
        else:
            node.value = left <= right
        node.dataType = Types.BOOLEAN

    @staticmethod
    @mapRoutine(nodeType= ASTNode.TRUE)
    @mapRoutine(nodeType=ASTNode.FALSE)
    def boolConst(node: ASTNode, _):
        node.dataType = Types.BOOLEAN


    @staticmethod
    @mapRoutine(nodeType= ASTNode.AND)
    @mapRoutine(nodeType = ASTNode.OR)
    def logicalOp(node: ASTNode, _ ):
        left = node.left.value
        right = node.right.value
        if node.nodeType == ASTNode.AND:
            node.value = left and right
        else:
            node.value = left or right
        
        node.dataType = Types.BOOLEAN
    
    @staticmethod
    @mapRoutine(nodeType=ASTNode.ARRAY_SEPARATOR)
    def array(node: ASTNode, _):

        if Types.isAtomic(node.left):
            node.left.value = [node.left.value]
        node.value= node.left.value
        node.value.append(node.right.value)
        isLooselyNumeric = lambda type: type == Types.NUMERICARRAY or type == Types.INTARRAY
        isNumericBool =lambda type: type == Types.INTARRAY or type == Types.NUMERICARRAY or type == Types.BOOLEANARRAY or type == Types.NUMERIC_BOOL_ARR
        if Types.isAtomic(node.left): ltype = Types.getArrayTypeBasedOnAtomic(node.left)
        else: ltype = node.left.dataType
        rtype = Types.getArrayTypeBasedOnAtomic(node.right)
        if ltype == rtype:
            node.dataType = ltype
        elif isLooselyNumeric(ltype) and isLooselyNumeric(rtype):
            node.dataType = Types.NUMERICARRAY
        elif isNumericBool(ltype) and isNumericBool(rtype):
            node.dataType = Types.NUMERIC_BOOL_ARR

    @staticmethod  
    @mapRoutine(nodeType = ASTNode.UNDEFINED)
    def undefined(node: ASTNode, _):
        node.dataType = Types.UNDEFINED

    @staticmethod
    @mapRoutine(nodeType=ASTNode.VAR)
    def variable(node, env):
        node.value, node.dataType = env(node)

    @staticmethod
    def apply(node: ASTNode, env):
        EvaluationRoutineMapping.routineMapping[node.nodeType](node, env)
for key,val in EvaluationRoutineMapping.routineMapping.items():
    print(key, val)
    