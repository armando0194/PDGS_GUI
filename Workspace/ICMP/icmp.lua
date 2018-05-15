protocol = Proto("ICMP2","ICMP Protocol")

type = ProtoField.new("Type", "icmp_protocol.type", ftypes.UINT8, nil, nil, nil)
code = ProtoField.new("Code", "icmp_protocol.code", ftypes.UINT8, nil, nil, nil)
checksum = ProtoField.new("Checksum", "icmp_protocol.checksum", ftypes.UINT16, nil, base.HEX, nil)
identifier = ProtoField.new("Identifier", "icmp_protocol.identiier", ftypes.UINT16, nil, nil, nil)
sequence_number = ProtoField.new("Sequence Number", "icmp_protocol.seq", ftypes.UINT16, nil, nil, nil)
data = ProtoField.new("Data", "icmp_protocol.data", ftypes.BYTES, nil, nil, nil)
protocol.fields = {type, code, checksum, identifier, sequence_number, data} 
function protocol.dissector(buffer, pinfo, tree)
    pinfo.cols.protocol = protocol.name
    local subtree = tree:add(protocol, buffer(), "ICMP2 Protocol Data")
    subtree:add(type, buffer(0,1))
    subtree:add(code, buffer(1,1))
    subtree:add(checksum, buffer(2,2))
    subtree:add(identifier, buffer(4,2))
    subtree:add(sequence_number, buffer(6,2))
    subtree:add(data, buffer(8,32))
end
local proto = DissectorTable.get("ip.proto")
proto:add(1, protocol)
