import struct, socket

def ip_to_uint32(ip):
   t = socket.inet_aton(ip)
   return struct.unpack("!I", t)[0]

def uint32_to_ip(ipn):
   t = struct.pack("!I", ipn)
   return socket.inet_ntoa(t)

if __name__ == '__main__':
    ip = '127.0.0.1'
    nip = ip_to_uint32(ip)
    print 'nip:', nip
    print 'ip:', uint32_to_ip(nip)
