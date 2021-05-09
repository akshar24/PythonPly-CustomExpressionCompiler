from AbstractSyntaxTree import ASTNode
class ASTNodeDataType:
    INTEGER = 'INTEGER'
    NUMERIC = 'NUMERIC'
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NUMERICBOOLEAN = "NUMERIC | BOOLEAN"
    NUMERIC_BOOL_ARR = "(NUMERIC | BOOLEAN)[]"
    UNDEFINED = 'UNDEFINED'
    INTARRAY = "INTEGER[]"
    NUMERICARRAY = "NUMERIC[]"
    BOOLEANARRAY = "BOOLEAN[]"
    STRINGARRAY = "STRING[]"
    ENUM = "ENUM"

    @classmethod
    def isIntArray(cls, node: ASTNode):
        return cls.INTARRAY == node.dataType
    @classmethod
    def isLooselyNumericArray(cls, node:ASTNode):
        return cls.isIntArray(node) or cls.isNumericArray(node)

    @classmethod
    def isNumericArray(cls, node: ASTNode):
        return cls.NUMERICARRAY == node.dataType
    @classmethod
    def isBooleanArray(cls, node: ASTNode):
        return cls.BOOLEANARRAY == node.dataType
    @classmethod
    def isStringArray(cls, node: ASTNode):
        return cls.STRINGARRAY == node.dataType
    @classmethod
    def isAtomic(cls, node: ASTNode):
        return not node.dataType.endswith("[]")

    @classmethod
    def isStrictlyInteger(cls, node: ASTNode):
        return node.dataType == cls.INTEGER
    @classmethod
    def isStrictlyNumeric(cls, node: ASTNode):
        return node.dataType == cls.NUMERIC
    @classmethod
    def isLooselyNumeric(cls,  node: ASTNode):
        return cls.isStrictlyInteger(node) or cls.isStrictlyNumeric(node)
    @classmethod
    def isStrictlyString(cls, node: ASTNode):
        return cls.STRING == node.dataType
    @classmethod
    def isStrictlyBoolean(cls, node: ASTNode):
        return cls.BOOLEAN == node.dataType
    @classmethod
    def isEqual(cls, one: ASTNode, two: ASTNode):
        if cls.isLooselyNumeric(one) and cls.isLooselyNumeric(two):
            return True
        else:
            return one.dataType == two.dataType
    @classmethod
    def getArrayTypeBasedOnAtomic(cls,atomic):
        dtype = atomic if isinstance(atomic, str) else atomic.dataType
        if dtype == cls.INTEGER: return cls.INTARRAY
        elif dtype == cls.STRING: return cls.STRINGARRAY
        elif dtype == cls.NUMERIC: return cls.NUMERICARRAY
        elif dtype == cls.BOOLEAN: return cls.BOOLEANARRAY
        else: return dtype
    @classmethod
    def getAtomicTypeBasedOnArray(cls, array):
        dtype = array if isinstance(array, str) else array.dataType
        if dtype == cls.INTARRAY: return cls.INTEGER
        elif dtype ==cls.BOOLEANARRAY: return cls.BOOLEAN
        elif dtype == cls.NUMERICARRAY: return cls.NUMERIC
        elif dtype == cls.STRINGARRAY: return cls.STRING
        elif dtype == cls.NUMERIC_BOOL_ARR: return cls.NUMERICBOOLEAN
        else: return dtype