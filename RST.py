from scapy.all import *
import subprocess
import ifaddr

def is_adapter_localhost(adapter, localhost_ip):
    return len([ip for ip in adapter.ips if ip.ip == localhost_ip]) > 0


def sniffPackets():
    print("Sniffing")
    localhost_ip = "127.0.0.1"
    local_ifaces = [
        adapter.name for adapter in ifaddr.get_adapters()
        if is_adapter_localhost(adapter, localhost_ip)
    ]

    iface = local_ifaces[0]

    localhost_server_port = 8000


    t = sniff(
        iface=iface,
        count=1,
        filter="host 127.0.0.1 and tcp port 8000")


    t.show()

def main():
    sniffPackets()



if __name__ == '__main__':
    main()