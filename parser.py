
from Node import Start
from Node import Field
from xml.etree import ElementTree
import json
from dicttoxml import dicttoxml

class Parser():
    def tree2xml(self, root):
        xml = dicttoxml(self.to_dict(root), custom_root='tree', attr_type=False) 
        return xml

    def xml2lua(self, xml):
        e = ElementTree.fromstring(xml)
        e = e.find('tree')
        
        protocol_name = e.find('protocol_name').text
        protocol_desc = e.find('protocol_desc').text 
        dependency_name = e.find('dependency_name').text 
        dependency_pattern = e.find('dependency_pattern').text 
        script = 'protocol = Proto("{}","{}")\n\n'.format(protocol_name, protocol_desc)
        
        fields = []
        script += self.define_fields(e.find('child'), fields)
        field_names, _ = zip(*fields)
        script += 'protocol.fields = {' + ', '.join(field_names) + '} \n'
        script += self.define_dissector(fields, protocol_name)
        
        script += 'local proto = DissectorTable.get("{}")\n'.format(dependency_name)
        script += 'proto:add({}, protocol)\n'.format(dependency_pattern)

        return script
        

    def define_fields(self, node, fields):
        script = ''

        while node.find('child') is not None:
            proto_name = node.find('name').text
            name = proto_name.lower().replace(' ', '_')
            abbr = node.find('abbv').text 
            dtype = node.find('dtype').text 
            size = node.find('size').text
            base = 'nil' if node.find('base').text is None else 'base.' + node.find('base').text
            mask = 'nil' if node.find('mask').text is None else node.find('mask').text
            
            script += '{} = ProtoField.new("{}", "{}", ftypes.{}, nil, {}, {})\n'.format(name, proto_name, abbr, dtype, base, mask)
            fields.append((name, size))
            node = node.find('child')

        return script

    def define_dissector(self, fields, name):
        tab = '    '
        i = 0
        script = ''
        script += 'function protocol.dissector(buffer, pinfo, tree)\n'
        script += tab + 'pinfo.cols.protocol = protocol.name\n'
        script += tab + 'local subtree = tree:add(protocol, buffer(), "{} Protocol Data")\n'.format(name)

        for field in fields:
            script += tab + 'subtree:add({}, buffer({},{}))\n'.format(field[0], i, field[1])
            i += int(field[1])
        script += 'end\n'
        return script

    def to_dict(self, obj):
        return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

