import uuid
from enum import Enum

sizes = {
    'UINT8': 1,
    'UINT16': 2,
    'UINT24': 3,
    'UINT32': 4,
    'UINT64': 8,
    'INT8': 1,
    'INT16': 2,
    'INT24': 3, 
    'INT32': 4,
    'INT64': 8
}


class OperatorEnum(Enum):
    AND = 'and'
    OR = 'or'
    NOT = 'not'
    LESS = '<'
    MORE = '>'
    LESS_EQUAL = '<='
    MORE_EQUAL = '>='
    EQUAL = '=='
    NOT_EQUAL = '~='


class Construct(object):
    def __init__(self):
        self.id = uuid.uuid4()

class Tree():
    def __init__(self, root, nodes):
        self.start = root
        self.children = []
        self.connections = []

class Field(Construct):
    def __init__(self, name, abbv, desc, ref, dtype, size, base, mask, constraint, required):
        super(Construct, self).__init__()
        self.name = name 
        self.abbv = abbv
        self.desc = desc
        self.ref = ref
        self.dtype = dtype
        self.base = base
        self.mask = mask
        self.size = size
        self.constraint = constraint
        self.required = required
        self.child = None
        self.type = "Field"

       

class Start(Construct):
    def __init__(self, protocol_name, protocol_desc, dependency_name, dependency_pattern):
        super(Construct, self).__init__()
        self.protocol_name = protocol_name
        self.protocol_desc = protocol_desc
        self.dependency_name = dependency_name
        self.dependency_pattern = dependency_pattern
        self.child = None
        self.type = "Start"

class End(Construct):
    def __init__(self):
        super(Construct, self).__init__()
        self.type = "End"

class operator(Construct):
    def __init__(self, operator):
        super(Construct, self).__init__()
        self.operator = operator.value
        self.type = "operator"

class operator(Construct):
    def __init__(self, operand):
        super(Construct, self).__init__()
        self.operand = operand.value
        self.type = "operand"

class Expression(Construct):
    def __init__(self, operand):
        super(Construct, self).__init__()
        self.children = []
        self.expression = []
        self.type = "Expression"
