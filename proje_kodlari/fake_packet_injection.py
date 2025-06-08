from scapy.all import *

# IP ve TCP başlıklarını ayarla
ip = IP(src="127.0.0.1", dst="127.0.0.1")
tcp = TCP(sport=1234, dport=5001, flags="S")  # SYN bayrağı

# Payload
data = b"Sahte Paket Veri"

# Paket oluştur
pkt = ip / tcp / data

# Paketi gönder
send(pkt, verbose=1)

print("[+] Sahte paket gönderildi!")
