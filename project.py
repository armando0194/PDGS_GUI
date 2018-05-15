
from Node import Start
from Node import Field
from parser import Parser
class Project():
    def __init__(self, path):
        self.tree = self.build_tree()	
        self.path = path + '/ICMP/'

    def build_tree(self):
        root = Start("ICMP2",  "ICMP Protocol", "ip.proto", 1)

        type_ = Field("Type", "icmp_protocol.type", "Description2", None, 'UINT8', 1, None, None, None, True)
        root.child = type_

        code = Field("Code", "icmp_protocol.code", "Description3", None, 'UINT8', 1, None, None, None, True)
        type_.child = code

        checksum = Field("Checksum", "icmp_protocol.checksum", "Description4", None, 'UINT16', 2, 'HEX', None, None, True)
        code.child = checksum

        identifier = Field("Identifier", "icmp_protocol.identiier", "Description4", None, 'UINT16', 2, None, None, None, True)
        checksum.child = identifier

        sequence_number = Field("Sequence Number", "icmp_protocol.seq", "Description5", None, 'UINT16', 2, None, None, None, True)
        identifier.child = sequence_number

        data = Field("Data", "icmp_protocol.data", "Description6", None, 'BYTES', 32, None, None, None, True)
        sequence_number.child = data
        return root

    def save(self):
        parser = Parser()
        xml = parser.tree2xml(self)
        print self.path
        text_file = open(self.path+'metadata.xml', "w+")
        text_file.write(xml)
        text_file.close()
        
    
    def save_lua(self):
        print self.path+'icmp.lua'
        parser = Parser()
        xml = parser.tree2xml(self)
        script = parser.xml2lua(xml)
        
        text_file = open(self.path+'icmp.lua', "w+")
        
        text_file.write(script)
        text_file.close()

        print 'saved'
    

    