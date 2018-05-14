class Field(Node):
    def __init__(self, name, abb, desc, ref_list, data_type, base, mask, value_cons, required):
        super(Node, self).__init__()
        self.name = name
        self.abb = abb
        self.desc = desc
        self.ref_list = ref_list
        self.data_type = data_type
        self.base = base
        self.mask = mask
        self.value_cons =v alue_cons
        self.required = required