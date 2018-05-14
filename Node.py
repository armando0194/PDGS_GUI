import uuid
from enum import Enum

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
        self.type = None

class Field(Construct):
    def __init__(self, name, abbv, desc, ref, dtype, base, mask, constraint, required):
        super(Construct, self).__init__()
        self.name = name 
        self.abbv = abbv
        self.desc = desc
        self.ref = ref
        self.dtype = dtype
        self.base = base
        self.mask = mask
        self.constraint = constraint
        self.required = required
        self.child = None
       

class Start(Node):
    def __init__(self, protocol_name, protocol_desc, dependency_name, dependency_pattern):
        super(Construct, self).__init__()
        self.protocol_name = protocol_name
        self.protocol_desc = protocol_desc
        self.dependency_name = dependency_name
        self.dependency_pattern = dependency_pattern
        self.child = None
        self.type = "Start"

class End(Node):
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
