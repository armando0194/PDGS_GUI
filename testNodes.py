
from Node import Start
from Node import Field
from xml.etree import ElementTree
import json
from dicttoxml import dicttoxml

def tree2xml(root):
    xml = dicttoxml(to_dict(root), custom_root='tree', attr_type=False) 
    return xml

def xml2lua(xml, filename):
    e = ElementTree.fromstring(xml)
    type_ = e.find('type').text
    
    protocol_name = e.find('protocol_name').text
    protocol_desc = e.find('protocol_desc').text 
    dependency_name = e.find('dependency_name').text 
    dependency_pattern = e.find('dependency_pattern').text 
    script = 'protocol = Proto("{}","{}")\n\n'.format(protocol_name, protocol_desc)
    
    fields = []
    script += define_fields(e.find('child'), fields)
    field_names, _ = zip(*fields)
    script += 'protocol.fields = {' + ', '.join(field_names) + '} \n'
    script += define_dissector(fields, protocol_name)
    
    script += 'local proto = DissectorTable.get("{}")\n'.format(dependency_name)
    script += 'proto:add({}, protocol)\n'.format(dependency_pattern)

    text_file = open("Output.lua", "w")
    text_file.write(script)
    text_file.close()

def define_fields(node, fields):
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

def define_dissector(fields, name):
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

def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

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

xml = tree2xml(root)
xml2lua(xml, 'Test.lua')

pcap

pcap.findall('packet')