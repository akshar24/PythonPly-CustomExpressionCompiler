from binarytree import Node
class ASTNode:
    PLUS = 'ADD'
    MULT = 'MULTIPLY'
    EXP = 'EXPONENT'
    DIV = 'DIVISION'
    SUB = 'SUBTRACT'
    NEGATE = 'NEGATE'
    REVERSE_STRING = 'REVERSE'
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    UNDEFINED = 'UNDEFINED'
    GT = 'Greater Than'
    LT = 'Less Than'
    GTE = 'Greater than or Equal to'
    LTE = 'Less than or Equal to'
    EQ = 'EQUAL'
    NE = 'NOT EQUAL'
    INTEGER = 'INTEGER'
    VAR = "VARIABLE"
    STR = "STRING"
    TRUE = "TRUE"
    FALSE = "FALSE"
    COMMA = "COMMA"
    ARRAY_SEPARATOR = "ARRAY_SEPARATOR"
    ENUM = "ENUM"
    SORT = "SORT"
    def __init__(self, value, nodeType):
        self.value = value
        self.nodeType = nodeType
        self.left = None
        self.right = None
        self.children = list()
        self.dataType = None
    def append(self, node):
        if not self.children:
            self.left = node
        self.children.append(node)
        if len(self.children) > 1:
            self.right = node
    def _newNode(self, node):
        if not node:
            return None

        string = str(node.value) + ", " + str(node.nodeType) + ("" if not node.dataType else ", " + str(node.dataType))
        return Node(string)
    def _create(self, old, node):
        if not old:
            return
        else:

            node.left = self._newNode(old.left)
            self._create(old.left, node.left)

            node.right = self._newNode(old.right)
            self._create(old.right,node.right)
    def _createTree(self):
        node = self._newNode(self)
        self._create(self, node)
        return node

    def __str__(self):
        return str(self._createTree())






