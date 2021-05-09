from NodeTypeSystem import ASTNodeDataType
class DataType:
    def __init__(self, dataType, acceptableTypes = set(), resolveUsing = None):
        self.dataType = dataType
        self.acceptableTypes = acceptableTypes
        self.__children = list()
        self._skip = False
        self.resolution = resolveUsing
    def appendChild(self, dataType, propogateDown = True):
        if not isinstance(dataType, DataType):
            raise ValueError("dataType must be an instance of DataType")
        if propogateDown:
            dataType.acceptableTypes = dataType.acceptableTypes.union(self.acceptableTypes)
        self.__children.append(dataType)
    def children(self):
        return iter(self.__children)
    def skip(self, skip = None):
        if skip is not None:
            self._skip =skip
        else:
            return self._skip

class DataTypeHierarchy:
    __instance = None
    def __init__(self, root: DataType):
        self.root = root
        self.nodesCache = dict()
        self.choices = []
        self.__buildCache(self.root)
    def __buildCache(self, node: DataType):
        if not node.skip():
            self.nodesCache[node.dataType] = node
            self.choices.append((node.dataType, node.dataType))
        for child in node.children():
            self.__buildCache(child)
    @classmethod
    def build(cls):
        if cls.__instance is not None: 
            return cls.__instance
        root = DataType(ASTNodeDataType.UNDEFINED, {ASTNodeDataType.UNDEFINED})
        root.skip(True)
        boolean = DataType('Boolean', {ASTNodeDataType.BOOLEAN, ASTNodeDataType.INTEGER}, ASTNodeDataType.BOOLEAN)
        booleanArr = DataType("BooleanArray", {ASTNodeDataType.INTARRAY, ASTNodeDataType.BOOLEANARRAY, ASTNodeDataType.NUMERIC_BOOL_ARR})
        root.appendChild(boolean)
        root.appendChild(booleanArr)
        numeric = DataType('Number', {ASTNodeDataType.INTEGER, ASTNodeDataType.NUMERIC}, ASTNodeDataType.INTEGER)
        dword = DataType('DWord', resolveUsing=ASTNodeDataType.INTEGER)
        qword = DataType('QWord', resolveUsing=ASTNodeDataType.INTEGER)
        byte = DataType('Byte', resolveUsing=ASTNodeDataType.INTEGER)
        word = DataType('Word', resolveUsing=ASTNodeDataType.INTEGER)
        root.appendChild(numeric)
        numeric.appendChild(dword)
        numeric.appendChild(qword)
        numeric.appendChild(byte)
        numeric.appendChild(word)
        numericArr = DataType("NumericArr", {ASTNodeDataType.INTARRAY, ASTNodeDataType.NUMERICARRAY})
        numericArr.skip(True)
        root.appendChild(numericArr)
        qwordArr = DataType('QWordArray')
        dwordArr = DataType('DWordArray')
        byteArray = DataType('ByteArray')
        wordArray  = DataType('WordArray')
        numericArr.appendChild(qwordArr)
        numericArr.appendChild(dwordArr)
        numericArr.appendChild(byteArray)
        numericArr.appendChild(wordArray)
        string = DataType("String", {ASTNodeDataType.STRING}, ASTNodeDataType.STRING)
        root.appendChild(string)
        enum = DataType("Enumeration", {ASTNodeDataType.ENUM}, ASTNodeDataType.INTEGER)
        root.appendChild(enum)
        cls.__instance = DataTypeHierarchy(root)
        return cls.__instance
