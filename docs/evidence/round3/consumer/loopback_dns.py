"""Minimal stdlib DNS responder/query helper; all sockets bind IPv4 loopback."""
import ipaddress, socket, socketserver, struct, threading

class Upstream(socketserver.ThreadingUDPServer):
    daemon_threads = True

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        end = 12
        labels=[]
        while data[end]:
            length=data[end];end+=1;labels.append(data[end:end+length].decode());end+=length
        end+=1
        qtype,qclass=struct.unpack('!HH',data[end:end+4]);end+=4
        host='.'.join(labels)
        if qtype not in (1,28):
            response=data[:2]+struct.pack('!HHHHH',0x8180,1,0,0,0)+data[12:end]
        else:
            addr=self.server.addresses[qtype]; raw=ipaddress.ip_address(addr).packed
            response=data[:2]+struct.pack('!HHHHH',0x8180,1,1,0,0)+data[12:end]+b'\xc0\x0c'+struct.pack('!HHIH',qtype,1,60,len(raw))+raw
        with self.server.lock:
            self.server.events.append({'host':host,'qtype':qtype,'server':self.server.tag,'answer':self.server.addresses.get(qtype)})
        sock.sendto(response,self.client_address)

def upstream(tag,addresses):
    server=Upstream(('127.0.0.1',0),Handler);server.addresses=addresses;server.tag=tag;server.events=[];server.lock=threading.Lock()
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    return server

def skipname(data,offset):
    while data[offset]:
        if data[offset]&0xc0==0xc0:return offset+2
        offset+=data[offset]+1
    return offset+1

def query(port,host,qtype):
    name=b''.join(bytes([len(p)])+p.encode() for p in host.split('.'))+b'\0'
    packet=struct.pack('!HHHHHH',1234,0x0100,1,0,0,0)+name+struct.pack('!HH',qtype,1)
    with socket.socket(socket.AF_INET,socket.SOCK_DGRAM) as sock:
        sock.settimeout(2);sock.sendto(packet,('127.0.0.1',port));data,_=sock.recvfrom(65535)
    ident,flags,qd,an,ns,ar=struct.unpack('!HHHHHH',data[:12]);offset=12
    for _ in range(qd):offset=skipname(data,offset)+4
    answers=[]
    for _ in range(an):
        offset=skipname(data,offset);typ,cl,ttl,length=struct.unpack('!HHIH',data[offset:offset+10]);offset+=10
        value=str(ipaddress.ip_address(data[offset:offset+length])) if typ in (1,28) else data[offset:offset+length].hex()
        answers.append({'type':typ,'value':value});offset+=length
    return {'rcode':flags&15,'answers':answers,'answer_count':an}

