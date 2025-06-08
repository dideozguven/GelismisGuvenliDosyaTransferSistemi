import socket
import struct

# IP checksum hesaplayan fonksiyon
def checksum(data):
    if len(data) % 2 != 0:
        data += b'\0'  # Veri çift bayt değilse padding ekle
    s = sum(struct.unpack("!%dH" % (len(data) // 2), data))  # 16-bit'lik bloklar halinde topla
    s = (s >> 16) + (s & 0xffff)  # Taşan bitleri alta ekle
    s += s >> 16  # Tekrar taşan varsa ekle
    return ~s & 0xffff  # Sonucu tersle ve 16-bit'e indir

# Raw socket oluştur (IP seviyesinde, ham paket gönderimi için)
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

# Kaynak ve hedef IP adresleri
src_ip = "127.0.0.1"
dst_ip = "127.0.0.1"

# IP başlığı alanlarını ayarla
ip_ver = 4        # IPv4
ihl = 5           # IP header length (5*4=20 byte)
ver_ihl = (ip_ver << 4) + ihl  # Versiyon ve header length birleşimi
tos = 0           # Type of Service
payload = b"merhaba"  # Veri yükü

# TCP başlığı alanlarını ayarla
src_port = 12345
dst_port = 80
seq_num = 0
ack_num = 0
data_offset_reserved = (5 << 4) + 0  # TCP header length ve reserved alanı
flags = 0         # TCP bayrakları (SYN, ACK gibi)
window = 8192     # Pencere boyutu
checksum_tcp = 0  # TCP checksum başlangıçta 0
urg_ptr = 0       # Urgent pointer

# TCP başlığını oluştur
tcp_header = struct.pack('!HHLLBBHHH',
                         src_port,
                         dst_port,
                         seq_num,
                         ack_num,
                         data_offset_reserved,
                         flags,
                         window,
                         checksum_tcp,
                         urg_ptr)

# IP toplam uzunluğu (header + TCP header + payload)
total_length = 20 + len(tcp_header) + len(payload)
identification = 54321   # IP paket kimliği
flags_offset = 0         # Bayrak ve fragment offset
ttl = 64                 # Time To Live
protocol = socket.IPPROTO_TCP  # TCP protokolü
checksum_ip = 0          # Başlangıçta 0 checksum

# IP başlığını oluştur
ip_header = struct.pack('!BBHHHBBH4s4s',
                        ver_ihl,
                        tos,
                        total_length,
                        identification,
                        flags_offset,
                        ttl,
                        protocol,
                        checksum_ip,
                        socket.inet_aton(src_ip),  # IP adreslerini binary formata çevir
                        socket.inet_aton(dst_ip))

# IP checksum'ı hesapla
checksum_ip = checksum(ip_header)
print("Hesaplanan Checksum:", hex(checksum_ip))

# IP başlığını, doğru checksum ile tekrar oluştur
ip_header = struct.pack('!BBHHHBBH4s4s',
                        ver_ihl,
                        tos,
                        total_length,
                        identification,
                        flags_offset,
                        ttl,
                        protocol,
                        checksum_ip,
                        socket.inet_aton(src_ip),
                        socket.inet_aton(dst_ip))

# Son paket: IP header + TCP header + payload
packet = ip_header + tcp_header + payload

# Paketi hedef IP adresine gönder
s.sendto(packet, (dst_ip, 0))
print("[+] IP paketi gönderildi (TCP header + payload dahil).")
